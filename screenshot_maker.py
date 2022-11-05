import pyautogui
import cv2
import numpy as np
import pathlib
import copy
import pytesseract
import re
from threading import Thread
from PIL import Image


# tesserocr is faster and usually more precise on its last version. To install it :
# https://github.com/sirfz/tesserocr
USE_TESSEROCR = False
if USE_TESSEROCR:
    import tesserocr
    print(tesserocr.tesseract_version())  # print tesseract-ocr version


current_dir = str(pathlib.Path(__file__).parent.absolute())


def img_to_digits(img, is_supply = True):

    word = ""
    if not USE_TESSEROCR:
        custom_config = r'--oem 3 --psm 7'
        pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
        word = pytesseract.image_to_string(img, output_type=pytesseract.Output.STRING, config=custom_config, lang="eng")
    else:
        tesserocr.image_to_text(Image.fromarray(img))
    word = word.replace('o', '0')
    word = word.replace('O', '0')
    word = word.replace('I', '1')
    word = word.replace('l', '1')
    word = word.replace('T', '1')
    word = word.replace('Z', '2')
    word = word.replace('z', '2')
    word = word.replace('A', '4')
    word = word.replace('P', '5')
    word = word.replace('S', '5')
    word = word.replace('B', '8')
    word = word[:-1]

    if is_supply:
        word = re.sub(r'[^\d/]+', '', word)
    else:
        word = re.sub('\D','', word)
    return word


def img_to_letters(img):

    word = ""
    if not USE_TESSEROCR:
        custom_config = r'--oem 3 --psm 7'
        pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
        word = pytesseract.image_to_string(img, output_type=pytesseract.Output.STRING, config=custom_config, lang="eng")
    else:
        tesserocr.image_to_text(Image.fromarray(img))
    word = word.replace('0', 'o')
    word = word.replace('2', 'z')
    word = word[:-1].lower()
    return word


def prepare_for_ocr(img, thresh):
    img = cv2.threshold(img, thresh, 255, cv2.THRESH_BINARY_INV)[1]
    bordersize = 8
    img = cv2.copyMakeBorder(img, top=bordersize, bottom=bordersize, left=bordersize, right=bordersize, borderType=cv2.BORDER_CONSTANT, value=255)
    img = cv2.resize(img, (img.shape[1] * 4, img.shape[0] * 4))
    return img

# multithreaded functions -------------------------------------------------------------------------------
def supply_handle(image, supply_left, supply_right, debug = False):
    supply = cv2.cvtColor(image[23:33, 1763:1867], cv2.COLOR_BGR2GRAY)
    supply = prepare_for_ocr(supply, 220)
    if debug:
        cv2.imwrite(current_dir + "\\images\\supply.png", supply)
    supply_str = img_to_digits(supply)
    slash = supply_str.index('/')
    if slash == -1:
        return
    supply_left[0] = int(supply_str[:slash])
    supply_right[0] = int(supply_str[slash + 1:])

def mineral_handle(image, minerals, debug = False):
    mineral = cv2.cvtColor(image[23:33, 1519:1594], cv2.COLOR_BGR2GRAY)
    mineral = prepare_for_ocr(mineral, 220)
    if debug:
        cv2.imwrite(current_dir + "\\images\\mineral.png", mineral)
    minerals[0] = int(img_to_digits(mineral))

def gas_handle(image, gas, debug = False):
    gas_temp = cv2.cvtColor(image[23:33, 1642:1712], cv2.COLOR_BGR2GRAY)
    gas_temp = prepare_for_ocr(gas_temp, 220)
    if debug:
        cv2.imwrite(current_dir + "\\images\\gas.png", gas_temp)
    gas[0] = int(img_to_digits(gas_temp))

def idle_workers_handle(image, idle_workers, debug = False):
    idle_worker = cv2.cvtColor(image[749:764, 48:77], cv2.COLOR_BGR2GRAY)
    idle_worker = prepare_for_ocr(idle_worker, 40)
    if debug:
        cv2.imwrite(current_dir + "\\images\\idle_workers.png", idle_worker)
    idle_workers[0] = int(img_to_digits(idle_worker))

def army_units_handle(image, army_units, debug = False):
    army_unit = cv2.cvtColor(image[749:763, 128:155], cv2.COLOR_BGR2GRAY)
    army_unit = prepare_for_ocr(army_unit, 40)
    if debug:
        cv2.imwrite(current_dir + "\\images\\army_units.png", army_unit)
    army_units[0] = int(img_to_digits(army_unit))

def selected_single_handle(image, selected_singles, debug = False):
    selected_single = cv2.cvtColor(image[897:915, 810:1080], cv2.COLOR_BGR2GRAY)
    selected_single = prepare_for_ocr(selected_single, 40)
    if debug:
        cv2.imwrite(current_dir + "\\images\\selected_single.png", selected_single)
    selected_singles[0] = img_to_letters(selected_single)

def minimap_handle(image, minimaps):
    minimaps[0] = image[808:1065, 25:291]

def building_handle(image, buildings):
    buildings[0] = image[850:1061, 1536:1896]

def selected_group_handle(image, selected_groups):
    selected_groups[0] = image[887:1058, 661:1121]

def game_handle(image, games):
    game = copy.deepcopy(image[:823, :])
    game[:41, 1530:] = 0
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
            print("supply_left =       " + str(self.supply_left))
            print("supply_right =      " + str(self.supply_right))
            print("mineral =           " + str(self.minerals))
            print("gas =               " + str(self.gas))
            print("idle_workers =      " + str(self.idle_workers))
            print("army_units =        " + str(self.army_units))
            print("selected_single =   " + str(self.selected_single))
            
            cv2.imwrite(current_dir + "\\images\\minimap.png", self.minimap)
            cv2.imwrite(current_dir + "\\images\\building.png", self.building)
            cv2.imwrite(current_dir + "\\images\\selected_group.png", self.selected_group)
            cv2.imwrite(current_dir + "\\images\\game.png", self.game)
