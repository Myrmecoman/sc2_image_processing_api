import pyautogui
import cv2
import numpy as np


# provides clicking locations
class clicker_helper:

    right_window = [ # if you want to click instead of using hotkeys
        [(1575, 880), (1640, 880), (1713, 880), (1780, 880), (1853, 880)],
        [(1575, 950), (1640, 950), (1713, 950), (1780, 950), (1853, 950)],
        [(1575, 1020), (1640, 1020), (1713, 1020), (1780, 1020), (1853, 1020)]
    ]
    middle_window = [ # might be useful for removing units from selected group
        [(690, 920), (746, 920), (805, 920), (862, 920), (920, 920), (980, 920), (1035, 920), (1090, 920),],
        [(690, 975), (746, 975), (805, 975), (862, 975), (920, 975), (980, 975), (1035, 975), (1090, 975),],
        [(690, 1035), (746, 1035), (805, 1035), (862, 1035), (920, 1035), (980, 1035), (1035, 1035), (1090, 1035),]
    ]

    def __init__(self):
        return
