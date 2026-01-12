#TODO: 1/3/26 frontend; IDK how.  Lets cross that bridge after a minute.
#Flask is the most popular lightweight web framework. It gives you more control than Streamlit but requires learning some HTML. It's versatile and widely used for everything from simple sites to APIs.

import numpy as np
from numpy import zeros, rot90, array
from random import randint, random

#####################################
#game loop

#TODO: get up n running
def game_loop(): # text game loop
    #init
    game_board = zeros((4,4), dtype = int)
    fill_cell(game_board)
    fill_cell(game_board)

    input_map = {'a' : 0, 'w' : 1, 'd' :2, 's' : 3} #WASD controls

    while True:
        if is_game_over(game_board):
            break
        print_board(game_board)
        user_input = input("\nYour Move: ").lower().strip()
        if user_input not in input_map:
            print("Invalid input, use WASD for movement")
            continue

        old_board = game_board.copy()
        game_board = move(game_board, input_map[user_input])

        if not np.array_equal(old_board, game_board):
            fill_cell(game_board)
        else:
            print("Invalid move: no tiles moved")

    print_board(game_board)
    print(f"Final Score: {np.sum(game_board)}")
    user_input = input("\nPress any key to quit:")

#####################################
#Board Set procedures
def fill_cell(board):
    i, j = (board == 0).nonzero()   #other note; we're looking at all the zeros here
    if i.size != 0:
        rand_index = randint(0, i.size - 1)
        board[i[rand_index], j[rand_index]] = 2 * ((random() > 0.9) + 1)
            #Note assignment in last line
                #+ -> 1
                #  -> Random (1, P = 0.1) (0, P = 0.9)
            #Sum is multiplied by 2, producing either a 2 or 4

def reset_board():
    game_board = zeros((4,4), dtype = int)
    game_over = False

#####################################
#Movement procedures
def move_left(col):
    new_col = zeros((4), dtype = col.dtype)
    j = 0
    prev = None
    for i in range(col.size):
        if col[i] != 0:
            if prev == None:  # Changed = to ==
                prev = col[i]   #Allocate
            else:
                if prev == col[i]:
                    new_col[j] = 2 * col[i]
                    j += 1
                    prev = None #De-allocate
                else:
                    new_col[j] = prev
                    j += 1
                    prev = col[i]
    if prev != None:
        new_col[j] = prev
    return new_col

def move(board, direction):
    #0 left; 1 up; 2 right; 3 down
    new_board = rot90(board, direction).copy()  #need call by val
    for i in range(4):
        new_board[i] = move_left(new_board[i])
    return rot90(new_board, -1 * direction)

#####################################
#logic check procedure
def is_game_over(board):
    #check for vacant space
    if np.any(board == 0):
        return False
    #check for available merges
    else:
        for i in range(3):
            for j in range(3):
                if (board[i][j] == board[i][j+1]
                    or board[i][j] == board[i+1][j]):
                    return False
    return True

#####################################
#display procedure
def print_board(board):
    print("\n" + "="*17)
    for row in board:
        print("|", end = "")
        for cell in row:
            print(f"{cell:4}", end = "  ")
        print(" |")
    print("\n" + "="*17)
