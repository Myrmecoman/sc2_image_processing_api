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
import time
import mss


# This file extracts the data from a screenshot.
# The ocr only extracts text data, numbers are extracted using template matching


# tesserocr is faster and usually more precise on its last version. To install it :
# https://github.com/sirfz/tesserocr
USE_TESSEROCR = True
if USE_TESSEROCR:
    import tesserocr
    #print(tesserocr.tesseract_version())  # print tesseract-ocr version


current_dir = str(pathlib.Path(__file__).parent.absolute()) + "\\output\\"


def img_to_digits(img, is_supply = False):
    # cropping each character
    num_labels, labels_ids, stats, centroids = cv2.connectedComponentsWithStats(img, 4, cv2.CV_32S)
    cropped = []
    for i in range(1, num_labels):
        if stats[i][cv2.CC_STAT_HEIGHT] < img.shape[0] - 3: # removing small components which are certainly not characters
            continue
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
        max_value = max(char_result)
        if max_value < 0.6:
            continue
        max_index = char_result.index(max_value)
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


def img_to_digits_extraction(img):
    # cropping each character
    num_labels, labels_ids, stats, centroids = cv2.connectedComponentsWithStats(img, 4, cv2.CV_32S)
    cropped = []
    for i in range(1, num_labels):
        if stats[i][cv2.CC_STAT_HEIGHT] < img.shape[0] - 3: # removing small components which are certainly not characters
            continue
        if stats[i][cv2.CC_STAT_AREA] > 100: # too big, can't be a character
            continue
        new_cropped = img[:, (stats[i][cv2.CC_STAT_LEFT] - 1):(stats[i][cv2.CC_STAT_LEFT] + stats[i][cv2.CC_STAT_WIDTH] + 1)]
        cropped.append(cv2.copyMakeBorder(new_cropped, top=2, bottom=2, left=2, right=2, borderType=cv2.BORDER_CONSTANT, value=0))

    # loading templates
    templates = []
    for i in range(10):
        templates.append(cv2.imread(str(pathlib.Path(__file__).parent.absolute()) + "\\templates\\numbers_supply_minerals_gas\\" + str(i) + ".png", cv2.IMREAD_GRAYSCALE))
    templates.append(cv2.imread(str(pathlib.Path(__file__).parent.absolute()) + "\\templates\\numbers_supply_minerals_gas\\slash.png", cv2.IMREAD_GRAYSCALE))

    # matching each character with each template and keeping best match
    word = ""
    for c in range(len(cropped)):
        char_result = []
        for i in range(len(templates)):
            res = cv2.matchTemplate(cropped[c], templates[i], cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(res)
            char_result.append(max_val)
        max_value = max(char_result)
        if max_value < 0.6:
            continue
        max_index = char_result.index(max_value)
        if max_index == 10:
            word += '/'
        else:
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
    supply = image[22:34, 1765:1867, 2]
    supply = prepare_for_matching(supply, 220)
    if debug:
        cv2.imwrite(current_dir + "supply.png", supply)
    supply_str = img_to_digits(supply, True)
    slash = supply_str.find('/')
    if slash == -1:
        return
    supply_left[0] = int(supply_str[:slash])
    supply_right[0] = int(supply_str[slash + 1:])

def mineral_handle(image, minerals, debug = False):
    mineral = image[22:34, 1519:1594, 2]
    mineral = prepare_for_matching(mineral, 230)
    if debug:
        cv2.imwrite(current_dir + "mineral.png", mineral)
    minerals[0] = int(img_to_digits(mineral))

def gas_handle(image, gas, debug = False):
    gas_temp = image[22:34, 1645:1712, 2]
    gas_temp = prepare_for_matching(gas_temp, 230)
    if debug:
        cv2.imwrite(current_dir + "gas.png", gas_temp)
    gas[0] = int(img_to_digits(gas_temp))

def idle_workers_handle(image, idle_workers, debug = False):
    idle_worker = cv2.cvtColor(image[749:764, 48:77], cv2.COLOR_BGR2GRAY)
    idle_worker = prepare_for_matching(idle_worker, 80)
    if debug:
        cv2.imwrite(current_dir + "idle_workers.png", idle_worker)
    idle_workers[0] = int(img_to_digits_idle_scvs_and_army(idle_worker))

def army_units_handle(image, army_units, debug = False):
    army_unit = cv2.cvtColor(image[749:763, 128:155], cv2.COLOR_BGR2GRAY)
    army_unit = prepare_for_matching(army_unit, 80)
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

def extraction_handle(image, minerals, gases):
    mineral_temp = cv2.imread(str(pathlib.Path(__file__).parent.absolute()) + "\\templates\\resource_templates\\mineral.png")
    gas_temp = cv2.imread(str(pathlib.Path(__file__).parent.absolute()) + "\\templates\\resource_templates\\gas.png")

    res_mineral = cv2.matchTemplate(image, mineral_temp, cv2.TM_CCOEFF_NORMED)
    res_gas = cv2.matchTemplate(image, gas_temp, cv2.TM_CCOEFF_NORMED)

    threshold = 0.9
    loc_mineral = np.where(res_mineral >= threshold)
    loc_gas = np.where(res_gas >= threshold)

    mineral_list = []
    for pt in zip(*loc_mineral[::-1]):
        extraction = image[pt[1]:pt[1] + mineral_temp.shape[1] - 2, (pt[0] + 105):(pt[0] + 180), 2]
        extraction = prepare_for_matching(extraction, 130)
        extraction[:, 12] = 0
        extraction[:, 24] = 0
        cv2.imwrite(current_dir + "mineral_extraction" + str(len(mineral_list)) + ".png", extraction)
        extraction = img_to_digits_extraction(extraction)
        slash = extraction.find('/')
        if slash == -1:
            print("ERROR: no / found")
        else:
            left = int(extraction[:slash])
            right = int(extraction[slash + 1:])
            if right > 16: # the program often get mistaken between 6 and 8 (tells 12/18 instead of 12/16), this acts as a patch for now since mineral patches can handle 16 workers max
                right = 16
            mineral_list.append(((left, right), (pt[0] + mineral_temp.shape[0] - 1, pt[1] + mineral_temp.shape[1] - 1)))

    gas_list = []
    for pt in zip(*loc_gas[::-1]):
        extraction = image[pt[1]:pt[1] + gas_temp.shape[1], (pt[0] + 103):(pt[0] + 150), 2]
        extraction = prepare_for_matching(extraction, 130)
        extraction[:, 13] = 0
        extraction[:, 24] = 0
        cv2.imwrite(current_dir + "gas_extraction" + str(len(gas_list)) + ".png", extraction)
        extraction = img_to_digits_extraction(extraction)
        slash = extraction.find('/')
        if slash == -1:
            print("ERROR: no / found")
        else:
            gas_list.append(((int(extraction[:slash]), 3), (pt[0] + gas_temp.shape[0] + 50, pt[1] + gas_temp.shape[1] - 1)))
    
    minerals[0] = mineral_list
    gases[0] = gas_list

# multithreaded functions -------------------------------------------------------------------------------


class screen_info:
    # setting [None]*1 in order to pass as pointers in threads
    minimap = [None]*1                  # image
    game = [None]*1                     # image
    building = [None]*1                 # image
    selected_group = [None]*1           # image
    supply_left = [None]*1              # int
    supply_right = [None]*1             # int
    minerals = [None]*1                 # int
    gas = [None]*1                      # int
    idle_workers = [None]*1             # int
    army_units = [None]*1               # int
    selected_single = [None]*1          # string
    mineral_extraction_infos = [None]*1 # list of ((int, int), (int, int)) corresponding to (( nb_workers/workers_max ), ( position_x, position_y )) where position is click position to select the command center
    gas_extraction_infos = [None]*1     # list of ((int, int), (int, int)) corresponding to (( nb_workers/workers_max ), ( position_x, position_y )) where position is click position to select the refinery
    base_locations = []                 # list of base locations on minimap
    resources_mask = []                 # minimap resources
    allies_mask = []                    # minimap allies
    enemies_mask = []                   # minimap enemies


    def __init__(self,
    debug = False,
    get_supply = True,
    get_mineral = True,
    get_gas = True,
    get_idle_workers = True,
    get_army_units = True,
    get_selected_single = True,
    get_minimap = True,
    get_building = True,
    get_selected_group = True,
    get_game_image = True,
    get_extraction_rate = True,
    get_mineral_locations = False): # should only be called once at game startup

        image = []
        with mss.mss() as mss_instance:
            monitor = mss_instance.monitors[1]
            image = cv2.cvtColor(np.array(mss_instance.grab(monitor)), cv2.COLOR_BGRA2BGR)

        # declaring threads
        threads = [None, None, None, None, None, None, None, None, None, None, None]
        if get_supply:
            threads[0] = Thread(target=supply_handle, args=(image, self.supply_left, self.supply_right, debug))
        if get_mineral:
            threads[1] = Thread(target=mineral_handle, args=(image, self.minerals, debug))
        if get_gas:
            threads[2] = Thread(target=gas_handle, args=(image, self.gas, debug))
        if get_idle_workers:
            threads[3] = Thread(target=idle_workers_handle, args=(image, self.idle_workers, debug))
        if get_army_units:
            threads[4] = Thread(target=army_units_handle, args=(image, self.army_units, debug))
        if get_selected_single:
            threads[5] = Thread(target=selected_single_handle, args=(image, self.selected_single, debug))
        if get_minimap:
            threads[6] = Thread(target=minimap_handle, args=(image, self.minimap))
        if get_building:
            threads[7] = Thread(target=building_handle, args=(image, self.building))
        if get_selected_group:
            threads[8] = Thread(target=selected_group_handle, args=(image, self.selected_group))
        if get_game_image:
            threads[9] = Thread(target=game_handle, args=(image, self.game))
        if get_extraction_rate:
            threads[10] = Thread(target=extraction_handle, args=(image, self.mineral_extraction_infos, self.gas_extraction_infos))
        
        # running threads
        for i in threads:
            if i is not None:
                i.start()
        
        # joining threads
        for i in threads:
            if i is not None:
                i.join()

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
        self.mineral_extraction_infos = self.mineral_extraction_infos[0]
        self.gas_extraction_infos = self.gas_extraction_infos[0]

        if get_minimap:
            # getting resources
            color = np.array([241, 191, 126])
            self.resources_mask = cv2.inRange(self.minimap, color, color)
            # getting allies
            left = np.array([0, 140, 0])
            right = np.array([0, 255, 0])
            self.allies_mask = cv2.inRange(self.minimap, left, right)
            # getting enemies
            left = np.array([0, 0, 190])
            right = np.array([0, 0, 255])
            self.enemies_mask = cv2.inRange(self.minimap, left, right)

            # finding approximate base locations
            if get_mineral_locations:
                kernel = np.ones((7, 7), np.uint8)
                locations = copy.deepcopy(self.resources_mask)
                locations = cv2.dilate(locations, kernel)
                num_labels, labels_ids, values, centroids = cv2.connectedComponentsWithStats(locations, 4)
                for i in range(1, num_labels):
                    if values[i][-1] < 200 : # components with small areas are very probably small minerals patches blocking passages
                        continue
                    self.base_locations.append([int(centroids[i][0]), int(centroids[i][1])])
                    locations[int(centroids[i][1])][int(centroids[i][0])] = 100
                
                if debug:
                    cv2.imwrite(current_dir + "locations.png", locations)
            
            if debug:
                cv2.imwrite(current_dir + "minimap.png", self.minimap)
                cv2.imwrite(current_dir + "ressources.png", self.resources_mask)
                cv2.imwrite(current_dir + "allies.png", self.allies_mask)
                cv2.imwrite(current_dir + "enemies.png", self.enemies_mask)

        if debug:
            if get_supply:
                print("supply =                   " + str(self.supply_left) + "/" + str(self.supply_right))
            if get_mineral:
                print("mineral =                  " + str(self.minerals))
            if get_gas:
                print("gas =                      " + str(self.gas))
            if get_idle_workers:
                print("idle_workers =             " + str(self.idle_workers))
            if get_army_units:
                print("army_units =               " + str(self.army_units))
            if get_selected_single:
                print("selected_single =          " + str(self.selected_single))
            if get_extraction_rate:
                print("mineral_extraction_infos = " + str(self.mineral_extraction_infos))
                print("gas_extraction_infos =     " + str(self.gas_extraction_infos))

            if get_building:
                cv2.imwrite(current_dir + "building.png", self.building)
            if get_selected_group:
                cv2.imwrite(current_dir + "selected_group.png", self.selected_group)
            if get_game_image:
                cv2.imwrite(current_dir + "game.png", self.game)
            cv2.imwrite(current_dir + "screenshot.png", image)
