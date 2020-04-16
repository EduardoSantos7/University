import time
import sys

import pygame
import gym
import gym_maze
import matplotlib.pyplot as plt

from agent import Agent
from memory_profiler import memory_usage


def test(search_type, with_portals=False, test_mem=False):
    NUM_TEST = 1
    speed = {}
    memory = {}

    total = 0
    mem_total = []
    for x, y in [(3, 3), (5, 5), (10, 10), (20, 20), (30, 30), (100, 100)]:
        total = 0
        mem_total = []
        for _ in range(NUM_TEST):
            # Initialize the "maze" environment
            portals = "-plus" if with_portals or x in [20, 30] else ""
            env = gym.make(f"maze-random-{x}x{y}{portals}-v0")

            agent = Agent(env, type_search=search_type, render=False, debug=False)

            if test_mem:
                start = time.time()
                mem_usage = memory_usage(agent.process)
                end = time.time()
                mem_total.extend(mem_usage)
            else:
                start = time.time()
                agent.process()
                end = time.time()

            total += end - start
            

        speed[x] = total / NUM_TEST
        memory[x] = max(mem_total) if mem_total else []

    return speed, memory


if __name__ == "__main__":

    # Initialize the "maze" environment
    # env = gym.make("maze-random-100x100-v0")

    # agent = Agent(env, type_search=Agent.SearchTypes.A_STAR, debug=True)

    # agent.process()

    # Test
    results, _ = test(Agent.SearchTypes.BREATH_FIRST_SEARCH)
    results_2, _ = test(Agent.SearchTypes.A_STAR)

    plt.plot(list(results.keys()), list(results.values()), 'r', label="BFS")
    plt.plot(list(results_2.keys()), list(results_2.values()), 'b', label="A*")
    plt.xlabel('Grid Size (N)')
    plt.ylabel('Seconds')
    plt.legend(loc="upper left")
    plt.grid()
    plt.title("Time Used")
    plt.show()

    _, memory = test(Agent.SearchTypes.BREATH_FIRST_SEARCH, test_mem=True)
    _, memory_2 = test(Agent.SearchTypes.A_STAR, test_mem=True)

    plt.plot(list(memory.keys()), list(memory.values()), 'r', label="BFS")
    plt.plot(list(memory_2.keys()), list(memory_2.values()), 'b', label="A*")
    plt.xlabel('Grid Size (N)')
    plt.ylabel('Memory (MiB)')
    plt.legend(loc="upper left")
    plt.grid()
    plt.title("Memory Used")
    plt.show()

    # mem_usage = memory_usage(agent2.process)
    # print('Maximum memory usage: %s' % max(mem_usage))

    time.sleep(5)
