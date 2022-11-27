from sc2 import maps
from sc2.player import Bot, Computer
from sc2.main import run_game
from sc2.data import Race, Difficulty
from sc2.bot_ai import BotAI
import numpy as np
import pathlib
import cv2
import time
import random
from sc2.ids.unit_typeid import UnitTypeId
from sc2.unit import Unit
from sc2.units import Units
import asyncio


map_names = ["AcropolisLE", "DiscoBloodbathLE", "EphemeronLE", "ThunderbirdLE", "TritonLE", "WintersGateLE", "WorldofSleepersLE"]
current_dir = str(pathlib.Path(__file__).parent.absolute()) + ""
state = [12, 15, 0, 50, 0, 125, 0] # supply, supply max, army_count, mineral, gas, map value, is enemy close ?
timer = -1
total_timer = time.time()
last_reward = -1


class BasicBot(BotAI):


    async def act(self, action):
        ccs: Units = self.townhalls
        cc: Unit = ccs.random

        if action == 0: # do nothing
            return
        elif action == 1: # attack
            army = self.units.filter(lambda unit: unit.can_attack_air or unit.type_id == UnitTypeId.MEDIVAC)
            for unit in army:
                unit.attack(self.enemy_start_locations[0])
        elif action == 2: # defend
            army = self.units.filter(lambda unit: unit.can_attack_air or unit.type_id == UnitTypeId.MEDIVAC)
            for unit in army:
                unit.attack(self.start_location)
        elif action == 3: # retreat
            army = self.units.filter(lambda unit: unit.can_attack_air or unit.type_id == UnitTypeId.MEDIVAC)
            for unit in army:
                unit.move(self.start_location)
        elif action == 4: # make scv
            if self.can_afford(UnitTypeId.SCV):
                cc.train(UnitTypeId.SCV)
        elif action == 5: # make marine
            for barrack in self.structures(UnitTypeId.BARRACKS).idle:
                barrack.train(UnitTypeId.MARINE)
                break
        elif action == 6: # make medivac
            for starport in self.structures(UnitTypeId.STARPORT).idle:
                starport.train(UnitTypeId.MEDIVAC)
                break
        elif action == 7: # build depot
            if self.can_afford(UnitTypeId.SUPPLYDEPOT):
                await self.build(UnitTypeId.SUPPLYDEPOT, near=cc.position.towards(self.game_info.map_center, 8))
        elif action == 8: # build barracks
            if self.can_afford(UnitTypeId.BARRACKS):
                await self.build(UnitTypeId.BARRACKS, near=cc.position.towards(self.game_info.map_center, 8))
        elif action == 9: # build factory
            if self.can_afford(UnitTypeId.FACTORY):
                await self.build(UnitTypeId.FACTORY, near=cc.position.towards(self.game_info.map_center, 8))
        elif action == 10: # build starport
            if self.can_afford(UnitTypeId.STARPORT):
                await self.build(UnitTypeId.STARPORT, near=cc.position.towards(self.game_info.map_center, 8))
        elif action == 11: # build base
            return
        elif action == 12: # build gas
            if self.can_afford(UnitTypeId.REFINERY):
                vgs: Units = self.vespene_geyser.closer_than(20, cc)
                for vg in vgs:
                    if self.gas_buildings.filter(lambda unit: unit.distance_to(vg) < 1):
                        break
                    worker: Unit = self.select_build_worker(vg.position)
                    if worker is None:
                        break
                    worker.build_gas(vg)
                    break


    def dist_enemies(self):
        # getting allies
        left = np.array([0, 140, 0])
        right = np.array([0, 255, 0])
        allies_dilated = cv2.inRange(self.minimap, left, right)
        # getting enemies
        left = np.array([130, 0, 0])
        right = np.array([255, 0, 0])
        enemies_dilated = cv2.inRange(self.minimap, left, right)
        # dilating
        kernel = np.ones((7, 7), np.uint8)
        allies_dilated = cv2.dilate(allies_dilated, kernel)
        enemies_dilated = cv2.dilate(enemies_dilated, kernel)
        # getting connected components
        nb_allies, _, _, centroids_allies = cv2.connectedComponentsWithStats(allies_dilated, 4, cv2.CV_32S)
        nb_enemies, _, _, centroids_enemies = cv2.connectedComponentsWithStats(enemies_dilated, 4, cv2.CV_32S)
        if nb_enemies != 0:
            min_dist = 100000
            for x in range(1, nb_allies):
                i = centroids_allies[x]
                for y in range(1, nb_enemies):
                    j = centroids_enemies[y]
                    dist = (i[0] - j[0]) * (i[0] - j[0]) + (i[1] - j[1]) * (i[1] - j[1])
                    if dist < min_dist:
                        min_dist = dist
            return min_dist
        return 100000


    def get_green_pixels(self):
        left = np.array([0, 130, 0])
        right = np.array([0, 255, 0])
        green = cv2.inRange(self.minimap, left, right)
        return np.sum(green == 255)


    def get_reward(self): # reward goes from 0 to 200
        #white_pixels = min(self.get_green_pixels(), 1000) // 5
        return self.supply_used# + white_pixels


    def get_state(self):
        global state

        attacked = 0
        if self.dist_enemies() < 400:
            attacked = 1
        state = [self.supply_used, self.supply_cap, self.army_count, self.minerals, self.vespene, 125, attacked]


    def reset_state(self):
        global state
        global last_reward

        last_reward = -1
        state = [self.supply_used, self.supply_cap, self.army_count, self.minerals, self.vespene, 125, 0]


    def step_sync(self):
        global state
        global last_reward

        self.get_state()
        reward = self.get_reward()
        if last_reward == -1:
            last_reward = reward
            return state, -1, False

        diff = (reward - last_reward) * 10 # -1 so that if nothing happens, we keep losing rewards
        if diff == 0:
            diff = -1
        if diff > 0:
            diff *= 5
        last_reward = reward
        return state, diff, (self.supply_used == 0)
    

    async def step(self, action):
        await self.act(action)
        return self.step_sync()


    async def on_step(self, iteration: int):
        global timer

        if iteration == 0:
            self.reset_state()

        if self.supply_left < 6 and not self.already_pending(UnitTypeId.SUPPLYDEPOT):
            await self.act(7)
        if self.structures(UnitTypeId.BARRACKS).amount < 4:
            await self.act(8)
        if self.army_count > 15:
            await self.act(1)
        else:
            await self.act(3)

        if self.time - timer >= 1: # update every in game second

            timer = self.time
            self.client._renderer._minimap_image.save(current_dir + "\\temp.bmp")
            self.minimap = cv2.imread(current_dir + "\\temp.bmp")
            state, step_score, done = await self.step(5)
            print(step_score)
            
            # leaving if we have no more supply
            if self.supply_used == 0:
                await self.client.leave()
                return


run_game(maps.get(map_names[random.randint(0, len(map_names) - 1)]),
        [Bot(Race.Terran, BasicBot()), Computer(Race.Random, Difficulty.Medium)], # VeryHard
        realtime=False,
        rgb_render_config={'window_size': (1280, 720), 'minimap_size': (256, 256)})

print("Total time : " + str(time.time() - total_timer))
