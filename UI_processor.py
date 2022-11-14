import cv2
import numpy as np
import pathlib
import copy
from threading import Thread
from PIL import Image
from Levenshtein import distance as lev
import units_dictionaries
import mss
import random


# This file extracts the data from a screenshot.
# Everything is extracted using template matching


current_dir = str(pathlib.Path(__file__).parent.absolute()) + "\\UI_processor_debug\\"


def img_to_digits(img, is_supply = False):
    # cropping each character
    num_labels, labels_ids, stats, centroids = cv2.connectedComponentsWithStats(img, 4, cv2.CV_32S)
    cropped = []
    for i in range(1, num_labels):
        if stats[i][cv2.CC_STAT_HEIGHT] < img.shape[0] - 3: # removing small components which are certainly not characters
            continue
        new_cropped = img[:, (stats[i][cv2.CC_STAT_LEFT] - 1):(stats[i][cv2.CC_STAT_LEFT] + stats[i][cv2.CC_STAT_WIDTH] + 1)]
        cropped.append((centroids[i][0], cv2.copyMakeBorder(new_cropped, top=2, bottom=2, left=2, right=2, borderType=cv2.BORDER_CONSTANT, value=0)))
    cropped.sort()

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
            res = cv2.matchTemplate(cropped[c][1], templates[i], cv2.TM_CCOEFF_NORMED)
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
        cropped.append((centroids[i][0], cv2.copyMakeBorder(new_cropped, top=2, bottom=2, left=2, right=2, borderType=cv2.BORDER_CONSTANT, value=0)))
    cropped.sort()

    # loading templates
    templates = []
    for i in range(10):
        templates.append(cv2.imread(str(pathlib.Path(__file__).parent.absolute()) + "\\templates\\numbers_workers_army\\" + str(i) + ".png", cv2.IMREAD_GRAYSCALE))

    # matching each character with each template and keeping best match
    word = ""
    for c in range(len(cropped)):
        char_result = []
        for i in range(len(templates)):
            res = cv2.matchTemplate(cropped[c][1], templates[i], cv2.TM_CCOEFF_NORMED)
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
        cropped.append((centroids[i][0], cv2.copyMakeBorder(new_cropped, top=2, bottom=2, left=2, right=2, borderType=cv2.BORDER_CONSTANT, value=0)))
    cropped.sort()

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
            res = cv2.matchTemplate(cropped[c][1], templates[i], cv2.TM_CCOEFF_NORMED)
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
    # cropping each character
    num_labels, labels_ids, stats, centroids = cv2.connectedComponentsWithStats(img, 4, cv2.CV_32S) # this is unordered !
    cropped = []
    for i in range(1, num_labels):
        if stats[i][cv2.CC_STAT_HEIGHT] < 5: # removing small components which are certainly i dots
            continue
        new_cropped = img[:, (stats[i][cv2.CC_STAT_LEFT] - 1):(stats[i][cv2.CC_STAT_LEFT] + stats[i][cv2.CC_STAT_WIDTH] + 1)]
        cropped.append((centroids[i][0], cv2.copyMakeBorder(new_cropped, top=10, bottom=10, left=14, right=14, borderType=cv2.BORDER_CONSTANT, value=0)))
    cropped.sort()

    # loading templates
    templates = []
    for i in range(26):
        templates.append(cv2.imread(str(pathlib.Path(__file__).parent.absolute()) + "\\templates\\letters\\" + chr(ord('a') + i) + ".png", cv2.IMREAD_GRAYSCALE))
    for i in range(26):
        templates.append(cv2.imread(str(pathlib.Path(__file__).parent.absolute()) + "\\templates\\letters\\" + chr(ord('a') + i) + "m.png", cv2.IMREAD_GRAYSCALE))
    
    # matching each character with each template and keeping best match
    word = ""
    for c in range(len(cropped)):
        char_result = []
        for i in range(len(templates)):
            res = cv2.matchTemplate(cropped[c][1], templates[i], cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(res)
            char_result.append(max_val)
        max_index = char_result.index(max(char_result))
        if max_index >= 26:
            word += chr(ord('a') + max_index - 26)
        else:
            word += chr(ord('a') + max_index)

    return word


# multithreaded functions -------------------------------------------------------------------------------
def supply_handle(image, supply_left, supply_right, debug = False):
    supply = image[22:34, 1765:1867, 2]
    supply = cv2.threshold(supply, 220, 255, cv2.THRESH_BINARY)[1]
    if debug:
        cv2.imwrite(current_dir + "supply.png", supply)
    supply_str = img_to_digits(supply, True)
    slash = supply_str.find('/')
    if slash == -1:
        supply_left[0] = -1
        supply_right[0] = -1
    else:
        supply_left[0] = int(supply_str[:slash])
        supply_right[0] = int(supply_str[slash + 1:])

def mineral_handle(image, minerals, debug = False):
    mineral = image[22:34, 1519:1594]
    left = np.array([230, 230, 230])
    right = np.array([255, 255, 255])
    mineral = cv2.inRange(mineral, left, right)
    if debug:
        cv2.imwrite(current_dir + "mineral.png", mineral)
    str_nb = img_to_digits(mineral)
    if str_nb == '':
        str_nb = '-1'
    minerals[0] = int(str_nb)

def gas_handle(image, gas, debug = False):
    gas_temp = image[22:34, 1645:1712]
    left = np.array([230, 230, 230])
    right = np.array([255, 255, 255])
    gas_temp = cv2.inRange(gas_temp, left, right)
    if debug:
        cv2.imwrite(current_dir + "gas.png", gas_temp)
    str_nb = img_to_digits(gas_temp)
    if str_nb == '':
        str_nb = '-1'
    gas[0] = int(str_nb)

def idle_workers_handle(image, idle_workers, debug = False):
    idle_worker = cv2.cvtColor(image[749:764, 48:77], cv2.COLOR_BGR2GRAY)
    idle_worker = cv2.threshold(idle_worker, 80, 255, cv2.THRESH_BINARY)[1]
    if debug:
        cv2.imwrite(current_dir + "idle_workers.png", idle_worker)
    str_nb = img_to_digits_idle_scvs_and_army(idle_worker)
    if str_nb == '':
        str_nb = '-1'
    idle_workers[0] = int(str_nb)

def army_units_handle(image, army_units, debug = False):
    army_unit = cv2.cvtColor(image[749:763, 128:155], cv2.COLOR_BGR2GRAY)
    army_unit = cv2.threshold(army_unit, 80, 255, cv2.THRESH_BINARY)[1]
    if debug:
        cv2.imwrite(current_dir + "army_units.png", army_unit)
    str_nb = img_to_digits_idle_scvs_and_army(army_unit)
    if str_nb == '':
        str_nb = '-1'
    army_units[0] = int(str_nb)

def selected_single_handle(image, selected_singles, debug = False):
    selected_single = cv2.cvtColor(image[895:920, 810:1080], cv2.COLOR_BGR2GRAY)
    selected_single = cv2.threshold(selected_single, 40, 255, cv2.THRESH_BINARY)[1]
    if debug:
        cv2.imwrite(current_dir + "selected_single.png", selected_single)
    
    output = img_to_letters(selected_single)
    min_dist = (100, '')
    for key in units_dictionaries.buildings:
        distance = lev(output, key)
        if distance < min_dist[0]:
            min_dist = (distance, key)
    for key in units_dictionaries.units:
        distance = lev(output, key)
        if distance < min_dist[0]:
            min_dist = (distance, key)
    if min_dist[0] <= 2:
        output = min_dist[1]
    else:
        output = ''
    selected_singles[0] = output

def minimap_handle(image, minimaps, debug = False):
    minimaps[0] = image[808:1065, 25:291]
    if debug:
        cv2.imwrite(current_dir + "minimap.png", minimaps[0])

def building_handle(image, buildings, debug = False):
    buildings[0] = image[850:1061, 1536:1896]
    if debug:
        cv2.imwrite(current_dir + "building.png", buildings[0])

def selected_group_handle(image, selected_groups, debug = False):
    selected_groups[0] = image[887:1058, 661:1121]
    if debug:
        cv2.imwrite(current_dir + "selected_group.png", selected_groups[0])

def game_handle(image, games, debug = False):
    game = copy.deepcopy(image[:823, :])
    game[:41, 1490:] = 0
    game[783:, 1518:] = 0
    game[745:, :359] = 0
    games[0] = game
    if debug:
        cv2.imwrite(current_dir + "game.png", games[0])

def extraction_handle(image, minerals, gases, debug = False):
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
        extraction = cv2.threshold(extraction, 130, 255, cv2.THRESH_BINARY)[1]
        extraction[:, 12] = 0
        extraction[:, 24] = 0
        if debug:
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
        extraction = cv2.threshold(extraction, 130, 255, cv2.THRESH_BINARY)[1]
        extraction[:, 13] = 0
        extraction[:, 24] = 0
        if debug:
            cv2.imwrite(current_dir + "gas_extraction" + str(len(gas_list)) + ".png", extraction)
        extraction = img_to_digits_extraction(extraction)
        slash = extraction.find('/')
        if slash == -1:
            print("ERROR: no / found")
        else:
            gas_list.append(((int(extraction[:slash]), 3), (pt[0] + gas_temp.shape[0] + 50, pt[1] + gas_temp.shape[1] - 1)))
    
    minerals[0] = mineral_list
    gases[0] = gas_list

def right_availability_handle(image, right_buttons, debug = False):
    buildings = [None]*1
    building_handle(image, buildings)
    buildings = buildings[0]
    hsv = cv2.cvtColor(buildings, cv2.COLOR_BGR2HSV)
    hsv = hsv[:, :, 1]
    if debug:
        cv2.imwrite(current_dir + "right_window_availability.png", hsv)
    rows = [[False, False, False, False, False],
            [False, False, False, False, False],
            [False, False, False, False, False]]
    x = 0
    y = 0
    for i in range(30, 180, 74):
        for j in range(40, 325, 71):
            square = hsv[i-25:i+25, j-25:j+25]
            # cv2.imwrite(current_dir + "right_window_availability" + str(y) + str(x) + ".png", square)
            avg = square.mean()
            if avg >= 5:
                rows[y][x] = True
            else:
                rows[y][x] = False
            x += 1
        y += 1
        x = 0
    right_buttons[0] = rows

# multithreaded functions -------------------------------------------------------------------------------


class UI_processor:
    # setting [None]*1 in order to pass as pointers in threads
    image = None
    minimap = [None]*1                       # image
    game = [None]*1                          # image
    building = [None]*1                      # image
    selected_group = [None]*1                # image
    supply_left = [None]*1                   # int
    supply_right = [None]*1                  # int
    minerals = [None]*1                      # int
    gas = [None]*1                           # int
    idle_workers = [None]*1                  # int
    army_units = [None]*1                    # int
    selected_single = [None]*1               # string
    mineral_extraction_infos = [None]*1      # list of ((int, int), (int, int)) corresponding to (( nb_workers/workers_max ), ( position_x, position_y )) where position is click position to select the command center
    gas_extraction_infos = [None]*1          # list of ((int, int), (int, int)) corresponding to (( nb_workers/workers_max ), ( position_x, position_y )) where position is click position to select the refinery
    right_window_button_available = [None]*1 # list of list of bool
    base_locations = []                      # list of base locations on minimap
    resources_mask = []                      # minimap resources
    allies_mask = []                         # minimap allies
    enemies_mask = []                        # minimap enemies
    enemy_starting_base = []                 # enemy starting base position on the minimap, a tuple (int, int)
    our_starting_base = []                   # our starting base position on the minimap, a tuple (int, int)


    def __init__(self,
    debug = False,
    get_supply = False,
    get_mineral = False,
    get_gas = False,
    get_idle_workers = False,
    get_army_units = False,
    get_selected_single = False,
    get_minimap = False,
    get_building = False,
    get_selected_group = False,
    get_game_image = False,
    get_extraction_rate = False,
    get_minimap_init_values = False,
    get_right_window_buttons_availability = False): # should only be called once at game startup, this detects mineral patches, the enemy base position and our position

        if debug:
            get_supply = True
            get_mineral = True
            get_gas = True
            get_idle_workers = True
            get_army_units = True
            get_selected_single = True
            get_minimap = True
            get_building = True
            get_selected_group = True
            get_game_image = True
            get_extraction_rate = True
            get_minimap_init_values = True
            get_right_window_buttons_availability = True
        
        if get_minimap_init_values:
            get_minimap = True

        with mss.mss() as mss_instance:
            monitor = mss_instance.monitors[1]
            self.image = cv2.cvtColor(np.array(mss_instance.grab(monitor)), cv2.COLOR_BGRA2BGR)

        # declaring threads
        threads = [None, None, None, None, None, None, None, None, None, None, None, None]
        if get_supply:
            threads[0] = Thread(target=supply_handle, args=(self.image, self.supply_left, self.supply_right, debug))
        if get_mineral:
            threads[1] = Thread(target=mineral_handle, args=(self.image, self.minerals, debug))
        if get_gas:
            threads[2] = Thread(target=gas_handle, args=(self.image, self.gas, debug))
        if get_idle_workers:
            threads[3] = Thread(target=idle_workers_handle, args=(self.image, self.idle_workers, debug))
        if get_army_units:
            threads[4] = Thread(target=army_units_handle, args=(self.image, self.army_units, debug))
        if get_selected_single:
            threads[5] = Thread(target=selected_single_handle, args=(self.image, self.selected_single, debug))
        if get_minimap:
            threads[6] = Thread(target=minimap_handle, args=(self.image, self.minimap, debug))
        if get_building:
            threads[7] = Thread(target=building_handle, args=(self.image, self.building, debug))
        if get_selected_group:
            threads[8] = Thread(target=selected_group_handle, args=(self.image, self.selected_group, debug))
        if get_game_image:
            threads[9] = Thread(target=game_handle, args=(self.image, self.game, debug))
        if get_extraction_rate:
            threads[10] = Thread(target=extraction_handle, args=(self.image, self.mineral_extraction_infos, self.gas_extraction_infos, debug))
        if get_right_window_buttons_availability:
            threads[11] = Thread(target=right_availability_handle, args=(self.image, self.right_window_button_available, debug))
        
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
        self.right_window_button_available = self.right_window_button_available[0]

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

            # finding approximate base locations and enemy base starting position
            if get_minimap_init_values:
                # base locations
                kernel = np.ones((7, 7), np.uint8)
                locations = copy.deepcopy(self.resources_mask)
                locations = cv2.dilate(locations, kernel)
                num_labels, labels_ids, values, centroids = cv2.connectedComponentsWithStats(locations, 4)
                for i in range(1, num_labels):
                    if values[i][-1] < 200 : # components with small areas are very probably small minerals patches blocking passages
                        continue
                    self.base_locations.append([int(centroids[i][0]), int(centroids[i][1])])
                    locations[int(centroids[i][1])][int(centroids[i][0])] = 100
                
                # enemy base starting position
                left = np.array([0, 0, 230])
                right = np.array([5, 5, 255])
                red_minimap = cv2.inRange(self.minimap, left, right)
                kernel = np.ones((9, 9), np.uint8)
                red_minimap = cv2.dilate(red_minimap, kernel)
                _, _, _, centroids = cv2.connectedComponentsWithStats(red_minimap, 4, cv2.CV_32S)
                if len(centroids) > 1:
                    self.enemy_starting_base = (int(centroids[1][0]), int(centroids[1][1]))
                else:
                    self.enemy_starting_base = None # red marker not found

                # our base starting position
                left = np.array([0, 140, 0])
                right = np.array([0, 255, 0])
                green_minimap = cv2.inRange(self.minimap, left, right)
                kernel = np.ones((9, 9), np.uint8)
                green_minimap = cv2.dilate(green_minimap, kernel)
                _, _, _, centroids = cv2.connectedComponentsWithStats(green_minimap, 4, cv2.CV_32S)
                self.our_starting_base = (int(centroids[1][0]), int(centroids[1][1]))

                if debug:
                    cv2.imwrite(current_dir + "locations.png", locations)
                    cv2.imwrite(current_dir + "enemy_location.png", red_minimap)
                    cv2.imwrite(current_dir + "our_location.png", green_minimap)
            
            if debug:
                cv2.imwrite(current_dir + "ressources.png", self.resources_mask)
                cv2.imwrite(current_dir + "allies.png", self.allies_mask)
                cv2.imwrite(current_dir + "enemies.png", self.enemies_mask)

        if debug:
            print("supply =                   " + str(self.supply_left) + "/" + str(self.supply_right))
            print("mineral =                  " + str(self.minerals))
            print("gas =                      " + str(self.gas))
            print("idle_workers =             " + str(self.idle_workers))
            print("army_units =               " + str(self.army_units))
            print("selected_single =          " + str(self.selected_single))
            print("mineral_extraction_infos = " + str(self.mineral_extraction_infos))
            print("gas_extraction_infos =     " + str(self.gas_extraction_infos))
            print("enemy base position =      " + str(self.enemy_starting_base))
            print("our base position =        " + str(self.our_starting_base))
            print("right availability =       " + str(self.right_window_button_available))
            cv2.imwrite(current_dir + "screenshot.png", self.image)
