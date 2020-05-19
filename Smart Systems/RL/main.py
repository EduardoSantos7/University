import gym
import gym_maze
import time
import matplotlib.pyplot as plt
from concurrent.futures import ProcessPoolExecutor, as_completed, wait

from QAgent import QAgent


results_per_policy = {}


def run_sample(policy):
    env = gym.make("maze-sample-3x3-v0")
    agent = QAgent(env, debug=True)
    agent.process(episodes=10, policy=policy)

    results_per_policy[policy] = agent.rewards_per_episode

    return (policy, agent.rewards_per_episode)


if __name__ == "__main__":

    s = time.time()
    with ProcessPoolExecutor() as executor:
        policies = ["e-greedy", "greedy"]
        results = [executor.submit(run_sample, policy) for policy in policies]

        for f in as_completed(results):
            policy, rewards = f.result()
            print(policy, rewards)
            results_per_policy[policy] = rewards


    e = time.time()
    print(f'total time: {e-s}')

    print("voy")
    print(results_per_policy)
    colors = ["r", "b", "g"]
    for i, (policy, results) in enumerate(results_per_policy.items()):
        print(results_per_policy)

        plt.plot(results, colors[i], label=policy)

    plt.xlabel('Number of episodes')
    plt.ylabel('Reward')
    plt.legend(loc="upper left")
    plt.grid()
    plt.title("Reward per episode")
    plt.show()

    # time.sleep(10)
