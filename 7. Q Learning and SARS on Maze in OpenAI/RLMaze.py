#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import matplotlib.pyplot as plt

import gym
import gym_maze


# In[ ]:





# In[13]:


def get_action(env, Q, state, explore_rate):
    
    rand_action = env.action_space.sample()
    
    max_action = np.argmax(Q[state])
    
#     if set(Q[state])==set([0.0]):        
#         max_action = env.action_space.sample()
    
    return int(np.random.choice([rand_action, max_action], 1, p=[explore_rate, 1 - explore_rate]))


# In[ ]:





# In[3]:


def run_maze(env, explore_rate, learning_rate, discount):
    Q = np.zeros((size, size, 4))
    moves = []
    
    reward_dump = []
    
    trial = 0
    
    
    while (len(set(reward_dump[abs(len(reward_dump)-4):len(reward_dump)])) != 1 or len(moves)<2):

        trial = trial +1
        
        print("\nTrial:", trial)

        env.reset()

        state = (0, 0)

        move = 0
        
        total_reward = 0

        while True:

            env.render()

            action = get_action(env, Q, state, explore_rate)

            observation, reward, done, info = env.step(action)

            new_state = (observation[0], observation[1])

            q_dash = max(Q[new_state])
            
            total_reward += reward

            if SARSA:
                new_action = get_action(env, Q, new_state, explore_rate)

                q_dash = Q[new_state][new_action]


            Q[state][action] += learning_rate * (reward + (discount * q_dash) - Q[state][action])

            state = new_state
            if done:
                print("Reached Goal in", move, "moves")
                reward_dump.append(total_reward)
                moves.append(move)
                break

            move += 1
            
    print("Converged in", len(reward_dump), "iterations")
    dump.append((moves, "Size: " + str(size) + " | Explore Rate: " + str(explore_rate) + " | Learning Rate: " + str(
        learning_rate) + " | Discount: " + str(discount), "SARSA: "+str(SARSA),"Iterations: "+str(len(reward_dump))))
    return Q


# In[ ]:





# In[4]:


def test_model(env, Q):
    env.reset()

    state = (0, 0)

    move = 0

    while True:

        env.render()

        action = int(np.argmax(Q[state]))

        observation, reward, done, info = env.step(action)

        new_state = (observation[0], observation[1])

        if True:
            _ = int(np.argmax(Q[new_state]))

            env.step(_)

            env.step(action)

        state = new_state

        if done:
            print("Reached Goal in", move, "moves")
            break

        move += 1


# In[ ]:





# In[5]:


def print_plots(dump):
    for moves, title, SARSA, iterations in dump:
        print(SARSA)
        print(iterations)
        plt.plot(moves)
        plt.ylabel('Moves')
        plt.xlabel('Trial')
        plt.title(title)
        plt.show()


# In[ ]:





# In[ ]:





# In[6]:


size = 5

env = gym.make("maze-random-" + str(size) + "x" + str(size) + "-v0")

dump = []


# In[ ]:





# In[14]:


SARSA = False
Q = run_maze(env, 0.05, 0.3, 0.8)


# In[ ]:





# In[15]:


SARSA = True
Q = run_maze(env, 0.05, 0.3, 0.8)


# In[ ]:





# In[9]:


# dump


# In[ ]:





# In[10]:


print_plots(dump)


# In[ ]:





# In[ ]:





# In[11]:


Q


# In[ ]:





# In[ ]:





# In[12]:


test_model(env, Q)


# In[ ]:





# In[ ]:





# In[ ]:




