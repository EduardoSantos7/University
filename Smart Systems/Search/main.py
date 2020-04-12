import time

import pygame
import gym
import gym_maze

from agent import Agent


if __name__ == "__main__":

    # Initialize the "maze" environment
    env = gym.make("maze-random-10x10-plus-v0")

    agent = Agent(env, type_search=Agent.SearchTypes.BREATH_FIRST_SEARCH)

    agent.process()

    time.sleep(10)
