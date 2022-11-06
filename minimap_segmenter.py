import cv2
import numpy as np
import pathlib
import copy


current_dir = str(pathlib.Path(__file__).parent.absolute()) + "\\output\\minimap_segmenter\\"


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

        # finding approximate base locations
        kernel = np.ones((7, 7), np.uint8)
        locations = copy.deepcopy(self.resources_mask)
        locations = cv2.dilate(locations, kernel)
        num_labels, labels_ids, values, centroids = cv2.connectedComponentsWithStats(locations, 4)
        for i in range(1, num_labels):
            if values[i][-1] < 200 : # components with small areas are very probably small minerals patches blocking passages
                continue
            self.base_locations.append([int(centroids[i][0]), int(centroids[i][1])])
            locations[int(centroids[i][1])][int(centroids[i][0])] = 100

        if debug:
            cv2.imwrite(current_dir + "ressources.png", self.resources_mask)
            cv2.imwrite(current_dir + "allies.png", self.allies_mask)
            cv2.imwrite(current_dir + "enemies.png", self.enemies_mask)
            cv2.imwrite(current_dir + "locations.png", locations)
