import random
import os
import json

RED = "\033[91m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

PRESET_SYMBOLS = ["😂", "❤️", "😭", "🔥", "🤣", "✨", "👍", "😍", "🥰", "😊"]
SAVE_FILE = "savegame.json"
WIN_LENGTH = {3: 3, 4: 3, 5: 4}


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


def print_reference_board(size):
    print(f"  Coordinates ({size}x{size}): row top→bottom (0-{size-1}), col left→right (0-{size-1})")
    print()
    header = "         " + "   ".join(f"col {c}" for c in range(size))
    print(header)
    for r in range(size):
        row_str = f"  row {r}   " + "   ".join(f"({r},{c})" for c in range(size))
        print(row_str)
    print()


def get_move(board, player, names, symbols):
    # Ask for a valid move; 'save' or 'exit' are accepted at the row prompt
    while True:
        try:
            size = len(board)
            raw = input(
                f"{names[player]} ({symbols[player]}), enter row (0-{size - 1}), 'save', or 'exit': "
            ).strip().lower()
            if raw == "save":
                return "save", -1
            if raw == "exit":
                return "exit", -1
            row = int(raw)
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
            print("Invalid input. Enter numbers only, 'save', or 'exit'.")


def switch_player(current_player):
    # Switch between X and O
    if current_player == "X":
        return "O"
    return "X"


def check_winner(board, player, win_length):
    size = len(board)
    # Rows
    for r in range(size):
        for c in range(size - win_length + 1):
            if all(board[r][c + k] == player for k in range(win_length)):
                return True
    # Columns
    for c in range(size):
        for r in range(size - win_length + 1):
            if all(board[r + k][c] == player for k in range(win_length)):
                return True
    # Diagonal top-left → bottom-right
    for r in range(size - win_length + 1):
        for c in range(size - win_length + 1):
            if all(board[r + k][c + k] == player for k in range(win_length)):
                return True
    # Diagonal top-right → bottom-left
    for r in range(size - win_length + 1):
        for c in range(win_length - 1, size):
            if all(board[r + k][c - k] == player for k in range(win_length)):
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



def save_game(board, current_player, names, symbols, scores, mode, size, history, pieces, starter):
    data = {
        "board": board,
        "current_player": current_player,
        "names": names,
        "symbols": symbols,
        "scores": scores,
        "mode": mode,
        "size": size,
        "history": [list(h) for h in history],
        "pieces": {k: [list(p) for p in v] for k, v in pieces.items()},
        "starter": starter,
    }
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(GREEN + f"  Game saved to {SAVE_FILE}." + RESET)


def load_game():
    if not os.path.exists(SAVE_FILE):
        print(YELLOW + "  No saved game found." + RESET)
        return None
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        data["history"] = [tuple(h) for h in data["history"]]
        data["pieces"] = {k: [tuple(p) for p in v] for k, v in data["pieces"].items()}
        return data
    except (json.JSONDecodeError, KeyError) as e:
        print(RED + f"  Failed to load save file: {e}" + RESET)
        return None


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


def play_game(scores, names, symbols, starter, mode, size, resume_state=None):
    win_length = WIN_LENGTH[size]
    if resume_state:
        board = resume_state["board"]
        current_player = resume_state["current_player"]
        history = list(resume_state["history"])
        pieces = {k: list(v) for k, v in resume_state["pieces"].items()}
        moves = len(history)
    else:
        board = create_board(size)
        current_player = starter
        moves = 0
        history = []
        pieces = {"X": [], "O": []}

    mode_label = "No-Draw Mode" if mode == "nodraw" else "Classic Mode"

    while True:
        clear_screen()
        print(f"  {mode_label}  |  {size}x{size}  |  Win: {win_length} in a row")
        print_board(board, symbols)

        result = get_move(board, current_player, names, symbols)
        if result[0] == "save":
            save_game(board, current_player, names, symbols, scores, mode, size, history, pieces, starter)
            input("  Press Enter to continue...")
            continue
        if result[0] == "exit":
            confirm = input("  You are leaving the game. Type 'confirm' to exit: ").strip().lower()
            if confirm == "confirm":
                print(YELLOW + "  Exiting game..." + RESET)
                return False
            continue

        row, col = result
        board[row][col] = current_player
        moves += 1
        history.append((current_player, row, col))

        if mode == "nodraw":
            pieces[current_player].append((row, col))
            if len(pieces[current_player]) > size:
                old_row, old_col = pieces[current_player].pop(0)
                board[old_row][old_col] = " "
                print(f"  {names[current_player]}'s oldest piece removed from ({old_row},{old_col}).")

        if check_winner(board, current_player, win_length):
            clear_screen()
            print(f"  {mode_label}  |  {size}x{size}")
            print_board(board, symbols)
            print(GREEN + f"{names[current_player]} ({symbols[current_player]}) wins in {moves} moves!" + RESET)
            scores[current_player] += 1
            scores["games"] += 1
            break

        if mode == "classic" and is_draw(board):
            clear_screen()
            print(f"  {mode_label}  |  {size}x{size}")
            print_board(board, symbols)
            print(YELLOW + "The game is a draw!" + RESET)
            scores["draws"] += 1
            scores["games"] += 1
            break

        current_player = switch_player(current_player)

    print_move_history(history, names, symbols)
    print_scoreboard(scores, names, symbols, mode)
    return True


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
    X = RED + "X" + RESET
    O = CYAN + "O" + RESET
    print()
    print("+------------------------+")
    print("|     TIC-TAC-TOE        |")
    print("+------------------------+")
    print(f"|    {X} | . | {X}           |")
    print("|   ---+---+---          |")
    print(f"|    . | {O} | .           |")
    print("|   ---+---+---          |")
    print(f"|    {O} | . | {X}           |")
    print("+------------------------+")
    print("|  1. Classic Mode       |")
    print("|  2. No-Draw Mode       |")
    print("|  3. Load Game          |")
    print("|  4. Game Rules         |")
    print("|  5. Exit               |")
    print("+------------------------+")
    while True:
        choice = input("  Option (1-5): ").strip()
        if choice in ("1", "2", "3", "4", "5"):
            return choice
        print("  Enter 1, 2, 3, 4, or 5.")


def show_game_rules():
    print("\n--- Game Rules / Controls ---")
    print("Players alternate placing their symbol on the board.")
    print("Win conditions:  3x3 → 3 in a row  |  4x4 → 3 in a row  |  5x5 → 4 in a row")
    print("Classic Mode: if all squares fill with no winner, it is a draw.")
    print("No-Draw Mode: oldest piece is removed once the piece limit is exceeded.")
    print("During your turn, type 'save' at the row prompt to save the game.")
    print()
    print("--- Coordinate Reference ---")
    for s in (3, 4, 5):
        print_reference_board(s)
    input("Press Enter to return to the menu...")


def main():
    print("Welcome to Tic-Tac-Toe!")

    while True:
        choice = show_main_menu()

        if choice == "3":
            data = load_game()
            if data is None:
                input("  Press Enter to return to the menu...")
                continue
            names = data["names"]
            symbols = data["symbols"]
            scores = data["scores"]
            mode = data["mode"]
            size = data["size"]
            starter = data["starter"]
            resume_state = {
                "board": data["board"],
                "current_player": data["current_player"],
                "history": data["history"],
                "pieces": data["pieces"],
            }
            print(GREEN + "  Save loaded!" + RESET)
            print(f"  {names['X']} ({symbols['X']}) vs {names['O']} ({symbols['O']})")
            input("  Press Enter to continue...")
            if not play_game(scores, names, symbols, starter, mode, size, resume_state=resume_state):
                continue
            while play_again_prompt():
                starter = switch_player(starter)
                if not play_game(scores, names, symbols, starter, mode, size):
                    break
            print("\nFinal Scoreboard:")
            print_scoreboard(scores, names, symbols, mode)
            continue

        if choice == "4":
            show_game_rules()
            continue
        if choice == "5":
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
            if not play_game(scores, names, symbols, starter, mode, size):
                break
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
