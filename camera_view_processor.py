import cv2
import numpy as np
import pathlib
import copy
from threading import Thread
import mss
import UI_processor
import random


current_dir = str(pathlib.Path(__file__).parent.absolute()) + "\\camera_view_processor_debug\\"


# multithreaded functions -------------------------------------------------------------------------------

def mineral_patches_handle(img, patches, debug = False):
    left = np.array([95, 32, 14])
    right = np.array([255, 110, 68])
    color_patch = cv2.inRange(img, left, right)
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    hsv = hsv[:, :, 1]
    hsv = cv2.inRange(hsv, 200, 255)
    patch = cv2.bitwise_and(hsv, color_patch)
    kernel = np.ones((13, 13), np.uint8)
    patch = cv2.dilate(patch, kernel)
    if debug:
        cv2.imwrite(current_dir + "mineral_patches_bitwise_and.png", patch)
        cv2.imwrite(current_dir + "mineral_patches_hsv.png", hsv)
        cv2.imwrite(current_dir + "mineral_patches_color.png", color_patch)
    kernel = np.ones((21, 21), np.uint8)
    patch = cv2.erode(patch, kernel)
    if debug:
        cv2.imwrite(current_dir + "mineral_patches_erode.png", patch)

    nb, _, stats, centroids = cv2.connectedComponentsWithStats(patch, 4, cv2.CV_32S)
    res = []
    for i in range(1, nb):
        if stats[i][cv2.CC_STAT_AREA] < 50: # too small to be a mineral patch
            continue
        res.append((int(centroids[i][0]), int(centroids[i][1])))
    patches[0] = res

def geysers_handle(img, geysers, debug = False):
    # THIS DOES NOT WORK, TOO MUCH FALSE POSITIVE
    left = np.array([50, 255, 90])
    right = np.array([200, 255, 255])
    patch = cv2.inRange(img, left, right)
    #kernel = np.ones((5, 5), np.uint8)
    #patch = cv2.erode(patch, kernel)
    #kernel = np.ones((13, 13), np.uint8)
    #patch = cv2.dilate(patch, kernel)
    if debug:
        cv2.imwrite(current_dir + "geysers.png", patch)

def building_authorization_handle(img, authorized, debug = False):
    left = np.array([5, 5, 145])
    right = np.array([50, 50, 220])
    building = cv2.inRange(img, left, right)
    kernel = np.ones((11, 11), np.uint8)
    building = cv2.dilate(building, kernel)
    if debug:
        cv2.imwrite(current_dir + "building_authorization.png", building)

    refusal_template = cv2.imread(str(pathlib.Path(__file__).parent.absolute()) + "\\templates\\building_authorization\\refusal_pattern.png", cv2.IMREAD_GRAYSCALE)
    res = cv2.matchTemplate(building, refusal_template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, _ = cv2.minMaxLoc(res)
    if max_val > 0.3:
        authorized[0] = False
    else:
        authorized[0] = True

# multithreaded functions -------------------------------------------------------------------------------


class cam_processor:
    # setting [None]*1 in order to pass as pointers in threads
    mineral_patches = [None]*1    # list of tuples (int, int)
    geysers = [None]*1            # list of tuples (int, int) /!\ this does not work and cannot be infered using basic image processing techniques like using colors and contrasts.
    building_authorized = [None]*1 # bool


    def __init__(self,
    debug = False,
    cam_view=None,
    get_mineral_patches = False,
    get_geysers = False,
    get_building_authorization = False):

        if debug:
            get_mineral_patches = True
            get_geysers = True
            get_building_authorization = True

        if cam_view is None:
            cam_view = UI_processor.UI_processor(get_game_image=True).game
        
        threads = [None, None, None]
        if get_mineral_patches:
            threads[0] = Thread(target=mineral_patches_handle, args=(cam_view, self.mineral_patches, debug))
        if get_geysers:
            threads[1] = Thread(target=geysers_handle, args=(cam_view, self.geysers, debug))
        if get_building_authorization:
            threads[2] = Thread(target=building_authorization_handle, args=(cam_view, self.building_authorized, debug))
        
        # running threads
        for i in threads:
            if i is not None:
                i.start()
        
        # joining threads
        for i in threads:
            if i is not None:
                i.join()
        
        self.mineral_patches = self.mineral_patches[0]
        self.geysers = self.geysers[0]
        self.building_authorized = self.building_authorized[0]
        
        if debug:
            print("Mineral patches :             " + str(self.mineral_patches))
            print("Geysers :                     " + str(self.geysers))
            print("Building authorized :         " + str(self.building_authorized))
