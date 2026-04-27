import random
import os

RED = "\033[91m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def cell_str(c):
    if c == "X":
        return RED + "X" + RESET
    if c == "O":
        return CYAN + "O" + RESET
    return " "


def create_board(size=3):
    # Creates an NxN board using a list of lists
    return [[" " for _ in range(size)] for _ in range(size)]


def print_board(board):
    # Displays the board in a clean format
    size = len(board)
    sep = "  +" + ("---+" * size)
    print()
    print("    " + "   ".join(str(c) for c in range(size)))
    print(sep)
    for row in range(size):
        cells = " | ".join(cell_str(board[row][col]) for col in range(size))
        print(f"{row} | " + cells + " |")
        print(sep)
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
            size = len(board)
            row = int(input(f"{names[player]}, enter row (0-{size - 1}): "))
            if row < 0 or row >= size:
                print(f"Row must be between 0 and {size - 1}.")
                continue
            col = int(input(f"{names[player]}, enter column (0-{size - 1}): "))
            if col < 0 or col >= size:
                print(f"Column must be between 0 and {size - 1}.")
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
    # Returns True if player fills any full row, column, or diagonal
    size = len(board)
    for row in range(size):
        if all(board[row][col] == player for col in range(size)):
            return True
    for col in range(size):
        if all(board[row][col] == player for row in range(size)):
            return True
    if all(board[i][i] == player for i in range(size)):
        return True
    if all(board[i][size - 1 - i] == player for i in range(size)):
        return True
    return False


def is_draw(board):
    # A draw happens when every cell is filled
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


def get_player_names():
    while True:
        raw_x = input("Enter name for player X (or 'back'): ").strip()
        if raw_x.lower() == "back":
            return None  # back → size selection
        name_x = raw_x or "Player X"
        while True:
            raw_o = input("Enter name for player O (or 'back'): ").strip()
            if raw_o.lower() == "back":
                break  # back → re-ask player X name
            name_o = raw_o or "Player O"
            if name_o != name_x:
                return {"X": name_x, "O": name_o}
            print(f"'{name_o}' is already taken by Player X. Choose a different name.")


def choose_starter(names):
    # Asks once per session; random uses random.choice to pick X or O
    while True:
        choice = input(f"Who goes first? X ({names['X']}) / O ({names['O']}) / random / back: ").strip().lower()
        if choice == "back":
            return None
        if choice == "x":
            return "X"
        if choice == "o":
            return "O"
        if choice in ("random", "r"):
            starter = random.choice(["X", "O"])
            print(f"{names[starter]} ({starter}) goes first!")
            return starter
        print("Enter 'X', 'O', 'random', or 'back'.")


def print_move_history(history, names):
    print("Move history:")
    for i, (player, row, col) in enumerate(history, 1):
        print(f"  {i}. {names[player]} ({player}): row {row}, col {col}")


def choose_size():
    print()
    print("+------------------------+")
    print("|    SELECT BOARD SIZE   |")
    print("+------------------------+")
    print("|  1. 3x3 (Classic)      |")
    print("|  2. 4x4                |")
    print("|  3. 5x5                |")
    print("|  0. Go Back            |")
    print("+------------------------+")
    while True:
        choice = input("  Size (0-3): ").strip().lower()
        if choice in ("0", "back"):
            return None
        if choice == "1":
            return 3
        if choice == "2":
            return 4
        if choice == "3":
            return 5
        print("  Enter 0 to go back, or 1, 2, or 3.")


def print_scoreboard(scores, names, mode):
    if mode == "nodraw":
        print(f"Score — {names['X']}: {scores['X']}  |  {names['O']}: {scores['O']}  |  Games: {scores['games']}")
    else:
        print(f"Score — {names['X']}: {scores['X']}  |  {names['O']}: {scores['O']}  |  Draws: {scores['draws']}  |  Games: {scores['games']}")


def play_game(scores, names, starter, mode, size):
    # Runs one round starting from starter; updates scores and shows board after each move
    board = create_board(size)
    current_player = starter
    moves = 0
    history = []
    pieces = {"X": [], "O": []}
    mode_label = "No-Draw Mode" if mode == "nodraw" else "Classic Mode"

    while True:
        clear_screen()
        print(f"  Playing: {mode_label}")
        print_board(board)

        row, col = get_move(board, current_player, names)
        board[row][col] = current_player
        moves += 1
        history.append((current_player, row, col))

        if mode == "nodraw":
            pieces[current_player].append((row, col))
            if len(pieces[current_player]) > size:
                old_row, old_col = pieces[current_player].pop(0)
                board[old_row][old_col] = " "
                print(f"  {names[current_player]}'s oldest piece removed from ({old_row},{old_col}).")

        if check_winner(board, current_player):
            clear_screen()
            print(f"  Playing: {mode_label}")
            print_board(board)
            print(GREEN + f"{names[current_player]} ({current_player}) wins in {moves} moves!" + RESET)
            scores[current_player] += 1
            scores["games"] += 1
            break

        if mode == "classic" and is_draw(board):
            clear_screen()
            print(f"  Playing: {mode_label}")
            print_board(board)
            print(YELLOW + "The game is a draw!" + RESET)
            scores["draws"] += 1
            scores["games"] += 1
            break

        current_player = switch_player(current_player)

    print_move_history(history, names)
    print_scoreboard(scores, names, mode)


def play_again_prompt():
    # Returns True only if the player explicitly enters 'y'
    while True:
        again = input("Play again? (y/n): ").strip().lower()
        if again in ("y", "yes", "ye", "ya", "yep", "yeah", "yeh"):
            return True
        if again in ("n", "no", "nope", "na", "nah"):
            return False
        print("Please enter 'y' or 'n'.")


def show_main_menu():
    clear_screen()
    print()
    print("+------------------------+")
    print("|     TIC-TAC-TOE        |")
    print("+------------------------+")
    print("|  1. Classic Mode       |")
    print("|  2. No-Draw Mode       |")
    print("|  3. Game Rules         |")
    print("|  4. Exit               |")
    print("+------------------------+")
    while True:
        choice = input("  Option (1-4): ").strip()
        if choice in ("1", "2", "3", "4"):
            return choice
        print("  Enter 1, 2, 3, or 4.")


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

        if choice == "3":
            show_game_rules()
            continue
        if choice == "4":
            print("Thanks for playing!")
            break

        mode = "classic" if choice == "1" else "nodraw"

        # Step-based setup: each 'back' goes to the previous step
        step = "size"
        size = names = starter = None
        while True:
            if step == "size":
                size = choose_size()
                if size is None:
                    break  # back at size → return to main menu
                step = "names"
            elif step == "names":
                names = get_player_names()
                step = "starter" if names is not None else "size"
            elif step == "starter":
                starter = choose_starter(names)
                if starter is None:
                    step = "names"
                else:
                    step = "play"
                    break

        if step != "play":
            continue

        # Dictionary to track wins for each player across multiple rounds
        scores = {"X": 0, "O": 0, "draws": 0, "games": 0}

        while True:
            play_game(scores, names, starter, mode, size)

            if not play_again_prompt():
                break
            starter = switch_player(starter)

        print("\nFinal Scoreboard:")
        print_scoreboard(scores, names, mode)
        if scores["X"] > scores["O"]:
            print(GREEN + f"Overall winner: {names['X']} (X)!" + RESET)
        elif scores["O"] > scores["X"]:
            print(GREEN + f"Overall winner: {names['O']} (O)!" + RESET)
        else:
            print(YELLOW + "Overall result: Tied!" + RESET)


if __name__ == "__main__":
    main()
