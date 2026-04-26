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


def main():
    print("Welcome to Tic-Tac-Toe!")

    board = create_board()
    print_board(board)


if __name__ == "__main__":
    main()