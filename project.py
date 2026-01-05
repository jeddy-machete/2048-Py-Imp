#TODO: 1/3/26 frontend; IDK how.  Lets cross that bridge after a minute.
#Flask is the most popular lightweight web framework. It gives you more control than Streamlit but requires learning some HTML. It's versatile and widely used for everything from simple sites to APIs.
#TODO: add "README.md" file @ root of project

import numpy as np
from numpy import zeros

#structure

#board global vars
#board methods
    #random filling
    #moving

#driver loop; see todo above


#####################################
#global vars
game_board = zeros((4,4), dtype = int)
game_over = False

#####################################
#Board Set procedures
from random import randint, random
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
from numpy import array, zeros
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

from numpy import rot90
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
    if np.any(obj == 0):
        return False
    #check for available merges
    else:
        for i in range(3):
            for j in range(3):
                if (obj[i][j] == obj[i][j+1]
                    or obj[i][j] == obj[i+1][j]):
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
