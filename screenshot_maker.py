import pyautogui
import cv2
import numpy as np
import time
import pathlib
import copy
import pytesseract


def prepare_for_ocr(img):
    img = 255-cv2.threshold(img, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    img = cv2.resize(img, (img.shape[1] * 3, img.shape[0] * 3))
    return img


def screenshot_and_crop():
    # screenshoting
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    
    supply = cv2.cvtColor(image[20:36, 1803:1907], cv2.COLOR_BGR2GRAY)
    supply = prepare_for_ocr(supply)
    gas = cv2.cvtColor(image[20:36, 1678:1752], cv2.COLOR_BGR2GRAY)
    gas = prepare_for_ocr(gas)
    mineral = cv2.cvtColor(image[20:36, 1559:1634], cv2.COLOR_BGR2GRAY)
    mineral = prepare_for_ocr(mineral)
    idle_workers = cv2.cvtColor(image[749:764, 48:77], cv2.COLOR_BGR2GRAY)
    idle_workers = prepare_for_ocr(idle_workers)
    army_supply = cv2.cvtColor(image[749:763, 128:155], cv2.COLOR_BGR2GRAY)
    army_supply = prepare_for_ocr(army_supply)
    timer = cv2.cvtColor(image[779:798, 269:343], cv2.COLOR_BGR2GRAY)
    timer = prepare_for_ocr(timer)
    minimap = image[808:1065, 25:291]
    building = image[850:1061, 1536:1896]
    selected_single = image[895:915, 820:1070]
    selected_group = image[887:1058, 661:1121]
    game = copy.deepcopy(image[:864, :])
    game[:41, 1530:] = 0
    game[783:, 1518:] = 0
    game[745:, :359] = 0
    return minimap, supply, gas, mineral, idle_workers, army_supply, building, timer, selected_single, selected_group, game


def img_to_text(img):
    custom_config = r'--oem 3 --psm 7'
    pytesseract.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    word = pytesseract.image_to_string(img, output_type=pytesseract.Output.DICT, config=custom_config, lang="eng")
    word = word['text']
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
    print(word)


print("starting")
current_dir = str(pathlib.Path(__file__).parent.absolute())
time.sleep(4)
start_time = time.time()

minimap, supply, gas, mineral, idle_workers, army_supply, building, timer, selected_single, selected_group, game = screenshot_and_crop()

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

print("done")
