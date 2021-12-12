import random

board = ["_" for x in range(9)]
win_conditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
]
hu_player = "x"
ai = "o"

print(f"{0} {1} {2}\n{3} {4} {5}\n{6} {7} {8}\n")


def print_board(board):
    print(f"{0} {1} {2}\n{3} {4} {5}\n{6} {7} {8}\n")
    print(
        f"\n{board[0]} {board[1]} {board[2]}\n{board[3]} {board[4]} {board[5]}\n{board[6]} {board[7]} {board[8]}\n--"
    )


def get_legal_moves(board):
    valid_positions = []
    for x in range(9):
        if board[x] == "_":
            valid_positions.append(x)
    return valid_positions


def check_win(board):
    for condition in win_conditions:
        if board[condition[0]] + board[condition[1]] + board[condition[2]] == ai * 3:
            return 10
        elif (
            board[condition[0]] + board[condition[1]] + board[condition[2]]
            == hu_player * 3
        ):
            return -10
    return 0


def get_opponent(current_player):
    if current_player == ai:
        return hu_player
    elif current_player == hu_player:
        return ai


def make_move(board, current_player, position):
    board[position] = current_player
    return board


def minimax_ai(board, current_player):
    best_move = best_score = None

    legal_moves = get_legal_moves(board)

    for legal_move in legal_moves:

        new_board = make_move(board, current_player, legal_move)
        opponet = get_opponent(current_player)

        score = minimax(new_board, opponet)

        board[legal_move] = "_"

        if best_score is None or score > best_score:
            best_score = score
            best_move = legal_move
    return best_move


def minimax(board, current_player):
    legal_moves = get_legal_moves(board)

    if check_win(board) != 0:
        return check_win(board)

    if len(legal_moves) == 0:
        return 0

    scores = []

    for legal_move in legal_moves:
        new_board = make_move(board, current_player, legal_move)
        print_board(new_board)
        opponet = get_opponent(current_player)
        score = minimax(new_board, opponet)
        scores.append(score)
        board[legal_move] = "_"
    if current_player == ai:
        return max(scores)
    else:
        return min(scores)


def player_input(board):
    player_move = input('Type the positin for "o" or 9 to exit: ')
    legal_moves = get_legal_moves(board)
    if int(player_move) not in legal_moves:
        print("Please give a valid input.")
    if player_move in [str(x) for x in range(9)]:
        board[int(player_move)] = hu_player
    elif player_move == "9":
        return
    elif player_move == "restart":
        board = ["_" for x in range(9)]
    best_move = minimax_ai(board, ai)
    if len(legal_moves) == 0:
        board[random.randint(0, 8)] = ai
    else:
        board[best_move] = ai
    print_board(board)
    winner = check_win(board)
    if winner in [10, -10]:
        print("Game Over")
    if len(legal_moves) == 0:
        print("It's a Draw")
    if len(legal_moves) > 0:
        player_input(board)


player_input(board)

# Ok, so for the most part everything works. Thou this can definitelly be worked on. 
# At the moment you can't change the between 'x' and 'o', and there is probably some
# bugs somewhere, but I didn't inted for this to be perfect, just a rough sketch so 
# that it will be easier for me to do it in JS. I will do the polishing there.
