import cv2
import numpy as np
import pathlib
import copy
from threading import Thread
import mss
import UI_processor


current_dir = str(pathlib.Path(__file__).parent.absolute()) + "\\camera_view_processor_debug\\"


# multithreaded functions -------------------------------------------------------------------------------

def mineral_patches_handle(img, patches, debug = False):
    left = np.array([95, 32, 14])
    right = np.array([255, 103, 68])
    patch = cv2.inRange(img, left, right)
    kernel = np.ones((13, 13), np.uint8)
    patch = cv2.dilate(patch, kernel)
    if debug:
        cv2.imwrite(current_dir + "mineral_patches_dilate.png", patch)
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

# multithreaded functions -------------------------------------------------------------------------------


class cam_processor:
    # setting [None]*1 in order to pass as pointers in threads
    mineral_patches = [None]*1 # list of tuples (int, int)


    def __init__(self, debug = False, cam_view=None, get_mineral_patches = False):

        if debug:
            get_mineral_patches = True

        if cam_view is None:
            cam_view = UI_processor.UI_processor(get_game_image=True).game
        
        threads = [None]
        if get_mineral_patches:
            threads[0] = Thread(target=mineral_patches_handle, args=(cam_view, self.mineral_patches, debug))
        
        # running threads
        for i in threads:
            if i is not None:
                i.start()
        
        # joining threads
        for i in threads:
            if i is not None:
                i.join()
        
        self.mineral_patches = self.mineral_patches[0]
        
        if debug:
            print("Mineral patches : " + str(self.mineral_patches))