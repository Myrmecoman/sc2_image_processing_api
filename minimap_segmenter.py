import cv2
import numpy as np
import pathlib


current_dir = str(pathlib.Path(__file__).parent.absolute())


class minimap_info:

    base_locations = []
    resources_mask = []
    allies_mask = []
    enemies_mask = []

    def __init__(self, minimap, debug = False):

        # getting resources
        color = np.array([241, 191, 126])
        self.resources_mask = cv2.inRange(minimap, color, color)
        
        # getting allies
        left = np.array([0, 140, 0])
        right = np.array([0, 255, 0])
        self.allies_mask = cv2.inRange(minimap, left, right)

        # getting enemies
        left = np.array([0, 0, 190])
        right = np.array([0, 0, 255])
        self.enemies_mask = cv2.inRange(minimap, left, right)

        if debug:
            cv2.imwrite(current_dir + "\\images\\minimap_seg\\ressources.png", self.resources_mask)
            cv2.imwrite(current_dir + "\\images\\minimap_seg\\allies.png", self.allies_mask)
            cv2.imwrite(current_dir + "\\images\\minimap_seg\\enemies.png", self.enemies_mask)
