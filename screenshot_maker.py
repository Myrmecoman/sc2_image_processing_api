import pyautogui
import cv2
import numpy as np
import pathlib
import copy
import pytesseract
import re
from threading import Thread
from PIL import Image
from Levenshtein import distance as lev
import units_dictionaries
import random


# This file extracts the data from a screenshot.
# The ocr only extracts text data, numbers are extracted using template matching


# tesserocr is faster and usually more precise on its last version. To install it :
# https://github.com/sirfz/tesserocr
USE_TESSEROCR = True
if USE_TESSEROCR:
    import tesserocr
    #print(tesserocr.tesseract_version())  # print tesseract-ocr version


current_dir = str(pathlib.Path(__file__).parent.absolute()) + "\\output\\screenshot_maker\\"


def img_to_digits(img, is_supply = True):
    # cropping each character
    num_labels, labels_ids, stats, centroids = cv2.connectedComponentsWithStats(img, 4, cv2.CV_32S)
    cropped = []
    for i in range(1, num_labels):
        new_cropped = img[:, (stats[i][cv2.CC_STAT_LEFT] - 1):(stats[i][cv2.CC_STAT_LEFT] + stats[i][cv2.CC_STAT_WIDTH] + 1)]
        cropped.append(cv2.copyMakeBorder(new_cropped, top=2, bottom=2, left=2, right=2, borderType=cv2.BORDER_CONSTANT, value=0))

    # loading templates
    templates = []
    for i in range(10):
        templates.append(cv2.imread(str(pathlib.Path(__file__).parent.absolute()) + "\\templates\\numbers_supply_minerals_gas\\" + str(i) + ".png", cv2.IMREAD_GRAYSCALE))
    if is_supply:
        templates.append(cv2.imread(str(pathlib.Path(__file__).parent.absolute()) + "\\templates\\numbers_supply_minerals_gas\\slash.png", cv2.IMREAD_GRAYSCALE))

    # matching each character with each template and keeping best match
    word = ""
    for c in range(len(cropped)):
        char_result = []
        for i in range(len(templates)):
            res = cv2.matchTemplate(cropped[c], templates[i], cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(res)
            char_result.append(max_val)
        max_index = char_result.index(max(char_result))
        if max_index == 10:
            word += '/'
        else:
            word += str(max_index)

    return word


def img_to_digits_idle_scvs_and_army(img):
    # cropping each character
    num_labels, labels_ids, stats, centroids = cv2.connectedComponentsWithStats(img, 4, cv2.CV_32S)
    cropped = []
    for i in range(1, num_labels):
        new_cropped = img[:, (stats[i][cv2.CC_STAT_LEFT] - 1):(stats[i][cv2.CC_STAT_LEFT] + stats[i][cv2.CC_STAT_WIDTH] + 1)]
        cropped.append(cv2.copyMakeBorder(new_cropped, top=2, bottom=2, left=2, right=2, borderType=cv2.BORDER_CONSTANT, value=0))

    # loading templates
    templates = []
    for i in range(10):
        templates.append(cv2.imread(str(pathlib.Path(__file__).parent.absolute()) + "\\templates\\numbers_workers_army\\" + str(i) + ".png", cv2.IMREAD_GRAYSCALE))

    # matching each character with each template and keeping best match
    word = ""
    for c in range(len(cropped)):
        char_result = []
        for i in range(len(templates)):
            res = cv2.matchTemplate(cropped[c], templates[i], cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(res)
            char_result.append(max_val)
        max_index = char_result.index(max(char_result))
        word += str(max_index)

    return word


def img_to_letters(img):
    word = ""
    if not USE_TESSEROCR:
        custom_config = r'--oem 3 --psm 7'
        pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
        word = pytesseract.image_to_string(img, output_type=pytesseract.Output.STRING, config=custom_config, lang="eng")
    else:
        word = tesserocr.image_to_text(Image.fromarray(img))
    word = word.replace('0', 'o')
    word = word.replace('2', 'z')
    word = word.replace('\n', '').lower()
    return word


def prepare_for_matching(img, thresh):
    img = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY)[1]
    return img


def prepare_for_ocr(img, thresh):
    img = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY_INV)[1]
    bordersize = 8
    img = cv2.copyMakeBorder(img, top=bordersize, bottom=bordersize, left=bordersize, right=bordersize, borderType=cv2.BORDER_CONSTANT, value=255)
    img = cv2.resize(img, (img.shape[1] * 4, img.shape[0] * 4))
    return img


# multithreaded functions -------------------------------------------------------------------------------
def supply_handle(image, supply_left, supply_right, debug = False):
    supply = cv2.cvtColor(image[22:34, 1765:1867], cv2.COLOR_BGR2GRAY)
    supply = prepare_for_matching(supply, 220)
    if debug:
        cv2.imwrite(current_dir + "supply.png", supply)
    supply_str = img_to_digits(supply)
    slash = supply_str.find('/')
    if slash == -1:
        return
    supply_left[0] = int(supply_str[:slash])
    supply_right[0] = int(supply_str[slash + 1:])

def mineral_handle(image, minerals, debug = False):
    mineral = cv2.cvtColor(image[22:34, 1519:1594], cv2.COLOR_BGR2GRAY)
    mineral = prepare_for_matching(mineral, 220)
    if debug:
        cv2.imwrite(current_dir + "mineral.png", mineral)
    minerals[0] = int(img_to_digits(mineral))

def gas_handle(image, gas, debug = False):
    gas_temp = cv2.cvtColor(image[22:34, 1642:1712], cv2.COLOR_BGR2GRAY)
    gas_temp = prepare_for_matching(gas_temp, 220)
    if debug:
        cv2.imwrite(current_dir + "gas.png", gas_temp)
    gas[0] = int(img_to_digits(gas_temp))

def idle_workers_handle(image, idle_workers, debug = False):
    idle_worker = cv2.cvtColor(image[749:764, 48:77], cv2.COLOR_BGR2GRAY)
    idle_worker = prepare_for_matching(idle_worker, 40)
    if debug:
        cv2.imwrite(current_dir + "idle_workers.png", idle_worker)
    idle_workers[0] = int(img_to_digits_idle_scvs_and_army(idle_worker))

def army_units_handle(image, army_units, debug = False):
    army_unit = cv2.cvtColor(image[749:763, 128:155], cv2.COLOR_BGR2GRAY)
    army_unit = prepare_for_matching(army_unit, 40)
    if debug:
        cv2.imwrite(current_dir + "army_units.png", army_unit)
    army_units[0] = int(img_to_digits_idle_scvs_and_army(army_unit))

def selected_single_handle(image, selected_singles, debug = False):
    selected_single = cv2.cvtColor(image[895:920, 810:1080], cv2.COLOR_BGR2GRAY)
    selected_single = prepare_for_ocr(selected_single, 40)
    if debug:
        cv2.imwrite(current_dir + "selected_single.png", selected_single)
    
    output = img_to_letters(selected_single)
    min_dist = (100, '')
    for key in units_dictionaries.building_prices:
        distance = lev(output, key)
        if distance < min_dist[0]:
            min_dist = (distance, key)
    for key in units_dictionaries.unit_prices_supply:
        distance = lev(output, key)
        if distance < min_dist[0]:
            min_dist = (distance, key)
    if min_dist[0] <= 2:
        output = min_dist[1]
    else:
        output = ''

    selected_singles[0] = output

def minimap_handle(image, minimaps):
    minimaps[0] = image[808:1065, 25:291]

def building_handle(image, buildings):
    buildings[0] = image[850:1061, 1536:1896]

def selected_group_handle(image, selected_groups):
    selected_groups[0] = image[887:1058, 661:1121]

def game_handle(image, games):
    game = copy.deepcopy(image[:823, :])
    game[:41, 1490:] = 0
    game[783:, 1518:] = 0
    game[745:, :359] = 0
    games[0] = game
# multithreaded functions -------------------------------------------------------------------------------


class screen_info:

    minimap = [None]*1
    game = [None]*1
    building = [None]*1
    selected_group = [None]*1
    supply_left = [None]*1
    supply_right = [None]*1
    minerals = [None]*1
    gas = [None]*1
    idle_workers = [None]*1
    army_units = [None]*1
    selected_single = [None]*1


    def __init__(self, debug = False):
        image = pyautogui.screenshot()
        image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        supply_thread = Thread(target=supply_handle, args=(image, self.supply_left, self.supply_right, debug))
        mineral_thread = Thread(target=mineral_handle, args=(image, self.minerals, debug))
        gas_thread = Thread(target=gas_handle, args=(image, self.gas, debug))
        idle_workers_thread = Thread(target=idle_workers_handle, args=(image, self.idle_workers, debug))
        army_units_thread = Thread(target=army_units_handle, args=(image, self.army_units, debug))
        selected_single_thread = Thread(target=selected_single_handle, args=(image, self.selected_single, debug))
        minimap_thread = Thread(target=minimap_handle, args=(image, self.minimap))
        building_thread = Thread(target=building_handle, args=(image, self.building))
        selected_group_thread = Thread(target=selected_group_handle, args=(image, self.selected_group))
        game_thread = Thread(target=game_handle, args=(image, self.game))

        supply_thread.start()
        mineral_thread.start()
        gas_thread.start()
        idle_workers_thread.start()
        army_units_thread.start()
        selected_single_thread.start()
        minimap_thread.start()
        building_thread.start()
        selected_group_thread.start()
        game_thread.start()

        supply_thread.join()
        mineral_thread.join()
        gas_thread.join()
        idle_workers_thread.join()
        army_units_thread.join()
        selected_single_thread.join()
        minimap_thread.join()
        building_thread.join()
        selected_group_thread.join()
        game_thread.join()

        self.minimap = self.minimap[0]
        self.game = self.game[0]
        self.building = self.building[0]
        self.selected_group = self.selected_group[0]
        self.supply_left = self.supply_left[0]
        self.supply_right = self.supply_right[0]
        self.minerals = self.minerals[0]
        self.gas = self.gas[0]
        self.idle_workers = self.idle_workers[0]
        self.army_units = self.army_units[0]
        self.selected_single = self.selected_single[0]

        if debug:
            print("supply_left =       " + str(self.supply_left) + "/" + str(self.supply_right))
            print("mineral =           " + str(self.minerals))
            print("gas =               " + str(self.gas))
            print("idle_workers =      " + str(self.idle_workers))
            print("army_units =        " + str(self.army_units))
            print("selected_single =   " + str(self.selected_single))
            
            cv2.imwrite(current_dir + "minimap.png", self.minimap)
            cv2.imwrite(current_dir + "building.png", self.building)
            cv2.imwrite(current_dir + "selected_group.png", self.selected_group)
            cv2.imwrite(current_dir + "game.png", self.game)
            cv2.imwrite(current_dir + "screenshot.png", image)
