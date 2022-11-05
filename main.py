import time
import screenshot_maker
import minimap_segmenter
import pyautogui

# run this script then you have 4 seconds to get in a 1v1 ongoing match. It will print info and walk through the ressource patches

time.sleep(4)

start_time = time.time()
screen_infos = screenshot_maker.screen_info(True)
print("%s sec" % (time.time() - start_time))

map_info = minimap_segmenter.minimap_info(screen_infos.minimap, True)

start_time = time.time()
for i in map_info.base_locations:
    pyautogui.moveTo(25 + i[0], 808 + i[1])
    pyautogui.click()
print("%s sec" % (time.time() - start_time))
