import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import Adam
import tensorflow as tf
from collections import deque
import time
import random
from tqdm import tqdm
from statistics import mean

import gym
import gym_maze
from matplotlib import pyplot as plt


REPLAY_MEMORY_SIZE = 50

# Minimum number of steps in a memory to start training
MIN_SIZE = 1_000
MINIBATCH_SIZE = 64
UPDATE_TARGET_EVERY = 2

MIN_EPSILON = 0.001

DISCOUNT = 0.99

#  Stats settings
STATS = 5  # episodes
SHOW_PREVIEW = True

GRID_SIZE = 3
env = gym.make(f"maze-sample-{GRID_SIZE}x{GRID_SIZE}-v0")


# Agent class
class DQNAgent:
    def __init__(self, env, render=True, debug=False):

        self.model = self.create_model()
        self.env = env

        self.target_model = self.create_model()
        self.target_model.set_weights(self.model.get_weights())

        self.replay_memory = deque(maxlen=REPLAY_MEMORY_SIZE)

        self.target_update_counter = 0

        self.MIN_REWARD = -5

        self.render = render
        self.debug = debug
        self.rewards_per_episode = []

        if self.render:
            # Render tha maze
            self.env.render()

    def create_model(self):
        model = Sequential()

        model.add(Dense(32, input_shape=(2,)))
        model.add(Activation('relu'))

        model.add(Dense(32))
        model.add(Activation('relu'))

        model.add(Dense(4))
        model.add(Activation('linear'))

        model.compile(loss="mse", optimizer=Adam(
            lr=0.001), metrics=['accuracy'])

        return model

    def train(self, terminal_state, step):

        # Entrena una vez haya guardado MIN_SIZE + 1 muestras
        if len(self.replay_memory) < MIN_SIZE:
            return

        minibatch = random.sample(self.replay_memory, MINIBATCH_SIZE)

        current_states = np.array([transition[0]
                                   for transition in minibatch])
        current_qs_list = self.model.predict(current_states)

        new_current_states = np.array(
            [transition[3] for transition in minibatch])
        future_qs_list = self.target_model.predict(new_current_states)

        input_ = []
        output_ = []

        for index, (current_state, action, reward, new_current_state, done) in enumerate(minibatch):

            if not done:
                max_future_q = np.max(future_qs_list[index])
                new_q = reward + DISCOUNT * max_future_q
            else:
                new_q = reward

            # Actualiza q value
            current_qs = current_qs_list[index]
            current_qs[action] = new_q

            input_.append(current_state)
            output_.append(current_qs)

        # Ajusta los valores
        self.model.fit(np.array(input_), np.array(output_), batch_size=MINIBATCH_SIZE, verbose=0,
                       shuffle=False if terminal_state else None)
        self.model.fit()

        if terminal_state:
            self.target_update_counter += 1

        # Actualiza los pesos de target_model con los pesos de model
        if self.target_update_counter > UPDATE_TARGET_EVERY:
            self.target_model.set_weights(self.model.get_weights())
            self.target_update_counter = 0

    def update_replay_memory(self, transition):
        self.replay_memory.append(transition)

    def get_qs(self, state):
        return self.model.predict(np.array(state).reshape(-1, *state.shape))[0]

    def process(self, episodes=100, epsilon=1.0, epsilon_decrease=.1, policy="e-greedy"):

        for episode in tqdm(range(1, episodes + 1), ascii=True, unit='episodes'):

            # Update epsilon each 5 episodes
            if episode % 5 == 0:
                epsilon = max(0.05, epsilon - epsilon_decrease)
                print(f'''
                    Episode: {episode}
                    Rewards: {mean(self.rewards_per_episode or [0])}
                    Epsilon: {epsilon}
                    ''')

            current_state = env.reset()          
            rewards = 0
            step = 1

            done = False
            while not done:
                if np.random.random() > epsilon:

                    action = np.argmax(self.get_qs(current_state))
                else:
                    action = np.random.randint(0, 4)

                action = ['N', 'E', 'S', 'W'][action]
                new_state, reward, done, _ = env.step(action)

                rewards += reward

                # if SHOW_PREVIEW and not episode % STATS:
                #     self.env.render()
                #     self.env.maze_view.update()
                #     time.sleep(.01)

                self.update_replay_memory(
                    (current_state, action, reward, new_state, done))
                self.train(done, step)

                current_state = new_state
                step += 1

            self.rewards_per_episode.append(rewards)

            min_reward = min(self.rewards_per_episode)
            max_reward = max(self.rewards_per_episode)

            if min_reward >= self.MIN_REWARD:
                #Guarda modelo
                self.model.save(
                    f'models/{max_reward:_>7.2f}.model')

            if epsilon > MIN_EPSILON:
                epsilon *= epsilon_decrease
                epsilon = max(MIN_EPSILON, epsilon)


agent = DQNAgent(env)

agent.process()

plt.plot(agent.rewards_per_episode)

plt.xlabel('Number of episodes')
plt.ylabel('Reward')
plt.legend(loc="lower right")
plt.grid()
plt.title(
    f"Av. Rewards per policy and algo. in a grid of {GRID_SIZE}x{GRID_SIZE}")
plt.show()
