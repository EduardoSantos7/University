import os
from itertools import product
import time
import pprint as pp
import numpy as np
import random
import pickle
from statistics import mean


class QAgent:

    def __init__(self, env, q_table="", render=True, debug=False):
        self.env = env
        self.render = render
        self.debug = debug
        self.q_table = q_table
        self.rewards_per_episode = []

        if self.render:
            # Render tha maze
            self.env.render()

    def process(self, episodes=2, gamma=0.99, alpha=0.01, epsilon=1.0, epsilon_decrease=.1, policy="e-greedy"):

        self.init_q_tabe(path="")

        for episode in range(episodes):

            # Update epsilon each 5 episodes
            if episode % 5 == 0:
                epsilon = max(0.05, epsilon - epsilon_decrease)
                print(f'''
                    Episode: {episode}
                    Rewards: {mean(self.rewards_per_episode or [0])}
                    Epsilon: {epsilon}
                    ''')

            state = self.pos_2_vec(self.env.reset())
            done = False
            rewards = 0
            while not done:
                # e-greedy policy
                action = self.pick_action(self.q_table[state], epsilon=epsilon)
                new_state, reward, done, info = self.env.step(action)
                new_state = self.pos_2_vec(new_state)
                rewards += reward

                next_action = self.pick_action(self.q_table[state], policy=policy)
                q_value = self.q_table[state][action]
                next_q_value = self.q_table[new_state][next_action]

                self.q_table[state][action] += alpha*(reward + (gamma*next_q_value) - q_value)

                state = new_state

                if self.debug and self.render:
                    # pp.pprint(self.q_table)
                    self.env.maze_view.update()
                    time.sleep(.1)

            self.rewards_per_episode.append(rewards)

        # self.save_q_table(policy, episode)

    def init_q_tabe(self, path=None):
        # If there's a path
        if self.q_table:
            with open(path, "rb") as f:
                self.q_table = pickle.load(f)
        else:
            # Create the table
            self.q_table = {}
            for prod in product(range(0, self.env.maze_view.goal[0] + 1), repeat=2):
                self.q_table[prod] = np.zeros((4,))

    def pos_2_vec(self, pos):
        return (pos[0], pos[1])

    def pick_action(self, actions, epsilon=1, policy="e-greedy"):
        if policy == "e-greedy":
            if random.random() < epsilon:
                return random.randint(0, len(actions) - 1)
            else:
                return int(np.argmax(actions))

        if policy == "greedy":
            return int(np.argmax(actions))

        if policy == "soft_max":
            prob_t = [np.exp(q_value/epsilon) for q_value in actions]
            prob_t = np.true_divide(prob_t, sum(prob_t))
            rand_probability = random.random()
            # Get a random action from a list of actions which
            # contain values greater than a random probability.
            # If the list is empty then pick a random action.
            gradient = [i for i, num in enumerate(
                prob_t) if num > rand_probability]

            if gradient:
                return random.choice([i for i, num in enumerate(prob_t) if num > rand_probability])
            
            return random.randint(0, len(actions) - 1)

    def save_q_table(self, policy, episodes):
        dimensions = f'{self.env.maze_view.goal[0] + 1}x{self.env.maze_view.goal[0] + 1}'
        rewards = mean(self.rewards_per_episode)

        with open(f"q_table/{dimensions}/{policy}_E_{episodes}.pickle", "wb") as f:
            pickle.dump(self.q_table, f)
