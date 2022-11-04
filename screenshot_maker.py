import pyautogui
import cv2
import numpy as np
import time
import os

def screenshot_and_crop():
    # screenshoting
    image = pyautogui.screenshot()
    image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    minimap = image[800:1080, 1820:1920]

def find_base_camera_locations(minimap):
    print("TODO")

