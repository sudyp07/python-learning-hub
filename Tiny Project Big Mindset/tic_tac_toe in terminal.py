# Tic Tac Toe Game with Computer AI
# Player X is human, Player O is computer

import random

# Initialize the board as a list of 9 spaces
board = [' '] * 9


# Function to display the board
def display_board():
    print(' ' + board[0] + ' | ' + board[1] + ' | ' + board[2])
    print('-----------')
    print(' ' + board[3] + ' | ' + board[4] + ' | ' + board[5])
    print('-----------')
    print(' ' + board[6] + ' | ' + board[7] + ' | ' + board[8])


# Function to check if a player has won
def check_winner(player):
    # All possible winning combinations (rows, columns, diagonals)
    win_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
        [0, 4, 8], [2, 4, 6]  # diagonals
    ]

    for combo in win_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] == player:
            return True
    return False


# Function to check if the board is full (tie game)
def is_board_full():
    return ' ' not in board


# Function to get a valid move from human player
def get_human_move():
    while True:
        try:
            move = int(input("Your turn (enter position 1-9): ")) - 1
            if 0 <= move <= 8 and board[move] == ' ':
                return move
            else:
                print("Invalid move. Position is taken or out of range.")
        except ValueError:
            print("Please enter a number between 1 and 9.")


# Computer AI - tries to win, block, or make a random move
def get_computer_move():
    # Check if computer can win in the next move
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'O'
            if check_winner('O'):
                board[i] = ' '  # Reset before returning
                return i
            board[i] = ' '  # Reset

    # Check if human can win in the next move and block them
    for i in range(9):
        if board[i] == ' ':
            board[i] = 'X'
            if check_winner('X'):
                board[i] = ' '  # Reset before returning
                return i
            board[i] = ' '  # Reset

    # Take center if available
    if board[4] == ' ':
        return 4

    # Take corners if available
    corners = [0, 2, 6, 8]
    available_corners = [c for c in corners if board[c] == ' ']
    if available_corners:
        return random.choice(available_corners)

    # Take any remaining empty space
    available_moves = [i for i in range(9) if board[i] == ' ']
    if available_moves:
        return random.choice(available_moves)

    return -1  # No moves available (should not happen)


# Main game loop
def play_game():
    print("Welcome to Tic Tac Toe!")
    print("You are X, Computer is O")
    print("Positions are numbered 1-9 from left to right, top to bottom")
    print()

    while True:
        display_board()

        # Human player's turn (X)
        move = get_human_move()
        board[move] = 'X'

        # Check if human wins
        if check_winner('X'):
            display_board()
            print("Congratulations! You win!")
            break

        # Check for tie after human move
        if is_board_full():
            display_board()
            print("It's a tie!")
            break

        # Computer player's turn (O)
        print("Computer is thinking...")
        move = get_computer_move()
        board[move] = 'O'
        print(f"Computer placed at position {move + 1}")

        # Check if computer wins
        if check_winner('O'):
            display_board()
            print("Computer wins! Better luck next time.")
            break

        # Check for tie after computer move
        if is_board_full():
            display_board()
            print("It's a tie!")
            break


# Start the game
if __name__ == "__main__":
    play_game()