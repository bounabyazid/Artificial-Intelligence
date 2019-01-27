import random


# William Scott | WS

# Combinatorics - program to fill a set of 4 numbers (usually referred to as colours) randomly in an nxn matrix and then making sure that no two similar numbers are adjacent to each other.

# function to print the matrix
def print_data():
    for k in data:
        print(k)


# Where the actual operation takes place
def do_operate(t):
    print_data()
    for i in range(t):
        for j in range(t):
            print("\nOperating on " + str(data[i][j]) + ": " + str(i) + str(j))
            var = data[i][j]
            if (var == data[i][j + 1]):
                if (i > 0):
                    while (var == data[i][j + 1] or data[i - 1][j + 1] == data[i][j + 1]):
                        data[i][j + 1] = random.randint(0, 3)
                        print("guess: " + str(data[i][j + 1]))
                else:
                    while (var == data[i][j + 1]):
                        data[i][j + 1] = random.randint(0, 3)
                        print("guess: " + str(data[i][j + 1]))
            if (var == data[i + 1][j]):
                while (var == data[i + 1][j]):
                    data[i + 1][j] = random.randint(0, 3)
                    print("guess: " + str(data[i + 1][j]))
            print_data()

    for i in range(t):
        var = data[i][t]
        print("\nOperating on " + str(data[i][t]) + ": " + str(i) + str(t))
        if (var == data[i + 1][t]):
            print(var)
            while (var == data[i + 1][t] or data[i + 1][t - 1] == data[i + 1][t]):
                data[i + 1][t] = random.randint(0, 3)
                print("guess: " + str(data[i + 1][t]))
        print_data()
        var = data[t][i]
        print("\nOperating on " + str(data[t][i]) + ": " + str(t) + str(i))
        if (var == data[t][i + 1]):
            print(var)
            while (var == data[t][i + 1] or data[t][i + 1] == data[t - 1][i + 1]):
                data[t][i + 1] = random.randint(0, 3)
                print("guess: " + str(data[t][i + 1]))
        print_data()

    print("\nFinal Matrix")
    print_data()


# main code

data = []

# Taking input from user
number_of_rows = int(input("Enter the Number of Rows: "))

# Filling the data array with a matrix full of random numbers ranging from 0 to 3
for i in range(number_of_rows):
    temp = []
    for j in range(number_of_rows):
        temp.append(random.randint(0, 3))
    data.append(temp)

# calling the operator method
do_operate(number_of_rows - 1)
