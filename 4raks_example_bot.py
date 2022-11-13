import time
from UI_processor import UI_processor
from camera_view_processor import cam_processor
from clicker_helper import clicker_helper as clicker_help
from hotkey_helper import hotkey_helper as hotkey_help
import pyautogui
import numpy as np
import cv2
import pathlib
import mss
import units_dictionaries
import keyboard
import random


print("Waiting for the game to start")
clicker = clicker_help() # usefull abstraction for clicking icons and elements
hotkey = hotkey_help()   # usefull for pressing keys


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

# this goes to a random base, it is mainly used by zerg player to inject by here we need to to center the command center
pyautogui.press(hotkey.go_to_random_base)

# command center in control group 1
pyautogui.moveTo(1920/2, 400, duration=0.0, _pause=False)
pyautogui.click()
time.sleep(0.1)
hotkey.put_selected_in_group(1)
time.sleep(0.1)

# workers in control group 2
pyautogui.moveTo(100, 100, duration=0.0, _pause=True)
pyautogui.dragTo(1500, 800, button='left')
time.sleep(0.1)
hotkey.put_selected_in_group(2)
time.sleep(0.1)

startup_info = UI_processor(get_minimap_init_values=True)

x = 100
y = 300

# https://www.youtube.com/watch?v=X8aAAenFkrU&t=274s we can keep going but for now only print marines, when reaching the end of the array we keep making supply depots and marines
build_order = ["scv", "supplydepot", "scv", "scv", "barracks", "barracks", "barracks", "barracks", "scv", "supplydepot"]
barracks_pos = [] # save this to put them later in a control group
start_time = 0
while not keyboard.is_pressed("esc"):

    if len(build_order) == 0:
        break
    
    time.sleep(0.4)
    info = UI_processor(get_mineral=True, get_idle_workers=True)
    
    object = None
    if build_order[0] in units_dictionaries.buildings:
        object = units_dictionaries.buildings[build_order[0]]
    else:
        object = units_dictionaries.units[build_order[0]]
    
    if info.minerals < object[0]:
        continue
    
    #cv2.putText(info.image, str(info.minerals), (100, 100), cv2.FONT_HERSHEY_SIMPLEX, 5, (0, 255, 0), 3)
    #cv2.imwrite(str(pathlib.Path(__file__).parent.absolute()) + "\\debug\\mineral" + str(random.random()) + ".png", info.image)

    if build_order[0] == "scv":
        clicker.select_group(0)
        time.sleep(0.1)
        pyautogui.press(hotkey.build_scv)
        print("built : " + build_order.pop(0))
        continue

    if info.idle_workers > 0:
        pyautogui.press(hotkey.select_idle_workers)
    else:
        clicker.select_group(1)
    time.sleep(0.1)     
    pyautogui.press(hotkey.scv_build_structure)
    time.sleep(0.3)
    info = UI_processor(get_idle_workers=True, get_right_window_buttons_availability=True)

    if (build_order[0] == "supplydepot" and info.right_window_button_available[0][2]) or (build_order[0] == "barracks" and info.right_window_button_available[1][0]):
        for j in range(x, 800, 200):
            breaking = False
            for i in range(y, 1610, 200):
                # go back on command center view
                pyautogui.moveTo(25 + startup_info.our_starting_base[0], 808 + startup_info.our_starting_base[1], duration=0.0, _pause=False)
                time.sleep(0.1)

                if info.idle_workers > 0:
                    pyautogui.press(hotkey.select_idle_workers)
                else:
                    clicker.select_group(1)
                time.sleep(0.1)
                
                pyautogui.press(hotkey.scv_build_structure)
                time.sleep(0.1)
                if build_order[0] == "supplydepot":
                    pyautogui.press(hotkey.scv_build_depot)
                else:
                    pyautogui.press(hotkey.scv_build_barracks)
                time.sleep(0.2)

                pyautogui.moveTo(i, j, duration=0.0, _pause=False)
                time.sleep(0.4)

                building_authorized = cam_processor(get_building_authorization=True).building_authorized
                if building_authorized: # success
                    pyautogui.click()
                    breaking = True
                    x = j
                    y = i + 200
                    if build_order[0] == "barracks":
                        barracks_pos.append((i, j))
                    if start_time == 0:
                        start_time = time.time()
                    print("built : " + build_order.pop(0))
                    break
            
            if breaking:
                break
            y = 300

for i in barracks_pos:
    # go back on command center view
    pyautogui.moveTo(25 + startup_info.our_starting_base[0], 808 + startup_info.our_starting_base[1], duration=0.0, _pause=False)
    pyautogui.click()
    time.sleep(0.05)

    pyautogui.moveTo(i[0], i[1], duration=0.0, _pause=False)
    pyautogui.click()
    time.sleep(0.05)

    info = UI_processor(get_selected_single=True)

    if info.selected_single == "barracks":
        print("barracks found")
        time.sleep(1)
        pyautogui.moveTo(i[0], i[1], duration=0.0, _pause=False)
        pyautogui.click()
        time.sleep(0.05)
        pyautogui.click()
        time.sleep(0.05)
        hotkey.put_selected_in_group(3)

        # go back on command center view
        pyautogui.moveTo(25 + startup_info.our_starting_base[0], 808 + startup_info.our_starting_base[1], duration=0.0, _pause=False)
        pyautogui.click()
        time.sleep(0.05)
        # select barracks
        clicker.select_group(2)
        time.sleep(0.05)
        # rally on one barrack
        pyautogui.moveTo(i[0], i[1], duration=0.0, _pause=False)
        pyautogui.click(button='right')
        time.sleep(0.05)
        break

# build order is done, now build only marines + supply and attack
start_time = 0
rallied = False
while not keyboard.is_pressed("esc"):

    time.sleep(0.4)
    info = UI_processor(get_supply=True, get_mineral=True, get_army_units=True)
    
    # if supply is not sufficient, build more depots
    if ((info.supply_right - info.supply_left) <= 4) and (time.time() - start_time) > (units_dictionaries.buildings["supplydepot"][2] + 3):
        
        depot_info = UI_processor(get_mineral=True, get_idle_workers=True)
        while depot_info.minerals < 100:
            depot_info = UI_processor(get_mineral=True, get_idle_workers=True)

        for j in range(x, 800, 200):
            breaking = False
            for i in range(y, 1610, 200):
                # go back on command center view
                pyautogui.moveTo(25 + startup_info.our_starting_base[0], 808 + startup_info.our_starting_base[1], duration=0.0, _pause=False)
                time.sleep(0.1)

                if depot_info.idle_workers > 0:
                    pyautogui.press(hotkey.select_idle_workers)
                else:
                    clicker.select_group(1)
                time.sleep(0.1)

                pyautogui.press(hotkey.scv_build_structure)
                time.sleep(0.1)
                pyautogui.press(hotkey.scv_build_depot)
                time.sleep(0.2)

                pyautogui.moveTo(i, j, duration=0.0, _pause=False)
                time.sleep(0.4)

                building_authorized = cam_processor(get_building_authorization=True).building_authorized
                if building_authorized: # success
                    pyautogui.click()
                    breaking = True
                    x = j
                    y = i + 200
                    break
            
            if breaking:
                break
            y = 300
        start_time = time.time()

    elif info.minerals >= 50:
        # select barracks
        clicker.select_group(2)
        time.sleep(0.05)
        # build marine
        pyautogui.press(hotkey.barracks_build_marine)
        
    time.sleep(0.05)
    
    if info.army_units >= 12 or rallied:
        if not rallied:
            # rally point in enemy base
            pyautogui.moveTo(25 + startup_info.enemy_starting_base[0], 808 + startup_info.enemy_starting_base[1], duration=0.0, _pause=False)
            pyautogui.click(button='right')
            time.sleep(0.05)
            rallied = True
        pyautogui.press(hotkey.select_army)
        time.sleep(0.05)
        pyautogui.press(hotkey.attack_command)
        pyautogui.moveTo(25 + startup_info.enemy_starting_base[0], 808 + startup_info.enemy_starting_base[1], duration=0.0, _pause=False)
        pyautogui.click()
        time.sleep(0.05)

        while UI_processor(get_idle_workers=True).idle_workers > 0:
            pyautogui.press(hotkey.select_idle_workers)
            time.sleep(0.05)
            pyautogui.press(hotkey.attack_command)
            pyautogui.moveTo(25 + startup_info.enemy_starting_base[0], 808 + startup_info.enemy_starting_base[1], duration=0.0, _pause=False)
            pyautogui.click()
            time.sleep(0.05)

        time.sleep(1)

print("end")
