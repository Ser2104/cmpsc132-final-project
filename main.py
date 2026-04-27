import random


def create_board():
    # Creates a 3x3 board using a list of lists
    return [[" " for _ in range(3)] for _ in range(3)]


def print_board(board):
    # Displays the board in a clean format
    print()
    for row in range(3):
        print(" " + board[row][0] + " | " + board[row][1] + " | " + board[row][2])
        if row < 2:
            print("---+---+---")
    print()


def print_reference_board():
    # Displays a coordinate guide so players know which (row, col) to enter
    print("Board positions (row, col):")
    print()
    print(" (0,0) | (0,1) | (0,2)")
    print("-------+-------+-------")
    print(" (1,0) | (1,1) | (1,2)")
    print("-------+-------+-------")
    print(" (2,0) | (2,1) | (2,2)")
    print()


def get_move(board, player, names):
    # Ask for a valid move until input is correct
    while True:
        try:
            row = int(input(f"{names[player]}, enter row (0-2): "))
            col = int(input(f"{names[player]}, enter column (0-2): "))

            if row < 0 or row > 2 or col < 0 or col > 2:
                print("Invalid move. Try again.")
            elif board[row][col] != " ":
                print("That spot is already taken. Try again.")
            else:
                return row, col

        except ValueError:
            print("Invalid input. Enter numbers only.")


def switch_player(current_player):
    # Switch between X and O
    if current_player == "X":
        return "O"
    return "X"


def check_winner(board, player):
    # Check rows
    for row in range(3):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True

    # Check columns
    for col in range(3):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True

    # Check diagonals
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True

    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True

    return False


def is_draw(board):
    # A draw happens when every cell is filled
    for row in range(3):
        for col in range(3):
            if board[row][col] == " ":
                return False
    return True


def get_player_names():
    name_x = input("Enter name for player X: ").strip() or "Player X"
    name_o = input("Enter name for player O: ").strip() or "Player O"
    return {"X": name_x, "O": name_o}


def choose_starter(names):
    while True:
        choice = input(f"Who goes first? X ({names['X']}) / O ({names['O']}) / random: ").strip().lower()
        if choice == "x":
            return "X"
        if choice == "o":
            return "O"
        if choice == "random":
            starter = random.choice(["X", "O"])
            print(f"{names[starter]} ({starter}) goes first!")
            return starter
        print("Enter 'X', 'O', or 'random'.")


def play_game(scores, names, starter):
    # Runs a single game and updates the scores dictionary when a player wins
    board = create_board()
    current_player = starter
    moves = 0

    while True:
        print_board(board)

        row, col = get_move(board, current_player, names)
        board[row][col] = current_player
        moves += 1

        if check_winner(board, current_player):
            print_board(board)
            print(f"{names[current_player]} ({current_player}) wins in {moves} moves!")
            scores[current_player] += 1
            break

        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            scores["draws"] += 1
            break

        current_player = switch_player(current_player)

    print(f"Score — {names['X']}: {scores['X']}  |  {names['O']}: {scores['O']}  |  Draws: {scores['draws']}")


def main():
    print("Welcome to Tic-Tac-Toe!")
    print("Players take turns entering row and column numbers from 0 to 2.")
    print("The first player to get three in a row wins.")
    print()
    print_reference_board()

    names = get_player_names()
    starter = choose_starter(names)

    # Dictionary to track wins for each player across multiple rounds
    scores = {"X": 0, "O": 0, "draws": 0}

    while True:
        play_game(scores, names, starter)
        starter = switch_player(starter)

        while True:
            again = input("Play again? (y/n): ").strip().lower()
            if again in ("y", "n"):
                break
            print("Please enter 'y' or 'n'.")
        if again != "y":
            break

    print(f"\nFinal scores — {names['X']}: {scores['X']}  |  {names['O']}: {scores['O']}  |  Draws: {scores['draws']}")
    print("Thanks for playing!")


if __name__ == "__main__":
    main()
