import time
import screenshot_maker
import pyautogui

# run this script then you have 4 seconds to get in a 1v1 ongoing match. It will print info and walk through the ressource patches

time.sleep(4)

start_time = time.time()
screen_infos = screenshot_maker.screen_info(True)
print("%s sec" % (time.time() - start_time))

'''
start_time = time.time()
for i in screen_infos.base_locations:
    pyautogui.moveTo(25 + i[0], 808 + i[1], duration=0.0, _pause=False)
    pyautogui.click()
print("%s sec" % (time.time() - start_time))
'''
