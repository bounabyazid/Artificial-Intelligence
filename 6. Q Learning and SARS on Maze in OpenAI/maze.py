import numpy as np
import matplotlib.pyplot as plt

import gym
import gym_maze


def run_maze(env, explore_rate, learning_rate, discount, trials):
    Q = np.zeros((size, size, 4))
    moves = []

    for trial in range(trials):

        print("\nTrial:", (trial + 1))

        env.reset()

        state = (0, 0)

        move = 0

        V = np.zeros((size, size, 4))

        while True:

            env.render()

            rand_action = env.action_space.sample()

            max_action = np.argmax(Q[state])

            action = int(np.random.choice([rand_action, max_action], 1, p=[explore_rate, 1 - explore_rate]))

            observation, reward, done, info = env.step(action)

            new_state = (observation[0], observation[1])

            q_dash = max(Q[new_state])

            if SARS:
                new_action = np.argmax(Q[new_state])

                q_dash = Q[new_state][new_action]

            Q[state][action] += learning_rate * (reward + (discount * q_dash) - Q[state][action])

            V[new_state][action] = reward

            state = new_state
            if done:
                print("Reached Goal in", move, "moves")
                moves.append(move)
                break

            move += 1

        if trials == 1:

            print(V)

    dump.append((moves, "Learning Rate: " + str(learning_rate)))


size = 5

env = gym.make("maze-random-" + str(size) + "x" + str(size) + "-v0")

dump = []
SARS = False
run_maze(env, 0.05, 0.2, 0.8, 1)

dump = []
SARS = True
run_maze(env, 0.05, 0.2, 0.8, 1)

# dump = []
# SARS = False
# run_maze(env, 0.05, 0.8, 0.8, 40)
#
# for moves, title in dump:
#     print(title)
#     print(moves, "\n")
#
#     plt.bar(list(range(len(moves))), moves)
#     plt.title(title)
#     plt.show()
#
# dump = []
# SARS = False
# run_maze(env, 0.05, 0.8, 0.2, 40)
#
# for moves, title in dump:
#     print(title)
#     print(moves, "\n")
#     plt.bar(list(range(len(moves))), moves)
#
#     plt.title(title)
#     plt.show()
#
# dump = []
# SARS = False
# run_maze(env, 0.2, 0.8, 0.8, 40)
#
# for moves, title in dump:
#     print(title)
#     print(moves, "\n")
#     plt.bar(list(range(len(moves))), moves)
#
#     plt.title(title)
#     plt.show()
#
# dump = []
# SARS = False
# run_maze(env, 0.05, 1, 0.8, 60)
#
# for moves, title in dump:
#     print(title)
#     print(moves, "\n")
#     plt.bar(list(range(len(moves))), moves)
#
#     plt.title(title)
#     plt.show()
#
# dump = []
# SARS = True
# run_maze(env, 0.05, 0.8, 0.8, 40)
#
# for moves, title in dump:
#     print(title)
#     print(moves, "\n")
#     plt.bar(list(range(len(moves))), moves)
#
#     plt.title(title)
#     plt.show()
#
# dump = []
# SARS = True
# run_maze(env, 0.05, 0.8, 0.2, 40)
#
# for moves, title in dump:
#     print(title)
#     print(moves, "\n")
#     plt.bar(list(range(len(moves))), moves)
#
#     plt.title(title)
#     plt.show()
#
# dump = []
# SARS = True
# run_maze(env, 0.2, 0.8, 0.8, 40)
#
# for moves, title in dump:
#     print(title)
#     print(moves, "\n")
#     plt.bar(list(range(len(moves))), moves)
#
#     plt.title(title)
#     plt.show()
#
# dump = []
# SARS = True
# run_maze(env, 0.05, 1, 0.8, 40)
#
# print("\nFinal Results:")
#
# for moves, title in dump:
#     print(title)
#     print(moves, "\n")
#     plt.bar(list(range(len(moves))), moves)
#
#     plt.title(title)
#     plt.show()
