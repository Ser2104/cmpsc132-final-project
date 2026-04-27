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

def get_move(board, player):
    # Ask for a valid move until input is correct
    while True:
        try:
            row = int(input(f"Player {player}, enter row (0-2): "))
            col = int(input(f"Player {player}, enter column (0-2): "))

            if row < 0 or row > 2 or col < 0 or col > 2:
                print("Invalid move. Try again.")
            elif board[row][col] != " ":
                print("Spot already taken.")
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

def main():
    print("Welcome to Tic-Tac-Toe!")

    board = create_board()
    current_player = "X"

    while True:
        print_board(board)

        row, col = get_move(board, current_player)
        board[row][col] = current_player

        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break

        if is_draw(board):
            print_board(board)
            print("The game is a draw!")
            break

        current_player = switch_player(current_player)


if __name__ == "__main__":
    main()