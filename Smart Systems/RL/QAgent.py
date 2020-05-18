from itertools import product
import time
import pprint as pp
import numpy as np
import random


class QAgent:

    def __init__(self, env, q_table="", render=True, debug=False):
        self.env = env
        self.render = render
        self.debug = debug
        self.q_table = q_table
        self.rewards_per_episode = []

    def process(self, episodes=15, gamma=0.99, alpha=0.01):

        if self.render:
            # Render tha maze
            self.env.render()

        self.init_q_tabe()

        for i in range(episodes):
            print(f'Episode {i}')

            state = self.pos_2_vec(self.env.reset())
            done = False
            rewards = 0
            while not done:
                # e-greedy policy
                action = self.pick_action(self.q_table[state])
                new_state, reward, done, info = self.env.step(action)
                new_state = self.pos_2_vec(new_state)
                rewards += reward

                next_action = self.pick_action(self.q_table[state], policy="greedy")
                q_value = self.q_table[state][action]
                next_q_value = self.q_table[new_state][next_action]

                self.q_table[state][action] += alpha*(reward + (gamma*next_q_value) - q_value)

                state = new_state

                if self.debug and self.render:
                    pp.pprint(self.q_table)
                    self.env.maze_view.update()
                    time.sleep(.1)

            self.rewards_per_episode.append(rewards)

    def init_q_tabe(self):
        # If there's a path
        if self.q_table:
            pass
        else:
            # Create the table
            self.q_table = {}
            for prod in product(range(0, self.env.maze_view.goal[0] + 1), repeat=2):
                self.q_table[prod] = np.zeros((4,))

    def pos_2_vec(self, pos):
        return (pos[0], pos[1])

    def pick_action(self, actions, epsilon, policy="e-greedy"):
        if policy == "e-greedy":
            if random.random() < epsilon:
                return random.randint(0, len(actions) - 1)
            else:
                return int(np.argmax(actions))

        if policy == "greedy":
            return int(np.argmax(actions))
