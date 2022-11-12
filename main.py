import time
from UI_processor import UI_processor
from camera_view_processor import cam_processor
import pyautogui


# run this script then you have 4 seconds to get in a 1v1 ongoing match. It will print info and walk through the ressource patches


time.sleep(4)

start_time = time.time()
infos = UI_processor(debug=True)
print("%s sec" % (time.time() - start_time))

print()

start_time = time.time()
cam_info = cam_processor(debug=True)
print("%s sec" % (time.time() - start_time))


'''
# this clicks on every detected mineral patch
for i in cam_info.mineral_patches:
    pyautogui.moveTo(i[0], i[1], duration=0.0, _pause=False)
    pyautogui.click()
    time.sleep(2)
'''
'''
# this clicks on every eventual base locations
for i in infos.base_locations:
    # (25, 808) is the minimap starting coordinates
    pyautogui.moveTo(25 + i[0], 808 + i[1], duration=0.0, _pause=False)
    pyautogui.click()
'''
