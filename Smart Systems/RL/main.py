import gym
import gym_maze
import time
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor, as_completed, wait

from QAgent import QAgent
from SARSAAgent import SARSAAgent


EPISODES = 10
GRID_SIZE = 3
results_per_policy = {}


def run_sample(policy):
    env = gym.make(f"maze-sample-{GRID_SIZE}x{GRID_SIZE}-v0")
    agent = QAgent(env, render=True, debug=True)
    agent.process(episodes=EPISODES, policy=policy)

    results_per_policy[policy] = agent.rewards_per_episode

    return (policy, agent.rewards_per_episode)


def compare_sarsa_q_learning(policy):
    env = gym.make(f"maze-sample-{GRID_SIZE}x{GRID_SIZE}-v0")
    q_agent = QAgent(env, render=False, debug=False)
    sarsa_agent = SARSAAgent(env, render=False, debug=False)
    q_agent.process(episodes=EPISODES, policy=policy)
    sarsa_agent.process(episodes=EPISODES, policy=policy)

    results_per_policy[policy] = [
        q_agent.rewards_per_episode, sarsa_agent.rewards_per_episode]

    return (policy, [
        q_agent.rewards_per_episode, sarsa_agent.rewards_per_episode])


def test_policies_in_same_algorithm():

    s = time.time()
    with ProcessPoolExecutor() as executor:
        policies = ["greedy"]
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


def test_policies_in_both_algorithms():

    s = time.time()
    with ProcessPoolExecutor() as executor:
        policies = ["soft_max"]
        results = [executor.submit(compare_sarsa_q_learning, policy)
                   for policy in policies]

        for f in as_completed(results):
            policy, rewards = f.result()
            results_per_policy[policy] = rewards

    e = time.time()
    print(f'total time: {e-s}')

    colors = ["r", "b", "g"]
    for i, (policy, results) in enumerate(results_per_policy.items()):
        plt.plot(results[0], colors[1], label=f'Q Learning - {policy}')
        plt.plot(results[1], colors[2], label=f'SARSA - {policy}')

    plt.xlabel('Number of episodes')
    plt.ylabel('Reward')
    plt.legend(loc="lower right")
    plt.grid()
    plt.title(f"Av. Rewards per policy and algo. in a grid of {GRID_SIZE}x{GRID_SIZE}")
    plt.show()



if __name__ == "__main__":
    test_policies_in_same_algorithm()
    # test_policies_in_both_algorithms()
