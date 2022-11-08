import time
from screenshot_maker import screen_info
from clicker_helper import clicker_helper as clicker_help
import pyautogui
import numpy as np
import cv2
import pathlib
import mss
import units_dictionaries
import keyboard


# while we don't detect a mineral sprite, the game has not started / is not open
mineral_temp = cv2.imread(str(pathlib.Path(__file__).parent.absolute()) + "\\templates\\resource_templates\\mineral.png")
while not keyboard.is_pressed("esc"):
    image = []
    with mss.mss() as mss_instance:
        monitor = mss_instance.monitors[1]
        image = cv2.cvtColor(np.array(mss_instance.grab(monitor)), cv2.COLOR_BGRA2BGR)
    image = image[50:880, 460:1460]

    res_mineral = cv2.matchTemplate(image, mineral_temp, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc_mineral = np.where(res_mineral >= threshold)
    found = False
    for i in zip(*loc_mineral[::-1]):
        found = True
        break
    if found:
        break

print("The game started")

# put command center in control group 1
pyautogui.moveTo(1920/2, 400, duration=0.0, _pause=False)
pyautogui.click()
time.sleep(0.2)
pyautogui.keyDown("shift")
pyautogui.press("1")
pyautogui.keyUp("shift")

time.sleep(0.2)

# workers in group 2
pyautogui.moveTo(100, 100, duration=0.0, _pause=True)
pyautogui.dragTo(1500, 800, button='left')
time.sleep(0.2)
pyautogui.keyDown("shift")
pyautogui.press("2")
pyautogui.keyUp("shift")
time.sleep(0.2)

#print("sleep")
#time.sleep(1000)

# https://www.youtube.com/watch?v=X8aAAenFkrU&t=274s we can keep going but for now only print marines, when reaching the end of the array we keep making supply depots and marines
build_order = ["scv", "supply depot", "scv", "scv", "barracks", "barracks", "barracks", "barracks", "scv", "supply depot"]# , "orbital command"]
barracks_pos = []
while not keyboard.is_pressed("esc"):

    info = screen_info(
        debug = False,
        get_supply = True,
        get_mineral = True,
        get_gas = False,
        get_idle_workers = True,
        get_army_units = True,
        get_selected_single = False,
        get_minimap = False,
        get_building = False,
        get_selected_group = False,
        get_game_image = False,
        get_extraction_rate = False,
        minimap_init_values = False)
    
    object = None
    if build_order[0] in units_dictionaries.buildings:
        object = units_dictionaries.buildings[build_order[0]]
    else:
        object = units_dictionaries.units[build_order[0]]

    if info.minerals >= object[0]:

        if build_order[0] == "scv":
            pyautogui.press("1")
            pyautogui.moveTo(clicker_help.right_window[0][0][0], clicker_help.right_window[0][0][1], duration=0.0, _pause=False)
            pyautogui.click()

        if build_order[0] == "supply depot" or build_order[0] == "barracks":
            for i in range(300, 1610, 200):
                breaking = False
                for j in range(40, 800, 200):
                    if info.idle_workers > 0:
                        pyautogui.press("tab") # my key for idle workers is tab
                    else:
                        pyautogui.press("2")
                    info = screen_info(
                        debug = False,
                        get_supply = False,
                        get_mineral = True,
                        get_gas = False,
                        get_idle_workers = False,
                        get_army_units = False,
                        get_selected_single = False,
                        get_minimap = False,
                        get_building = False,
                        get_selected_group = False,
                        get_game_image = False,
                        get_extraction_rate = False,
                        minimap_init_values = False)
                    if build_order[0] == "supply depot":
                        pyautogui.moveTo(clicker_help.right_window[2][0][0], clicker_help.right_window[2][0][1], duration=0.0, _pause=False)
                        pyautogui.click()
                        pyautogui.moveTo(clicker_help.right_window[0][2][0], clicker_help.right_window[0][2][1], duration=0.0, _pause=False)
                        pyautogui.click()
                    else:
                        pyautogui.moveTo(clicker_help.right_window[2][0][0], clicker_help.right_window[2][0][1], duration=0.0, _pause=False)
                        pyautogui.click()
                        pyautogui.moveTo(clicker_help.right_window[1][0][0], clicker_help.right_window[1][0][1], duration=0.0, _pause=False)
                        pyautogui.click()
                    pyautogui.moveTo(i, j, duration=0.0, _pause=False)
                    pyautogui.click()
                    new_info = screen_info(
                        debug = False,
                        get_supply = False,
                        get_mineral = True,
                        get_gas = False,
                        get_idle_workers = False,
                        get_army_units = False,
                        get_selected_single = False,
                        get_minimap = False,
                        get_building = False,
                        get_selected_group = False,
                        get_game_image = False,
                        get_extraction_rate = False,
                        minimap_init_values = False)
                    if new_info.minerals < info.minerals: # success
                        breaking = True
                        if build_order[0] == "barracks":
                            barracks_pos.append((i, j))
                        break
                if breaking:
                    break

        build_order.pop(0)

        if len(build_order) == 0:
            break

for i in barracks_pos:
    pyautogui.moveTo(i[0], i[1], duration=0.0, _pause=False)
    pyautogui.click()
    pyautogui.keyDown("shift")
    pyautogui.press("3")
    pyautogui.keyUp("shift")

# build order is done, now build only marines and attack
while not keyboard.is_pressed("esc"):

    info = screen_info(
        debug = False,
        get_supply = True,
        get_mineral = True,
        get_gas = False,
        get_idle_workers = False,
        get_army_units = True,
        get_selected_single = False,
        get_minimap = False,
        get_building = False,
        get_selected_group = False,
        get_game_image = False,
        get_extraction_rate = False,
        minimap_init_values = False)
    
    if info.minerals >= 50:
        pyautogui.press("3")
        pyautogui.moveTo(clicker_help.right_window[0][0][0], clicker_help.right_window[0][0][1], duration=0.0, _pause=False)
        pyautogui.click()
    
    if info.army_units > 12:
        pyautogui.press("F2")
        break

print("end")
