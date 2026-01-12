#TODO: add openGL graphics//pygame

import pygame
import numpy as np
from numpy import zeros, rot90, array
from random import randint, random

#reimplementing our stuff from project.py in Object Style
class BoardObj:
    def __init__(self):
        self.board = zeros((4,4), dtype = int)
        self.fill_cell()
        self.fill_cell()
        print(self.board)

    def fill_cell(self):
        i, j = (self.board == 0).nonzero()   #other note; we're looking at all the zeros here

        if i.size != 0:
            rand_index = randint(0, i.size - 1)
            self.board[i[rand_index], j[rand_index]] = 2 * ((random() > 0.9) + 1)

    def move_left(self, col):
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

    def move(self, direction):
        #0 left; 1 up; 2 right; 3 down
        new_board = rot90(self.board, direction).copy()  #need call by val
        for i in range(4):
            new_board[i] = self.move_left(new_board[i])
        self.board = rot90(new_board, -1 * direction)

    def print_board(self):
        print(self.board)

#Dummy till we get it working,
def game_window():
    #initializations
    pygame.init()

    WIDTH = 800
    HEIGHT = 800
    window = pygame.display.set_mode((WIDTH, HEIGHT))

    pygame.display.set_caption("2048 pygame prototype")

    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)

    run = True

    current_game = BoardObj()

    #event loop
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                keydown_handler(event, current_game)
                print(f"Keypress : {event.key}")

        window.fill(WHITE)

        #events happen here TODO

        pygame.display.flip()

    pygame.quit()

#handles events for keydown; passes to WASD_handler, R_handler, Q_handler
def keydown_handler(event, board_obj):
    if event in (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d):     #up
        DIRECTIONS = {pygame.K_a : 0,
                      pygame.K_w : 1,
                      pygame.K_d : 2,
                      pygame.K_s : 3}

        old_board = board_obj.board.copy()
        board_obj.move(DIRECTIONS[event])

        if not np.array_equal(old_board, board_obj.board):
            board_obj.fill_cell()
    elif event == pygame.K_q:   #quit
        pass
    elif event == pygame.K_r:   #reset
        pass
    else:
        pass
    print("called keydown_handler")



def WASD_handler(event, board):
    pass

def R_handler(event, board):
    pass

def Q_handler(event, board):
    pass
