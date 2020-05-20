import gym
import gym_maze
import time
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor, as_completed, wait

from QAgent import QAgent


EPISODES = 200
GRID_SIZE = 100
results_per_policy = {}


def run_sample(policy):
    env = gym.make(f"maze-sample-{GRID_SIZE}x{GRID_SIZE}-v0")
    agent = QAgent(env, render=False, debug=False)
    agent.process(episodes=EPISODES, policy=policy)

    results_per_policy[policy] = agent.rewards_per_episode

    return (policy, agent.rewards_per_episode)


if __name__ == "__main__":

    s = time.time()
    with ProcessPoolExecutor() as executor:
        policies = ["e-greedy", "greedy", "soft_max"]
        results = [executor.submit(run_sample, policy) for policy in policies]

        for f in as_completed(results):
            policy, rewards = f.result()
            results_per_policy[policy] = rewards

    e = time.time()
    print(f'total time: {e-s}')

    colors = ["r", "b", "g"]
    for i, (policy, results) in enumerate(results_per_policy.items()):
        plt.plot(results, colors[i], label=policy)

    plt.xlabel('Number of episodes')
    plt.ylabel('Reward')
    plt.legend(loc="lower right")
    plt.grid()
    plt.title(f"Av. Rewards in a grid of {GRID_SIZE}x{GRID_SIZE}")
    plt.show()

    # time.sleep(10)
