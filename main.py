import random
import os

RED = "\033[91m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

PRESET_SYMBOLS = ["😂", "❤️", "😭", "🔥", "🤣", "✨", "👍", "😍", "🥰", "😊"]


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def cell_str(c, symbols):
    if c == "X":
        return RED + symbols["X"] + RESET
    if c == "O":
        return CYAN + symbols["O"] + RESET
    return " "


def create_board(size=3):
    # Creates an NxN board using a list of lists
    return [[" " for _ in range(size)] for _ in range(size)]


def _is_wide(sym):
    # Emoji and non-ASCII symbols render as 2 columns in the terminal
    return not (len(sym) == 1 and ord(sym[0]) < 128)


def print_board(board, symbols):
    size = len(board)
    wide = _is_wide(symbols["X"]) or _is_wide(symbols["O"])
    cell_w = 4 if wide else 3

    sep = "  +" + ("-" * cell_w + "+") * size
    print()
    print("    " + (" " * cell_w).join(str(c) for c in range(size)))
    print(sep)
    for row in range(size):
        row_str = f"{row} |"
        for col in range(size):
            c = board[row][col]
            if c != " ":
                sym = symbols[c]
                color = RED if c == "X" else CYAN
                # narrow symbol in a wide-mode board needs an extra space
                extra = " " if wide and not _is_wide(sym) else ""
                row_str += " " + color + sym + RESET + extra + " |"
            else:
                row_str += " " * cell_w + "|"
        print(row_str)
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


def get_move(board, player, names, symbols):
    # Ask for a valid move until input is correct
    while True:
        try:
            size = len(board)
            row = int(input(f"{names[player]} ({symbols[player]}), enter row (0-{size - 1}): "))
            if row < 0 or row >= size:
                print(f"Row must be between 0 and {size - 1}.")
                continue
            col = int(input(f"{names[player]} ({symbols[player]}), enter column (0-{size - 1}): "))
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


def choose_symbol(player_key, player_name, taken_symbol=None):
    print(f"\nChoose symbol for {player_name} ({player_key}):")
    print(f"  1. Keep default ({player_key})")
    print(f"  2. Choose from emoji list")
    print(f"  3. Enter custom symbol")
    print(f"  0. Back")
    while True:
        choice = input("  Option (0-3): ").strip()
        if choice == "0" or choice.lower() == "back":
            return None
        if choice == "1":
            if player_key == taken_symbol:
                print("  That symbol is already taken. Choose another.")
                continue
            return player_key
        if choice == "2":
            print()
            for i, sym in enumerate(PRESET_SYMBOLS, 1):
                print(f"    {i:2}. {sym}")
            print("     0. Back")
            while True:
                sub = input("    Choice (0-10): ").strip()
                if sub == "0" or sub.lower() == "back":
                    break
                if sub.isdigit() and 1 <= int(sub) <= 10:
                    sym = PRESET_SYMBOLS[int(sub) - 1]
                    if sym == taken_symbol:
                        print("    That symbol is already taken. Choose another.")
                        continue
                    return sym
                print("    Enter a number between 0 and 10.")
            continue
        if choice == "3":
            custom = input("  Enter your custom symbol (1 visible character): ").strip()
            if not custom:
                print("  Symbol cannot be empty.")
                continue
            if len(custom) > 3:
                print("  Please enter 1 visible character only.")
                continue
            if custom == taken_symbol:
                print("  That symbol is already taken. Choose another.")
                continue
            return custom
        print("  Enter 0, 1, 2, or 3.")


def choose_symbols(names):
    # Returns {"X": sym, "O": sym} or None to go back
    while True:
        sym_x = choose_symbol("X", names["X"])
        if sym_x is None:
            return None
        while True:
            sym_o = choose_symbol("O", names["O"], taken_symbol=sym_x)
            if sym_o is None:
                break  # back → re-ask X's symbol
            return {"X": sym_x, "O": sym_o}



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


def choose_starter(names, symbols):
    # Asks once per session; random uses random.choice to pick X or O
    while True:
        choice = input(
            f"Who goes first? X ({names['X']} {symbols['X']}) / O ({names['O']} {symbols['O']}) / random / back: "
        ).strip().lower()
        if choice == "back":
            return None
        if choice == "x":
            return "X"
        if choice == "o":
            return "O"
        if choice in ("random", "r"):
            starter = random.choice(["X", "O"])
            print(f"{names[starter]} ({symbols[starter]}) goes first!")
            return starter
        print("Enter 'X', 'O', 'random', or 'back'.")


def print_move_history(history, names, symbols):
    print("Move history:")
    for i, (player, row, col) in enumerate(history, 1):
        print(f"  {i}. {names[player]} ({symbols[player]}): row {row}, col {col}")


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


def print_scoreboard(scores, names, symbols, mode):
    x_label = f"{names['X']} ({symbols['X']})"
    o_label = f"{names['O']} ({symbols['O']})"
    if mode == "nodraw":
        print(f"Score — {x_label}: {scores['X']}  |  {o_label}: {scores['O']}  |  Games: {scores['games']}")
    else:
        print(f"Score — {x_label}: {scores['X']}  |  {o_label}: {scores['O']}  |  Draws: {scores['draws']}  |  Games: {scores['games']}")


def play_game(scores, names, symbols, starter, mode, size):
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
        print_board(board, symbols)

        row, col = get_move(board, current_player, names, symbols)
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
            print_board(board, symbols)
            print(GREEN + f"{names[current_player]} ({symbols[current_player]}) wins in {moves} moves!" + RESET)
            scores[current_player] += 1
            scores["games"] += 1
            break

        if mode == "classic" and is_draw(board):
            clear_screen()
            print(f"  Playing: {mode_label}")
            print_board(board, symbols)
            print(YELLOW + "The game is a draw!" + RESET)
            scores["draws"] += 1
            scores["games"] += 1
            break

        current_player = switch_player(current_player)

    print_move_history(history, names, symbols)
    print_scoreboard(scores, names, symbols, mode)


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
    print("Players alternate placing their symbol on the board.")
    print("First to get three in a row (row, column, or diagonal) wins.")
    print("If all squares fill with no winner, it is a draw (Classic Mode).")
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
        size = names = symbols = starter = None
        while True:
            if step == "size":
                size = choose_size()
                if size is None:
                    break  # back at size → return to main menu
                step = "names"
            elif step == "names":
                names = get_player_names()
                step = "symbols" if names is not None else "size"
            elif step == "symbols":
                symbols = choose_symbols(names)
                step = "starter" if symbols is not None else "names"
            elif step == "starter":
                starter = choose_starter(names, symbols)
                if starter is None:
                    step = "symbols"
                else:
                    step = "play"
                    break

        if step != "play":
            continue

        # Dictionary to track wins for each player across multiple rounds
        scores = {"X": 0, "O": 0, "draws": 0, "games": 0}

        while True:
            play_game(scores, names, symbols, starter, mode, size)

            if not play_again_prompt():
                break
            starter = switch_player(starter)

        print("\nFinal Scoreboard:")
        print_scoreboard(scores, names, symbols, mode)
        if scores["X"] > scores["O"]:
            print(GREEN + f"Overall winner: {names['X']} ({symbols['X']})!" + RESET)
        elif scores["O"] > scores["X"]:
            print(GREEN + f"Overall winner: {names['O']} ({symbols['O']})!" + RESET)
        else:
            print(YELLOW + "Overall result: Tied!" + RESET)


if __name__ == "__main__":
    main()
