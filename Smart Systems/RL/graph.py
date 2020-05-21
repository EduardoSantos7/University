from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib import style
import numpy as np
import math as m

style.use('ggplot')


def get_q_color(value, vals):
    if m.isclose(value, max(vals), abs_tol=0.000001):
        return "green", 1.0, 50
    else:
        return "red", 0.4, 50


SIZE = 10
POLICIES = ["e-greedy", "greedy", "soft_max"]

for eps in range(0, 200):
    fig = plt.figure(figsize=(12, 9))
    ax1 = fig.add_subplot(311)
    ax2 = fig.add_subplot(312)
    ax3 = fig.add_subplot(313)
    q_table = np.load(f"q_table/q_learning/{SIZE}x{SIZE}/e-greedy_E_{eps}.pickle", allow_pickle=True)
    q_table2 = np.load(
        f"q_table/q_learning/{SIZE}x{SIZE}/greedy_E_{eps}.pickle", allow_pickle=True)
    q_table3 = np.load(
        f"q_table/q_learning/{SIZE}x{SIZE}/soft_max_E_{eps}.pickle", allow_pickle=True)

    for i, ((x, y), q_values) in enumerate(q_table.items()):
        for j, q_val in enumerate(q_values):
            ax1.scatter(i, j,
                        c=get_q_color(q_val, q_values)[0],
                        alpha=get_q_color(q_val, q_values)[1],
                        s=get_q_color(q_val, q_values)[2],
                        marker="o")

        ax1.set_ylabel("Actions in E-greedy", fontsize=9)

    for i, ((x, y), q_values) in enumerate(q_table2.items()):
        for j, q_val in enumerate(q_values):
            ax2.scatter(i, j,
                        c=get_q_color(q_val, q_values)[0],
                        alpha=get_q_color(q_val, q_values)[1],
                        s=get_q_color(q_val, q_values)[2],
                        marker="o")

        ax2.set_ylabel("Actions in Greedy", fontsize=9)

    for i, ((x, y), q_values) in enumerate(q_table3.items()):
        for j, q_val in enumerate(q_values):
            ax3.scatter(i, j,
                        c=get_q_color(q_val, q_values)[0],
                        alpha=get_q_color(q_val, q_values)[1],
                        s=get_q_color(q_val, q_values)[2],
                        marker="o")

        ax3.set_ylabel("Actions in SoftMax", fontsize=9)

    plt.yticks(np.arange(0, 4, 1))
    plt.savefig(f"images/q_learning/{SIZE}x{SIZE}/E_{eps}.png")
    plt.clf()
    #plt.show()
