import pyautogui
import cv2
import numpy as np
import time
import pathlib
import copy
import pytesseract


def screenshot_and_crop():
    # screenshoting
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    minimap = image[808:1065, 25:291]
    supply = cv2.cvtColor(image[20:36, 1803:1907], cv2.COLOR_BGR2GRAY)
    supply = 255-cv2.threshold(supply, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    gas = cv2.cvtColor(image[20:36, 1678:1752], cv2.COLOR_BGR2GRAY)
    gas = 255-cv2.threshold(gas, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    mineral = cv2.cvtColor(image[20:36, 1559:1634], cv2.COLOR_BGR2GRAY)
    mineral = 255-cv2.threshold(mineral, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    idle_workers = cv2.cvtColor(image[749:764, 48:77], cv2.COLOR_BGR2GRAY)
    idle_workers = 255-cv2.threshold(idle_workers, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    army_supply = cv2.cvtColor(image[749:763, 128:155], cv2.COLOR_BGR2GRAY)
    army_supply = 255-cv2.threshold(army_supply, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    timer = cv2.cvtColor(image[779:798, 269:343], cv2.COLOR_BGR2GRAY)
    timer = 255-cv2.threshold(timer, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    building = image[850:1061, 1536:1896]
    selected_single = image[895:915, 820:1070]
    selected_group = image[887:1058, 661:1121]
    game = copy.deepcopy(image[:864, :])
    game[:41, 1530:] = 0
    game[783:, 1518:] = 0
    game[745:, :359] = 0
    return minimap, supply, gas, mineral, idle_workers, army_supply, building, timer, selected_single, selected_group, game


def img_to_text(img):
    custom_config = r'--oem 3 --psm 6'
    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    details = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT, config=custom_config, lang="eng")
    word = ""
    for s_word in details["text"]:
        if s_word != '':
            print(s_word)


print("starting")
current_dir = str(pathlib.Path(__file__).parent.absolute())
time.sleep(4)

start_time = time.time()
minimap, supply, gas, mineral, idle_workers, army_supply, building, timer, selected_single, selected_group, game = screenshot_and_crop()
print("%s sec" % (time.time() - start_time))

cv2.imwrite(current_dir + "\\images\\minimap.png", minimap)
cv2.imwrite(current_dir + "\\images\\supply.png", supply)
cv2.imwrite(current_dir + "\\images\\gas.png", gas)
cv2.imwrite(current_dir + "\\images\\mineral.png", mineral)
cv2.imwrite(current_dir + "\\images\\idle_workers.png", idle_workers)
cv2.imwrite(current_dir + "\\images\\army_supply.png", army_supply)
cv2.imwrite(current_dir + "\\images\\building.png", building)
cv2.imwrite(current_dir + "\\images\\timer.png", timer)
cv2.imwrite(current_dir + "\\images\\selected_single.png", selected_single)
cv2.imwrite(current_dir + "\\images\\selected_group.png", selected_group)
cv2.imwrite(current_dir + "\\images\\game.png", game)

print("supply :")
img_to_text(supply)
print("gas :")
img_to_text(gas)
print("mineral :")
img_to_text(mineral)
print("idle_workers :")
img_to_text(idle_workers)
print("army_supply :")
img_to_text(army_supply)
print("timer :")
img_to_text(timer)

print("done")
