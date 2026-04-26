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


def main():
    print("Welcome to Tic-Tac-Toe!")

    board = create_board()
    print_board(board)


if __name__ == "__main__":
    main()