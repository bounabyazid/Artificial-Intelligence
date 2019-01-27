import copy


def is_done(board):
    for element in ["O", "X"]:
        if board[0][0] == board[1][1] == board[2][2] == element or board[0][2] == board[1][1] == board[2][0] == element:
            return True, element
        for i in [0, 1, 2]:
            if board[i][0] == board[i][1] == board[i][2] == element or board[0][i] == board[1][i] == board[2][i] == element:
                return True, element
    return False, ""


def get_empty_places(board):
    list_ = []
    for i in [0, 1, 2]:
        for j in [0, 1, 2]:
            if board[i][j] == " ":
                list_.append((i, j))
    return list_


def print_board(board):
    print("\n")
    for i in board:
        print(i)


def minimax(board, is_maximising, p, alpha, beta):
    count.append("")

    empty = get_empty_places(board)

    check = is_done(board)
    if check[0]:
        if check[1] == "X":
            return 1, 0
        else:
            return -1, 0

    if len(empty) == 0:
        return 0, 0

    if is_maximising:

        best = -1
        best_move = empty[0]

        for i in empty:
            temp_board = copy.deepcopy(board)
            temp_board[i[0]][i[1]] = "X"
            return_value = minimax(temp_board, False, p + 1, alpha, beta)
            if best < return_value[0]:
                best = return_value[0]
                best_move = i

        return best, best_move

    else:
        best_min = 1
        best_min_move = empty[0]

        for i in empty:
            temp_board = copy.deepcopy(board)
            temp_board[i[0]][i[1]] = "O"
            return_value = minimax(temp_board, True, p + 1, alpha, beta)
            if best_min > return_value[0]:
                best_min = return_value[0]
                best_min_move = i

        return best_min, best_min_move


count = []

while True:
    print("\n\n---William Scott Minimax---\n")

    use_pruning = input("Enter 1 to use alpha beta pruning, else anything else\n")

    Board = [[" ", " ", " "],
             [" ", " ", " "],
             [" ", " ", " "]]

    count = []

    won = False

    while len(get_empty_places(Board)) > 0:

        print_board(Board)
        Check = is_done(Board)
        if Check[0]:
            won = True
            print(Check[1], " Won")
            break
        t = tuple(map(int, input("Enter Location: ").split(',')))
        if t in get_empty_places(Board):
            count = []
            Board[t[0]][t[1]] = "O"
            chosenLocation = minimax(Board, True, 0, -1, +1)
            c = chosenLocation[1]
            if c != 0:
                Board[c[0]][c[1]] = "X"
            print("Nodes Checked: ", len(count))
        else:
            print("Occupied!")
    if not won:
        print("Draw")
