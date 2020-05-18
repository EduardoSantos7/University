import gym
import gym_maze
import time
import matplotlib.pyplot as plt

from QAgent import QAgent


if __name__ == "__main__":

    # Initialize the "maze" environment
    env = gym.make("maze-random-3x3-v0")
    agent = QAgent(env, debug=True)
    s = time.time()
    agent.process(episodes=15)
    e = time.time()
    print(f'total time: {e-s}')

    plt.plot(agent.rewards_per_episode, 'r', label="Q Table")
    plt.xlabel('Number of episodes')
    plt.ylabel('Reward')
    plt.legend(loc="upper left")
    plt.grid()
    plt.title("Reward per episode")
    plt.show()

    # time.sleep(10)
