import time
from UI_processor import UI_processor
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

# command center in control group 1
pyautogui.moveTo(1920/2, 400, duration=0.0, _pause=False)
pyautogui.click()
time.sleep(0.05)
pyautogui.keyDown("shift") # shift + number adds units to a control group on my keybinds, change accordingly to yours
pyautogui.press("1")
pyautogui.keyUp("shift")
time.sleep(0.05)

# workers in control group 2
pyautogui.moveTo(100, 100, duration=0.0, _pause=True)
pyautogui.dragTo(1500, 800, button='left')
time.sleep(0.05)
pyautogui.keyDown("shift")
pyautogui.press("2")
pyautogui.keyUp("shift")
time.sleep(0.05)

startup_info = UI_processor(minimap_init_values=True)

x = 50

# https://www.youtube.com/watch?v=X8aAAenFkrU&t=274s we can keep going but for now only print marines, when reaching the end of the array we keep making supply depots and marines
build_order = ["scv", "supply depot", "scv", "scv", "barracks", "barracks", "barracks", "barracks", "scv", "supply depot"]
barracks_pos = []
start_time = 0
while not keyboard.is_pressed("esc"):

    if len(build_order) == 0:
        break
    
    time.sleep(0.2)

    info = UI_processor(get_mineral=True, get_idle_workers=True)
    
    object = None
    if build_order[0] in units_dictionaries.buildings:
        object = units_dictionaries.buildings[build_order[0]]
    else:
        object = units_dictionaries.units[build_order[0]]
    
    if info.minerals < object[0]:
        continue
    
    time.sleep(0.2)

    if build_order[0] == "scv":
        pyautogui.moveTo(clicker_help.control_groups[0][0], clicker_help.control_groups[0][1], duration=0.0, _pause=False)
        pyautogui.click()
        time.sleep(0.1)
        pyautogui.moveTo(clicker_help.right_window[0][0][0], clicker_help.right_window[0][0][1], duration=0.0, _pause=False)
        pyautogui.click()
        print("built : " + build_order.pop(0))

    elif (build_order[0] == "supply depot" or build_order[0] == "barracks") and (start_time == 0 or (time.time() - start_time) > 20):
        for j in range(x, 800, 200):
            breaking = False
            for i in range(300, 1610, 200):
                # go back on command center view
                pyautogui.moveTo(clicker_help.control_groups[0][0], clicker_help.control_groups[0][1], duration=0.0, _pause=False)
                pyautogui.click(clicks=3)
                time.sleep(0.1)

                if info.idle_workers > 0:
                    pyautogui.moveTo(clicker_help.idle_workers[0], clicker_help.idle_workers[1], duration=0.0, _pause=False)
                    pyautogui.click()
                else:
                    pyautogui.moveTo(clicker_help.control_groups[1][0], clicker_help.control_groups[1][1], duration=0.0, _pause=False)
                    pyautogui.click()
                time.sleep(0.1)

                mineral_info = UI_processor(get_mineral=True)
                
                if build_order[0] == "supply depot":
                    pyautogui.moveTo(clicker_help.right_window[2][0][0], clicker_help.right_window[2][0][1], duration=0.0, _pause=False)
                    pyautogui.click()
                    time.sleep(0.1)
                    pyautogui.moveTo(clicker_help.right_window[0][2][0], clicker_help.right_window[0][2][1], duration=0.0, _pause=False)
                    pyautogui.click()
                else:
                    pyautogui.moveTo(clicker_help.right_window[2][0][0], clicker_help.right_window[2][0][1], duration=0.0, _pause=False)
                    pyautogui.click()
                    time.sleep(0.1)
                    pyautogui.moveTo(clicker_help.right_window[1][0][0], clicker_help.right_window[1][0][1], duration=0.0, _pause=False)
                    pyautogui.click()
                time.sleep(0.1)

                pyautogui.moveTo(i, j, duration=0.0, _pause=False)
                pyautogui.click()
                time.sleep(0.2)

                new_info = UI_processor(get_mineral=True)

                if new_info.minerals < mineral_info.minerals: # success
                    breaking = True
                    x = j
                    if build_order[0] == "barracks":
                        barracks_pos.append((i, j))
                    if start_time == 0:
                        start_time = time.time()
                    print("built : " + build_order.pop(0))
                    break
            if breaking:
                break

for i in barracks_pos:
    # go back on command center view
    pyautogui.moveTo(clicker_help.control_groups[0][0], clicker_help.control_groups[0][1], duration=0.0, _pause=False)
    pyautogui.click(clicks=3)
    time.sleep(0.1)

    pyautogui.moveTo(i[0], i[1], duration=0.0, _pause=False)
    pyautogui.click()
    time.sleep(0.1)

    info = UI_processor(get_selected_single=True)

    if info.selected_single == "barracks":
        print("barracks found")
        time.sleep(1)
        pyautogui.moveTo(i[0], i[1], duration=0.0, _pause=False)
        pyautogui.click()
        time.sleep(0.1)
        pyautogui.click()
        time.sleep(0.1)
        pyautogui.keyDown("shift")
        pyautogui.press("3")
        pyautogui.keyUp("shift")
        break

# build order is done, now build only marines + supply and attack
start_time = 0
while not keyboard.is_pressed("esc"):

    info = UI_processor(get_supply=True, get_mineral=True, get_army_units=True)
    
    # if supply is not sufficient, build more depots
    if info.supply_right - info.supply_left <= 4 and (time.time() - start_time) > (units_dictionaries.buildings["supply depot"][2] + 3):
        
        depot_info = UI_processor(get_mineral=True, get_idle_workers=True)
        while depot_info.minerals < 100:
            depot_info = UI_processor(get_mineral=True, get_idle_workers=True)

        for j in range(x + 200, 800, 200):
            breaking = False
            for i in range(300, 1610, 200):
                # go back on command center view
                pyautogui.moveTo(clicker_help.control_groups[0][0], clicker_help.control_groups[0][1], duration=0.0, _pause=False)
                pyautogui.click(clicks=3)
                time.sleep(0.1)

                if depot_info.idle_workers > 0:
                    pyautogui.moveTo(clicker_help.idle_workers[0], clicker_help.idle_workers[1], duration=0.0, _pause=False)
                    pyautogui.click()
                else:
                    pyautogui.moveTo(clicker_help.control_groups[1][0], clicker_help.control_groups[1][1], duration=0.0, _pause=False)
                    pyautogui.click()
                time.sleep(0.1)

                depot_info = UI_processor(get_mineral=True)
                
                pyautogui.moveTo(clicker_help.right_window[2][0][0], clicker_help.right_window[2][0][1], duration=0.0, _pause=False)
                pyautogui.click()
                time.sleep(0.1)
                pyautogui.moveTo(clicker_help.right_window[0][2][0], clicker_help.right_window[0][2][1], duration=0.0, _pause=False)
                pyautogui.click()
                time.sleep(0.1)

                pyautogui.moveTo(i, j, duration=0.0, _pause=False)
                pyautogui.click()
                time.sleep(0.2)

                new_info = UI_processor(get_mineral=True)

                if new_info.minerals < depot_info.minerals: # success
                    breaking = True
                    x = j
                    break
            if breaking:
                break
        start_time = time.time()

    elif info.minerals >= 50:
        # select barracks
        pyautogui.moveTo(clicker_help.control_groups[2][0], clicker_help.control_groups[2][1], duration=0.0, _pause=False)
        pyautogui.click()
        time.sleep(0.1)
        # build marine
        pyautogui.moveTo(clicker_help.right_window[0][0][0], clicker_help.right_window[0][0][1], duration=0.0, _pause=False)
        pyautogui.click()
        
    time.sleep(0.1)
    
    if info.army_units > 12:
        # rally point in enemy base
        pyautogui.moveTo(25 + startup_info.enemy_starting_base[0], 808 + startup_info.enemy_starting_base[1], duration=0.0, _pause=False)
        pyautogui.click(button='right')
        time.sleep(0.1)
        pyautogui.moveTo(clicker_help.army[0], clicker_help.army[1], duration=0.0, _pause=False)
        pyautogui.click()
        time.sleep(0.1)
        pyautogui.press("T") # i have a french keyboard and we use T move, not A move :3
        pyautogui.moveTo(25 + startup_info.enemy_starting_base[0], 808 + startup_info.enemy_starting_base[1], duration=0.0, _pause=False)
        pyautogui.click()
        time.sleep(0.1)

        while UI_processor(get_idle_workers=True).idle_workers > 0:
            pyautogui.moveTo(clicker_help.idle_workers[0], clicker_help.idle_workers[1], duration=0.0, _pause=False)
            pyautogui.click()
            time.sleep(0.1)
            pyautogui.press("T") # i have a french keyboard and we use T move, not A move :3
            pyautogui.moveTo(25 + startup_info.enemy_starting_base[0], 808 + startup_info.enemy_starting_base[1], duration=0.0, _pause=False)
            pyautogui.click()
            time.sleep(0.1)

        time.sleep(0.3)

print("end")
