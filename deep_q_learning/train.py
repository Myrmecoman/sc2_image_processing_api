import torch
import torch.nn as nn
import numpy as np
import random
import torch.nn.functional as F 
import torch.optim as optim
from collections import namedtuple, deque
import numpy as np
import pathlib
import cv2
import time
import random
from threading import Thread
from sc2 import maps
from sc2.player import Bot, Computer
from sc2.main import run_game
from sc2.data import Race, Difficulty
from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId
from sc2.unit import Unit
from sc2.units import Units
# source for training : https://github.com/tawsifkamal/Deep-Q-Learning-CartPole-v0/blob/main/CartPoleDQL.py


map_names = ["AcropolisLE", "DiscoBloodbathLE", "EphemeronLE", "ThunderbirdLE", "TritonLE", "WintersGateLE", "WorldofSleepersLE"]
current_dir = str(pathlib.Path(__file__).parent.absolute())
lenstate = 7
nb_actions = 13
bot = [None]*1


class BasicBot(BotAI):
    def __init__(self):
        self.timer = -1
        self.last_reward = -1
        self.step_state = np.array([12, 15, 0, 50, 0, 125, 0])


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
        attacked = 0
        if self.dist_enemies() < 400:
            attacked = 1
        self.step_state = np.array([self.supply_used, self.supply_cap, self.army_count, self.minerals, self.vespene, 125, attacked])


    # leaving if we have no more supply
    async def kill_session(self):
        await self.client.leave()


    async def step(self, action):
        self.timer = self.time
        self.client._renderer._minimap_image.save(current_dir + "\\temp.bmp")
        self.minimap = cv2.imread(current_dir + "\\temp.bmp")

        await self.act(action)

        self.get_state()
        reward = self.get_reward()
        if self.last_reward == -1:
            self.last_reward = reward
            return self.step_state, -1, False
        diff = (reward - self.last_reward) * 10
        if diff == 0:
            diff = -1 # -1 so that if nothing happens, we keep losing rewards
        if diff > 0:
            diff *= 5
        self.last_reward = reward
        return self.step_state, diff, (self.supply_used == 0)


    async def on_step(self, iteration: int):
        return
            

class env:
    global bot
    def __init__(self):
        self.thread = None


    def launch_game(self):
        total_timer = time.time()
        run_game(maps.get(map_names[random.randint(0, len(map_names) - 1)]),
                [Bot(Race.Terran, bot[0]), Computer(Race.Random, Difficulty.VeryEasy)], # VeryHard, VeryEasy
                realtime=False,
                rgb_render_config={'window_size': (1280, 720), 'minimap_size': (256, 256)})
        print("Game time : " + str(time.time() - total_timer))


    def reset(self):
        if self.thread is not None:
            self.thread.join()
        if bot[0] is not None:
            bot[0].kill_session()
        bot[0] = BasicBot()
        self.thread = Thread(target=self.launch_game)
        self.thread.start()
        return np.array([12, 15, 0, 50, 0, 125, 0])


# training ----------------------------------------------------------------------------------------------------------------------------------------------------
# Defining the Neural Network 
class Network(nn.Module):
    def __init__(self, state_shape, action_shape):
        super().__init__()
        self.states = state_shape
        self.actions = action_shape

        # defining our layers
        self.fc1 = nn.Linear(in_features = self.states, out_features = 24)
        self.fc2 = nn.Linear(in_features = 24, out_features = 12)
        self.out = nn.Linear(in_features = 12, out_features = self.actions)

    
    # forward method 
    def forward(self, t): 
        t = F.relu(self.fc1(t))
        t = F.relu(self.fc2(t))
        t = self.out(t)
        return t 

# Defining the experience tuple 
Experience = namedtuple('Experience', ('state', 'action', 'reward', 'next_state', 'terminal'))


class Memory(object):
    def __init__(self, capacity):
        self.memory = deque(maxlen=capacity)
        self.capacity = capacity

    def push(self, state, next_state, action, reward, mask):
        self.memory.append(Experience(state, next_state, action, reward, mask))

    def sample(self, batch_size):
        experience = random.sample(self.memory, batch_size)
        batch = Experience(*zip(*experience))
        return batch

    def __len__(self):
        return len(self.memory)


def train_model(policy_net, target_net, optimizer, batch):
    # Extracting states, next_states, actions, rewards, and done variable in current batch
    states = torch.stack(batch.state) 
    next_states = torch.stack(batch.next_state)  
    actions = torch.Tensor(batch.action).float().to(device) 
    rewards = torch.Tensor(batch.reward).to(device)
    terminals = torch.Tensor(batch.terminal).to(device)

    # Predicting the current and next_state-action pair q-values 
    policy_qs = policy_net(states).squeeze(1) 
    target_qs = target_net(next_states).squeeze(1)  
    policy_qs = torch.sum(policy_qs.mul(actions), dim=1)  

    # Applying the Bellman Equation: R(s, a) + max_a' Q(s', a')
    target_qs = rewards + terminals * discount_factor * target_qs.max(1)[0]
    
    # Hubber-Loss Function is applied 
    loss = F.mse_loss(policy_qs, target_qs.detach()) 

    # Calculating Gradients + Back Propagation and Gradient Descent
    optimizer.zero_grad() 
    loss.backward() 
    optimizer.step() 
    return loss

def get_action(input, model, epsilon, env):
    # Epsilon-Greedy Strategy 
    if np.random.rand() <= epsilon:
        action = random.randint(0, bot.nb_actions - 1)
        return action
    else:
        qvalue = model.forward(input)
        _, action = torch.max(qvalue, 1)
        return action.cpu().numpy()[0]


# main code ------------------------------------------------------------------------------------------------------------------------------------------------------
# defining environment
env = env()
# Defining hyper-paramaters     
epsilon = 1
max_exploration_rate = 1
min_exploration_rate = 0.01
exp_decay = 0.001
discount_factor = 0.99
replay_memory = Memory(100000)
learning_rate = 0.001
batch_size = 64
steps_until_traning = 0

# Setting a device for pytorch (if available)
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

# Defining neural networks
policy_net = Network(lenstate, nb_actions).to(device) # state length, number possible actions
target_net = Network(lenstate, nb_actions).to(device)

# Setting the same parameters as the policy net for our target net 
target_net.load_state_dict(policy_net.state_dict())

# Using the Adam Optimizer
optimizer = optim.Adam(params = policy_net.parameters(), lr = learning_rate)

# Setting both the policy_net and target_net in training mode
policy_net.train()
target_net.train()

# Iterating through episodes 
for episode in range(100): # initially set to 1000
    state = torch.Tensor(env.reset()).unsqueeze(0).to(device)
    total_rewards_per_episode = 0
    done = False

    #Iterating through time_steps in current episode 
    while not done:
        if bot[0].time - bot[0].timer < 1:
            continue

        steps_until_traning += 1
        action = get_action(state, policy_net, epsilon, env)
        next_state, reward, done, info = bot.bot[0].step(action)
        next_state = torch.from_numpy(next_state).float().unsqueeze(0).to(device)

        # terminal = done variable; if done is True, a 0 will be returned. Otherwise, a 1 will be returned
        terminal = 0 if done else 1

        # turning the action into a vector with shape (2,)
        action_one_hot = np.zeros(2)
        action_one_hot[action] = 1 

        # pushing the experience into the replay memory list 
        replay_memory.push(state, action_one_hot, reward, next_state, terminal)

        # for every 4 time_steps, the networks will train
        if steps_until_traning % 4 == 0 or done:
            if len(replay_memory) > batch_size:
                batch = replay_memory.sample(batch_size)
                loss = train_model(policy_net, target_net, optimizer, batch)

        state = next_state
        total_rewards_per_episode += reward
        
        if done: 
            print(f'Total training rewards: {total_rewards_per_episode} after n steps = {episode} with eps: {epsilon} with action {action}')
            if steps_until_traning >= 100:
                print('Copying main network weights to the target network weights')
                target_net.load_state_dict(policy_net.state_dict())
                steps_until_traning = 0
            break
        
    # Updating the current exploration rate (epsilon) by applying the decay rate 
    epsilon = min_exploration_rate + (max_exploration_rate - min_exploration_rate) * np.exp(-exp_decay * episode)
