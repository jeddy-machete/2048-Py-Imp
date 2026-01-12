#TODO 1/12/26:
#   - colorize our board drawer
#   - add score counter above
#   - add support for UP DOWN LEFT RIGHT (easier, just need to work on WASD_handler)

#   - Need game-over handler

#   - add reset//quit support + prompts
#   - should have a popup window on board!
#       - abstract this to two functions that call prompt(), prompt takes input y/n
#       - if y TRUE
#       - elif n FALSE,
#       - else hold

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
        draw_board(window, current_game, WIDTH, HEIGHT)
        pygame.display.flip()

    pygame.quit()

#TODO implement
def draw_board(window, board_obj, width, height):
    BACKGROUND = (51, 51, 255)
    EMPTY_TILE = (51, 153, 255)

    TILE_COLORS = {0 :  EMPTY_TILE,
                   #TODO actually populate colors ; text color needs to be changed to a choice 'if' when that happens
                   2 : (192, 192, 192),
                   4 : (192, 192, 192),
                   8 : (192, 192, 192),
                   16 : (192, 192, 192),
                   32 : (192, 192, 192),
                   64 : (192, 192, 192),
                   128 : (192, 192, 192),
                   256 : (192, 192, 192),
                   512 : (192, 192, 192),
                   1024 : (192, 192, 192),
                   2048 : (192, 192, 192)}

    #dimension calculations
    padding = 10
    board_size = min(width, height) - (2 * padding)
    gap = 10
    prelim_tile_size = board_size // 4
    final_tile_size = prelim_tile_size - gap

    board_rect = pygame.Rect(padding, padding, board_size, board_size)
    pygame.draw.rect(window, BACKGROUND, board_rect, border_radius = 10)

    for row in range(4):
        for col in range(4):
            #tile pos
            x = padding + col * prelim_tile_size + gap // 2
            y = padding + row * prelim_tile_size + gap // 2

            #tile val
            value = board_obj.board[row][col]

            tile_rect = pygame.Rect(x, y, final_tile_size, final_tile_size)
            color = TILE_COLORS.get(value, TILE_COLORS[2048])
            pygame.draw.rect(window, color, tile_rect, border_radius = 5)

            if value != 0:
                font = pygame.font.Font(None, 48)
                text_color = (0, 0, 0)  #TODO : add to choice if, see hash table above

                text = font.render(str(value), True, text_color)
                text_rect = text.get_rect(center = tile_rect.center)
                window.blit(text, text_rect)


#handles events for keydown; passes to WASD_handler, R_handler, Q_handler
def keydown_handler(event, board_obj):
    print("keydown called")
    if event.key in (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d):     #up
        print("called WASD_handler")
        WASD_handler(event, board_obj)
    #TODO: add functionality
    elif event.key == pygame.K_q:   #quit
        pass
    elif event.key == pygame.K_r:   #reset
        pass
    elif event.key == pygame.K_p:
        print("printing board")
        board_obj.print_board()
    else:
        pass


def WASD_handler(event, board_obj):
    DIRECTIONS = {pygame.K_a : 0,
                  pygame.K_w : 1,
                  pygame.K_d : 2,
                  pygame.K_s : 3}

    old_board = board_obj.board.copy()
    board_obj.move(DIRECTIONS[event.key])

    if not np.array_equal(old_board, board_obj.board):
        board_obj.fill_cell()

def R_handler(event, board):
    pass

def Q_handler(event, board):
    pass
