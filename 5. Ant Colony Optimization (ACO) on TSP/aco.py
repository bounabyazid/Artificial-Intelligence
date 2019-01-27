import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import random
import copy
from scipy.spatial import distance
from collections import Counter
import time

start_time = time.time()


def print_matrix(m):
    for i in m:
        print(i)
    print("")


def gen_rand_coordinates(n):
    coordinates = []
    for i in range(n):
        a = random.randint(0, 2 * n)
        b = random.randint(0, 2 * n)
        if ((a, b)) not in coordinates:
            coordinates.append((a, b))

    print("\nCoordinates:", coordinates, "\n")

    return coordinates


# G = nx.Graph()
# for p in range(len(coordinates)):
#     G.add_node(p, pos=[coordinates[p][0], coordinates[p][1]])
# pos = nx.get_node_attributes(G, 'pos')
# G_dash = copy.deepcopy(G)
# G_dash.add_edge(path[i], path[i + 1])
# edges = G_dash.edges()
# weights = [G_dash[u][v]['weight'] for u, v in edges]

# nx.draw_networkx(G_dash, pos, node_size=300, edges=edges, width=weights)
# plt.show()




# def gen_rand_distance_matrix(n):
#     matrix = []
#     for i in range(n):
#         p = []
#         for j in range(n):
#             if i == j:
#                 p.append(0)
#             else:
#                 p.append(random.randint(1, n))
#         matrix.append(p)
#     rez = [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]
#     result = [[matrix[i][j] + rez[i][j] for j in range(len(matrix[0]))] for i in range(len(matrix))]
#     print_matrix(result)
#     return result
# distance_matrix = gen_rand_distance_matrix(no_of_cities)
# K = nx.from_numpy_matrix(np.array(distance_matrix))
# gen_positions = nx.random_layout(K)
# print("K", gen_positions)
# G = nx.Graph()
# for p in range(len(gen_positions)):
#     G.add_node(p, pos=gen_positions[p])
# pos = nx.get_node_attributes(G, 'pos')
# print("Positions:", pos, "\n")
# nx.draw_networkx(G, pos, node_size=1000)
# plt.show()


no_of_cities = 10
no_of_ants = 20
pheromone_evaporation_level = 0.1
alpha = 4
beta = 6

coordinates = gen_rand_coordinates(no_of_cities)

distance_matrix = []

for i in range(no_of_cities):
    a = []
    for k in range(no_of_cities):
        # print(i, k, coordinates[i], coordinates[k], distance.euclidean(coordinates[i], coordinates[k]))
        a.append(int(distance.euclidean(coordinates[i], coordinates[k])))
    distance_matrix.append(a)

print("Distance Matrix")
print_matrix(distance_matrix)

G = nx.Graph()
for p in range(len(coordinates)):
    G.add_node(p, pos=[coordinates[p][0], coordinates[p][1]])
pos = nx.get_node_attributes(G, 'pos')

pheromone_level = list(np.zeros((no_of_cities, no_of_cities)))

plm = [-1, -1]
history_ant_his = []

iteration = 0
while len(plm) > 1:
    ant_history = []
    for i in range(no_of_ants):

        allowed_cites = list(range(no_of_cities))

        ant_choice = []
        distance = 0

        antchoice = 0
        ant_choice.append(antchoice)
        allowed_cites.remove(antchoice)

        prev_choice = antchoice

        while allowed_cites:

            denominator = 0

            i_node = ant_choice[len(ant_choice) - 1]

            probs = []

            for j_node in allowed_cites:
                probs.append((pheromone_level[i_node][j_node] ** alpha) * ((1.0 / distance_matrix[i_node][j_node]) ** beta))
                denominator += (pheromone_level[i_node][j_node] ** alpha) * ((1.0 / distance_matrix[i_node][j_node]) ** beta)

            probs = probs / denominator

            if iteration == 0:
                antchoice = random.choice(allowed_cites)
            else:
                antchoice = np.random.choice(allowed_cites, p=probs)
            ant_choice.append(antchoice)
            allowed_cites.remove(antchoice)
            distance += distance_matrix[ant_choice[len(ant_choice) - 1]][ant_choice[len(ant_choice) - 2]]

        ant_choice.append(ant_choice[0])
        distance += distance_matrix[ant_choice[len(ant_choice) - 1]][ant_choice[len(ant_choice) - 2]]

        ant_history.append((ant_choice, distance))

    G_dash = copy.deepcopy(G)

    cal_edges = []

    for an in ant_history:
        path = an[0]
        for nod in range(len(path) - 1):
            if (path[nod], path[nod + 1]) and (path[nod + 1], path[nod]) not in cal_edges:
                cal_edges.append((path[nod], path[nod + 1]))
            elif (path[nod], path[nod + 1]) in cal_edges:
                cal_edges.append((path[nod], path[nod + 1]))
            else:
                cal_edges.append((path[nod + 1], path[nod]))

    weighted_edges = Counter(cal_edges)

    for pher_i in range(len(pheromone_level)):
        for pher_j in range(len(pheromone_level)):
            pheromone_level[pher_i][pher_j] = (1 - pheromone_evaporation_level) * pheromone_level[pher_i][pher_j]
            pheromone_level[pher_j][pher_i] = pheromone_level[pher_i][pher_j]

    # print_matrix(pheromone_level)

    for k in ant_history:
        l = k[1]
        path = k[0]

        for i in range(len(path) - 1):
            G_dash.add_edge(path[i], path[i + 1], weight=(weighted_edges[(path[i], path[i + 1])] + weighted_edges[(path[i + 1], path[i])]) / (no_of_ants / 4))
            pheromone_level[path[i]][path[i + 1]] += (1.0 / l)
            pheromone_level[path[i + 1]][path[i]] = pheromone_level[path[i]][path[i + 1]]

    # print_matrix(ant_history)

    history_ant_his = ant_history

    coun = []

    for ck in ant_history:
        coun.append(ck[1])

    plm = Counter(coun)

    print("Unique Paths:")
    print(len(plm))

    edges = G_dash.edges()
    weights = [G_dash[u][v]['weight'] for u, v in edges]

    nx.draw_networkx(G_dash, pos, node_size=300, edges=edges, width=weights)
    plt.show()

    iteration += 1

print(history_ant_his[0])
print("Iterations:", iteration)
print("Time %s" % (time.time() - start_time))
