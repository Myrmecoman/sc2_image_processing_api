from sc2 import maps
from sc2.player import Bot, Computer
from sc2.main import run_game
from sc2.data import Race, Difficulty
from sc2.bot_ai import BotAI
from skimage.io import imsave
import numpy as np
import pathlib
import cv2


current_dir = str(pathlib.Path(__file__).parent.absolute()) + ""


class WorkerRushBot(BotAI):
    async def on_step(self, iteration: int):

        if iteration == 0:
            for worker in self.workers:
                worker.attack(self.enemy_start_locations[0])
                
        if iteration % 10 == 0:
            self.client._renderer._minimap_image.save(current_dir + "\\temp.bmp")
            npminimap = cv2.imread(current_dir + "\\temp.bmp")
            npminimap = cv2.cvtColor(npminimap, cv2.COLOR_BGR2RGB)
            npminimap = cv2.imwrite(current_dir + "\\cv.bmp", npminimap)


run_game(
    maps.get("AcropolisLE"),
    [Bot(Race.Terran, WorkerRushBot()), Computer(Race.Random, Difficulty.Easy)],
    realtime=False,
    rgb_render_config={'window_size': (1280, 720), 'minimap_size': (256, 256)}
)
