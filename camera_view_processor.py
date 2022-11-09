import cv2
import numpy as np
import pathlib
import copy
from threading import Thread
import mss
import UI_processor


current_dir = str(pathlib.Path(__file__).parent.absolute()) + "\\camera_view_processor_debug\\"


class cam_processor:

    mineral_patches = [None]*1 # list of tuples (int, int)

    def __init__(self, cam_view=None):
        if cam_view is None:
            cam_view = UI_processor.UI_processor(get_game_image=True).game
        return