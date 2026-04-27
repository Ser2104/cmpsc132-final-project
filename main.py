import random


def create_board():
    # Creates a 3x3 board using a list of lists
    return [[" " for _ in range(3)] for _ in range(3)]


def print_board(board):
    # Displays the board in a clean format
    print()
    print("    0   1   2")
    print("  +---+---+---+")
    for row in range(3):
        print(f"{row} | " + board[row][0] + " | " + board[row][1] + " | " + board[row][2] + " |")
        print("  +---+---+---+")
    print()


def print_reference_board():
    # Displays a coordinate guide so players know which (row, col) to enter
    print("Coordinates: row = top to bottom (0-2), column = left to right (0-2)")
    print()
    print("          col 0   col 1   col 2")
    print("row 0     (0,0)   (0,1)   (0,2)")
    print("row 1     (1,0)   (1,1)   (1,2)")
    print("row 2     (2,0)   (2,1)   (2,2)")
    print()


def get_move(board, player, names):
    # Ask for a valid move until input is correct
    while True:
        try:
            row = int(input(f"{names[player]}, enter row (0-2): "))
            if row < 0 or row > 2:
                print("Row must be between 0 and 2.")
                continue
            col = int(input(f"{names[player]}, enter column (0-2): "))
            if col < 0 or col > 2:
                print("Column must be between 0 and 2.")
                continue
            if board[row][col] != " ":
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
    # Returns True if player has three in a row, column, or diagonal
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
    while True:
        name_o = input("Enter name for player O: ").strip() or "Player O"
        if name_o != name_x:
            break
        print(f"'{name_o}' is already taken by Player X. Choose a different name.")
    return {"X": name_x, "O": name_o}


def choose_starter(names):
    # Asks once per session; random uses random.choice to pick X or O
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


def print_move_history(history, names):
    print("Move history:")
    for i, (player, row, col) in enumerate(history, 1):
        print(f"  {i}. {names[player]} ({player}): row {row}, col {col}")


def print_scoreboard(scores, names):
    print(f"Score — {names['X']}: {scores['X']}  |  {names['O']}: {scores['O']}  |  Draws: {scores['draws']}")


def play_game(scores, names, starter):
    # Runs one round starting from starter; updates scores and shows board after each move
    board = create_board()
    current_player = starter
    moves = 0
    history = []

    while True:
        print_board(board)

        row, col = get_move(board, current_player, names)
        board[row][col] = current_player
        moves += 1
        history.append((current_player, row, col))

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

    print_move_history(history, names)
    print_scoreboard(scores, names)


def play_again_prompt():
    # Returns True only if the player explicitly enters 'y'
    while True:
        again = input("Play again? (y/n): ").strip().lower()
        if again in ("y", "n"):
            return again == "y"
        print("Please enter 'y' or 'n'.")


def show_main_menu():
    print()
    print("+----------------------+")
    print("|    TIC-TAC-TOE       |")
    print("+----------------------+")
    print("|  1. New Game         |")
    print("|  2. Game Rules       |")
    print("|  3. Exit             |")
    print("+----------------------+")
    while True:
        choice = input("  Option (1-3): ").strip()
        if choice in ("1", "2", "3"):
            return choice
        print("  Enter 1, 2, or 3.")


def show_game_rules():
    print("\n--- Game Rules / Controls ---")
    print("Players alternate placing X and O on the board.")
    print("First to get three in a row (row, column, or diagonal) wins.")
    print("If all 9 squares fill with no winner, it is a draw.")
    print()
    print_reference_board()
    input("Press Enter to return to the menu...")


def main():
    print("Welcome to Tic-Tac-Toe!")

    while True:
        choice = show_main_menu()

        if choice == "2":
            show_game_rules()
            continue
        if choice == "3":
            print("Thanks for playing!")
            break

        names = get_player_names()
        starter = choose_starter(names)

        # Dictionary to track wins for each player across multiple rounds
        scores = {"X": 0, "O": 0, "draws": 0}

        while True:
            play_game(scores, names, starter)

            if not play_again_prompt():
                break
            starter = switch_player(starter)

        print("\nFinal Scoreboard:")
        print_scoreboard(scores, names)


if __name__ == "__main__":
    main()
