import copy


def print_data(data):
    for k in data:
        print(k)


def insert_for_a_star(queue_array, insert_object):
    if queue_array:
        check = 0
        for i in range(len(queue_array)):
            if queue_array[i][1] >= insert_object[1]:
                check = 1
                queue_array.insert(i, insert_object)
                break
        if check == 0:
            queue_array.append(insert_object)
    else:
        queue_array.append(insert_object)


def find_manhattan_dist(arr, final_arr):
    manhattan = 0
    for p in range(len(final_arr)):
        for q in range(len(final_arr)):
            element = arr[p][q]
            m = 0
            n = 0
            for t in range(len(final_arr)):
                try:
                    n = final_arr[t].index(element)
                    m = t
                except:
                    a = 1
            manhattan = manhattan + abs(n - p) + abs(m - q)
    return manhattan


def find_possibilities(input_array):
    possibilities = []
    n = 0
    m = 0
    size = len(input_array[0]) - 1
    for i in range(size + 1):
        try:
            n = input_array[i].index(0)
            m = i
        except:
            a = 1
    for i in [-1, 1]:
        if (m + i) >= 0 and m + i <= size:
            possibilities.append((m + i, n))
    for j in [-1, 1]:
        if (n + j) >= 0 and n + j <= size:
            possibilities.append((m, n + j))
    return [possibilities, (m, n)]


def compute_a_star(original_array, final_array, bound):
    if (bound != -1):
        print("**Trying bound: " + str(bound))

    queue = []

    extended_list = []

    queue.append([original_array, find_manhattan_dist(original_array, final_array), [], 0])

    count = 0

    max_heuristic = 0

    while queue:
        popped_array = queue.pop(0)

        if (max_heuristic < popped_array[1]):
            max_heuristic = popped_array[1]

        if popped_array[0] == final_array:
            print("\n**Done**")
            print_data(popped_array[0])
            print("Cost : " + str(popped_array[3]))
            print("Queue Size: " + str(len(queue)))
            print("Moves: " + str(popped_array[2]))
            exit(0)

        count = count + 1
        extended_list.append(popped_array[0])
        array_possibilities = find_possibilities(popped_array[0])

        m = array_possibilities[1][0]
        n = array_possibilities[1][1]

        print("Queue: " + str(len(queue)) + " Extended: " + str(len(extended_list)) + " Heuristic Cost: " + str(
            popped_array[1]) + " Cost: " + str(popped_array[3]))

        for z in array_possibilities[0]:
            temp_data = copy.deepcopy(popped_array[0])
            temp_data[m][n] = temp_data[z[0]][z[1]]
            swap_element = temp_data[z[0]][z[1]]
            temp_data[z[0]][z[1]] = 0

            manhattan_dist = find_manhattan_dist(temp_data, final_array)

            insert_data = [temp_data, popped_array[3] + 1 + manhattan_dist,
                           popped_array[2] + ["Swap with " + str(swap_element)],
                           popped_array[3] + 1]

            if (max_heuristic < insert_data[1]):
                max_heuristic = insert_data[1]

            if temp_data not in extended_list:
                if bound == -1:
                    insert_for_a_star(queue, insert_data)
                else:
                    if bound >= (insert_data[1]):
                        insert_for_a_star(queue, insert_data)

            if insert_data[0] == final_array:
                print("\n\n\n**Found while enqueuing, but waiting to dequeue this**")
                print_data(insert_data[0])
                print("Cost : " + str(insert_data[3]))
                print("Queue Size: " + str(len(queue)))
                print("Moves: " + str(insert_data[2]) + "\n\n\n")

    if bound > (max_heuristic):
        return [0]
    else:
        return [1]


# original_array = [[0, 3],
#                   [1, 2]]
#
# final_array = [[1, 2],
#                [2, 0]]
#
# original_array = [[1, 3, 0],
#                   [4, 2, 6],
#                   [7, 5, 8]]
#
# final_array = [[1, 2, 3],
#                [4, 5, 6],
#                [7, 8, 0]]
#
# original_array = [[2, 0, 3, 4],
#                   [1, 5, 6, 7],
#                   [9, 11, 12, 8],
#                   [13, 10, 14, 15]]
#
# final_array = [[1, 2, 3, 4],
#                [5, 6, 7, 8],
#                [9, 10, 11, 12],
#                [13, 14, 15, 0]]
#
# original_array = [[1, 2, 3, 4, 5],
#                   [6, 7, 8, 9, 10],
#                   [11, 12, 13, 14, 15],
#                   [16, 17, 18, 0, 19],
#                   [21, 22, 23, 24, 20]]
#
# final_array = [[1, 2, 3, 4, 5],
#                [6, 7, 8, 9, 10],
#                [11, 12, 13, 14, 15],
#                [16, 17, 18, 19, 20],
#                [21, 22, 23, 24, 0]]

n = int(input("\nEnter size of Matrix: "))

print("Input Matrix: ")
original_array = []
for i in range(n):
    temp = []
    for j in range(n):
        temp += [int(input("[" + str(i) + str(j) + "]: "))]
    original_array.append(temp)

c = 0
final_array = []
for i in range(n):
    temp = []
    for j in range(n):
        c = (c + 1) % (n * n)
        temp += [c]
    final_array.append(temp)

print_data(original_array)
print("")
print_data(final_array)

queue = []

extended_list = []

usr_input = int(input(
    "\n1. BFS\n2. DFS\n3. BFS with Extended List Check\n4. DFS with Extended List Check\n5. A*\n6. IDA*\nEnter Option: "))

if usr_input == 1 or usr_input == 2 or usr_input == 3 or usr_input == 4:

    queue.append([original_array, 0, []])

    print("\n----Operating---")

    count = 0

    while queue:
        popped_array = queue.pop(0)

        if popped_array[0] == final_array:
            print("\n**Done**")
            print_data(popped_array[0])
            print("Cost: " + str(popped_array[1]))
            print("Queue Size: " + str(len(queue)))
            print("Moves: " + str(popped_array[2]))
            exit(0)

        count = count + 1
        extended_list.append(popped_array[0])
        array_possibilities = find_possibilities(popped_array[0])

        m = array_possibilities[1][0]
        n = array_possibilities[1][1]

        print("Queue: " + str(len(queue)) + " Extended: " + str(len(extended_list)) + " Cost: " + str(popped_array[1]))
        for z in array_possibilities[0]:
            # print(queue)
            temp_data = copy.deepcopy(popped_array[0])
            temp_data[m][n] = temp_data[z[0]][z[1]]
            swap_element = temp_data[z[0]][z[1]]
            temp_data[z[0]][z[1]] = 0

            insert_data = [temp_data, popped_array[1] + 1, popped_array[2] + ["Move " + str(swap_element)]]

            if usr_input == 1:
                queue.append(insert_data)
            elif usr_input == 2:
                queue.insert(0, insert_data)
            if usr_input == 3:
                if temp_data not in extended_list:
                    queue.append(insert_data)
            elif usr_input == 4:
                if temp_data not in extended_list:
                    queue.insert(0, insert_data)

            if insert_data[0] == final_array:
                print("\n\n\n**Found while enqueuing, but waiting to dequeue this**")
                print_data(insert_data[0])
                print("Cost: " + str(insert_data[1]))
                print("Queue Size: " + str(len(queue)))
                print("Moves: " + str(insert_data[2]) + "\n\n\n")
    print("No Permutation Possible for the given input")

elif usr_input == 5:
    print("\n---Performing A*---")
    compute_a_star(original_array, final_array, -1)

elif usr_input == 6:
    print("\n---Performing IDA*---")

    bound = 40

    while compute_a_star(original_array, final_array, bound)[0]:
        print("\n**Bound " + str(bound) + " Failed\n\n")
        bound = bound + 1

    print("No Permutation Possible for the given input")
else:
    print("Invalid Input! Please try again...")
