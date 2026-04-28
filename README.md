# CMPSC 132 Final Project — Tic-Tac-Toe

Author: Sergio Yacolca

## Project Description

This project is a terminal-based Tic-Tac-Toe game developed in Python. Two players take turns entering row and column positions to place their symbols on the board until one player wins or the game ends in a draw.
The program follows all required specifications, including input validation, prevention of invalid moves, and detection of winning and draw conditions. The board is implemented using a list of lists, and the game logic is organized using functions to ensure clarity and structure.

## Instructions to Run and Play the Program

### Running the Program

1. Make sure Python is installed on your system.
2. Open a terminal in the project folder.
3. Run the following command:

python main.py

No external libraries are required.

### How to Play

1. When the program starts, select a game mode:
   - Classic Mode
   - No-Draw Mode
   - Load Game
2. Choose the board size:
   - 3x3, 4x4, or 5x5
3. Enter player names.
4. Choose symbols for each player (default or emoji).
5. Select who goes first (X, O, or random).
6. On each turn:
   - Enter a row number (for example 0–2 on a 3x3 board)
   - Then enter a column number
   - Your symbol will be placed on the board
7. The game continues until:
   - A player wins (row, column, or diagonal), or
   - The game ends in a draw (Classic Mode only)

## Controls During the Game

At any turn, you can type:
- save - Save the current game
- undo - Undo the last two moves (confirmation required)
- exit - Exit the current game (confirmation required)

During setup menus:
- back - Return to the previous step

## Notes

- The board uses row and column indexing starting at 0.
- Invalid moves (out of range or occupied cells) are rejected.
- Saved games are stored in a JSON file (saves.json) and can be loaded from the main menu.