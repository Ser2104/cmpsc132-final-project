# CMPSC 132 - Final Project
# Tic-Tac-Toe Game (2-Player, Terminal-Based)
# Author: Sergio Yacolca


import random
import os
import json

# ANSI escape codes for terminal colors and text formatting
RED = "\033[91m"
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
RESET = "\033[0m"

PRESET_SYMBOLS = ["😂", "❤️", "😭", "🔥", "🤣", "✨", "👍", "😍", "🥰", "😊"]
SAVE_FILE = "saves.json"
WIN_LENGTH = {3: 3, 4: 3, 5: 4}


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def create_board(size=3):
    # Creates an NxN board using a list of lists
    return [[" " for _ in range(size)] for _ in range(size)]


def _is_wide(sym):
    # Emoji and non-ASCII symbols render as 2 columns in the terminal
    return not (len(sym) == 1 and ord(sym[0]) < 128)


# Displays the board with dynamic size and supports colored and emoji symbols
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


# Displays a coordinate guide to help players understand row/column positions
def print_reference_board(size):
    print(f"  Coordinates ({size}x{size}): row top→bottom (0-{size-1}), col left→right (0-{size-1})")
    print()
    header = "         " + "   ".join(f"col {c}" for c in range(size))
    print(header)
    for r in range(size):
        row_str = f"  row {r}   " + "   ".join(f"({r},{c})" for c in range(size))
        print(row_str)
    print()


# Handles one complete turn input for the current player.
# Validates row and column values, rejects occupied cells, and recognizes special commands such as save, undo, and exit.
def get_move(board, player, names, symbols):
    while True:
        try:
            size = len(board)
            raw = input(
                f"  {names[player]} ({symbols[player]})  row (0-{size-1}) / save / undo / exit: "
            ).strip().lower()
            if raw == "save":
                return "save", -1
            if raw == "exit":
                return "exit", -1
            if raw == "undo":
                return "undo", -1
            row = int(raw)
            if row < 0 or row >= size:
                print(f"  Row must be 0-{size - 1}.")
                continue
            col_raw = input(
                f"  {names[player]} ({symbols[player]})  col (0-{size-1}) / back to re-enter row: "
            ).strip().lower()
            if col_raw == "back":
                continue
            col = int(col_raw)
            if col < 0 or col >= size:
                print(f"  Col must be 0-{size - 1}.")
                continue
            if board[row][col] != " ":
                print("  That spot is already taken. Try again.")
            else:
                return row, col

        except ValueError:
            print("  Enter a number, 'save', 'undo', or 'exit'.")


# Alternates the current player after each valid turn
def switch_player(current_player):
    if current_player == "X":
        return "O"
    return "X"


# Checks all possible win sequences by sliding a window of size win_length (rows, columns, and diagonals)
# The win_length parameter enables functionality for all board sizes (3x3, 4x4, and 5x5)
def check_winner(board, player, win_length):
    size = len(board)
    # Rows
    for r in range(size):
        # size - win_length + 1 limits the start so the window always fits in the board
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


# Returns True if every cell on the board is filled (no empty spaces left)
def is_draw(board):
    # A draw happens when every cell is filled
    for row in board:
        for cell in row:
            if cell == " ":
                return False
    return True


# Reconstructs the board based on the move history.
# In No-Draw mode, enforces the piece limit by removing the oldest piece.
def rebuild_from_history(history, size, mode, win_length):
    board = create_board(size)
    pieces = {"X": [], "O": []}
    for player, r, c in history:
        board[r][c] = player
        if mode == "nodraw":
            pieces[player].append((r, c))
            if len(pieces[player]) > win_length:
                # pop(0) removes the oldest piece (first placed)
                old_r, old_c = pieces[player].pop(0)
                board[old_r][old_c] = " "
    return board, pieces


# Asks one player to pick a symbol. Keep the default or choose from the emoji list
def choose_symbol(player_key, player_name, taken_symbol=None):
    print(f"\nChoose symbol for {player_name} ({player_key}):")
    print(f"  1. Keep default ({player_key})")
    print(f"  2. Choose from emoji list")
    print(f"  0. Back")
    while True:
        choice = input("  Option (0-2): ").strip()
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
        print("  Enter 0, 1, or 2.")


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


# Loads saved games from JSON file. Returns empty dictionary if file is missing or invalid
def _load_saves():
    if not os.path.exists(SAVE_FILE):
        return {}
    try:
        with open(SAVE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, KeyError, OSError):
        # file exists but is corrupted or has the wrong structure
        return {}


# Writes the full saves dictionary to the JSON file, overwriting the previous content
def _write_saves(saves):
    with open(SAVE_FILE, "w", encoding="utf-8") as f:
        json.dump(saves, f, ensure_ascii=False, indent=2)


# Displays all saved games in a formatted table
def _saves_table(saves):
    if not saves:
        print("  (no saves yet)")
        return
    print(f"  {'#':<4} {'Name':<16} {'Players':<26} {'Board':<6} Mode")
    print("  " + "-" * 62)
    for i, (slot, d) in enumerate(saves.items(), 1):
        n = d["names"]
        players = f"{n['X']} ({d['symbols']['X']}) vs {n['O']} ({d['symbols']['O']})"
        board_lbl = f"{d['size']}x{d['size']}"
        mode_lbl = "Classic" if d["mode"] == "classic" else "No-Draw"
        print(f"  {i:<4} {slot:<16} {players:<26} {board_lbl:<6} {mode_lbl}")


# Saves the current game state into a named slot in the JSON file
def save_game(board, current_player, names, symbols, scores, mode, size, history, pieces, starter):
    saves = _load_saves()
    print()
    print("+--------------------------------+")
    print("|           SAVE GAME            |")
    print("+--------------------------------+")
    _saves_table(saves)
    print()
    slot = input("  Save name (or 'back'): ").strip()
    if not slot or slot.lower() == "back":
        print("  Save cancelled.")
        return
    if slot in saves:
        ow = input(f"  '{slot}' already exists. Overwrite? (y/n): ").strip().lower()
        if ow not in ("y", "yes"):
            print("  Save cancelled.")
            return
    # JSON cannot store tuples, so history and pieces are converted to lists
    saves[slot] = {
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
    _write_saves(saves)
    print(GREEN + f"  Saved as '{slot}'." + RESET)


# Shows all saved games in a table and lets the player choose one to continue from
def load_game():
    saves = _load_saves()
    if not saves:
        print(YELLOW + "  No saved games found." + RESET)
        return None
    print()
    print("+--------------------------------+")
    print("|           LOAD GAME            |")
    print("+--------------------------------+")
    _saves_table(saves)
    print()
    slots = list(saves.keys())
    while True:
        raw = input("  Slot number or name (or 'back'): ").strip()
        if raw.lower() == "back" or raw == "0":
            return None
        if raw.isdigit() and 1 <= int(raw) <= len(slots):
            slot = slots[int(raw) - 1]
        elif raw in saves:
            slot = raw
        else:
            print(f"  Enter a number 1-{len(slots)} or an exact save name.")
            continue
        data = saves[slot]
        # JSON loaded lists back. Convert them to tuples so the rest of the code works normally
        data["history"] = [tuple(h) for h in data["history"]]
        data["pieces"] = {k: [tuple(p) for p in v] for k, v in data["pieces"].items()}
        return data


# Asks both players to enter their names and makes sure they are not the same
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


# Prints the full list of moves made during the game, in order
def print_move_history(history, names, symbols):
    print("Move history:")
    for i, (player, row, col) in enumerate(history, 1):
        print(f"  {i}. {names[player]} ({symbols[player]}): row {row}, col {col}")


# Allows the user to select the board size or go back to the previous menu
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


# Shows the current score for both players, including draws and total games played
def print_scoreboard(scores, names, symbols, mode):
    x_label = f"{names['X']} ({symbols['X']})"
    o_label = f"{names['O']} ({symbols['O']})"
    if mode == "nodraw":
        print(f"Score — {x_label}: {scores['X']}  |  {o_label}: {scores['O']}  |  Games: {scores['games']}")
    else:
        print(f"Score — {x_label}: {scores['X']}  |  {o_label}: {scores['O']}  |  Draws: {scores['draws']}  |  Games: {scores['games']}")


# Handles the undo command. Confirms with the player, pops moves from history, and returns the new game state
# Returns (board, pieces, current_player, moves) if confirmed or None if cancelled
def _do_undo(history, size, mode, win_length, starter, names, symbols):
    if not history:
        print("  Nothing to undo.")
        input("  Press Enter to continue...")
        return None
    count = min(2, len(history))
    confirm = input(f"  Undo last {count} move(s)? Type 'confirm' to proceed: ").strip().lower()
    if confirm != "confirm":
        print("  Undo cancelled.")
        input("  Press Enter to continue...")
        return None
    print()
    print("  +-------- UNDO STACK --------+")
    for _ in range(count):
        p, r, c = history.pop()
        print(f"  |  pop  {names[p]:<12} ({symbols[p]}) at ({r},{c})")
    print("  +----------------------------+")
    board, pieces = rebuild_from_history(history, size, mode, win_length)
    # if history is empty after undo, the starter goes first again
    current_player = switch_player(history[-1][0]) if history else starter
    print(f"  {count} move(s) undone.")
    input("  Press Enter to continue...")
    return board, pieces, current_player, len(history)


# Main game loop. Controls turns, board updates, win/draw detection, and save/undo/exit commands.
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
            print("  Exit cancelled.")
            input("  Press Enter to continue...")
            continue

        if result[0] == "undo":
            undo_result = _do_undo(history, size, mode, win_length, starter, names, symbols)
            if undo_result:
                board, pieces, current_player, moves = undo_result
            continue

        row, col = result
        board[row][col] = current_player
        moves += 1
        history.append((current_player, row, col))

        # In No-Draw mode, each player has a limit on active pieces. If the limit is exceeded, that player's oldest piece is removed
        if mode == "nodraw":
            pieces[current_player].append((row, col))
            if len(pieces[current_player]) > win_length:
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


# Asks the players if they want another round. Returns True for yes, False for no.
def play_again_prompt():
    # Returns True for yes responses and False for no responses
    while True:
        again = input("Play again? (y/n): ").strip().lower()
        if again in ("y", "yes", "ye", "ya", "yep", "yeah", "yeh"):
            return True
        if again in ("n", "no", "nope", "na", "nah"):
            return False
        print("Please enter 'y' or 'n'.")


# Clears the screen and shows the main menu with a decorative board and all available options
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


# Prints the game rules, win conditions, available commands, and coordinate reference for each board size
def show_game_rules():
    print("\n--- Game Rules / Controls ---")
    print("Players alternate placing their symbol on the board.")
    print("Win conditions:  3x3 → 3 in a row  |  4x4 → 3 in a row  |  5x5 → 4 in a row")
    print("Classic Mode: if all squares fill with no winner, it is a draw.")
    print("No-Draw Mode: oldest piece is removed once the piece limit is exceeded.")
    print("Commands at your turn:  'save' → save game  |  'undo' → undo last 2 moves  |  'exit' → return to menu")
    print()
    print("--- Coordinate Reference ---")
    for s in (3, 4, 5):
        print_reference_board(s)
    input("Press Enter to return to the menu...")


# Program entry point. This controls menu navigation and the overall flow.
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
