#TODO 1/12/26:
#   - add score counter above
#   - Need game-over handler

#TODO 1/14/26
# want to add
#   - pause interrupt
#   - some sound functionality


import pygame
import numpy as np
from numpy import zeros, rot90, array
from random import randint, random
import sys

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

    def reset_board(self):
        self.board = zeros((4,4), dtype = int)
        self.fill_cell()
        self.fill_cell()

    def print_board(self):
        print(self.board)

##############################3
#Main game driver
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
                keydown_handler(event, window, current_game, WIDTH, HEIGHT)
                #print(f"Keypress : {event.key}")

        window.fill(WHITE)
        draw_board(window, current_game, WIDTH, HEIGHT)
        pygame.display.flip()

    pygame.quit()

##############################################3
def draw_board(window, board_obj, width, height):
    BACKGROUND = (51, 51, 255)
    EMPTY_TILE = (51, 153, 255)

    TILE_COLORS = {0 :  EMPTY_TILE,
                   #TODO actually populate colors ; text color needs to be changed to a choice 'if' when that happens
                   2 : (224, 224, 224),
                   4 : (255, 255, 153),
                   8 : (255, 178, 102),
                   16 : (225, 153, 51),
                   32 : (255, 102, 102),
                   64 : (255, 51, 51),
                   128 : (255, 255, 51),
                   256 : (255, 225, 80),
                   512 : (255, 200, 51),
                   1024 : (240, 200, 51),
                   2048 : (153, 255, 51)}

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
                text_color = (0, 0, 0)  if (value < 8) else (204, 229, 255)

                text = font.render(str(value), True, text_color)
                text_rect = text.get_rect(center = tile_rect.center)
                window.blit(text, text_rect)

#######################################################
#Powerhouse to display a bunch of prompts on the screen
def display_prompt(window, prompt, width, height):
    BOX_COLOR = (255, 51, 255)
    TEXT_COLOR = (0, 0, 0)

    box_width = int(width * 0.75)
    box_height = height // 4

    #centering
    box_x = (width - box_width) // 2
    box_y = (height - box_height) // 2

    box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
    pygame.draw.rect(window, BOX_COLOR, box_rect, border_radius = 0)

    font = pygame.font.Font(None, 48)
    text = font.render(prompt, False, TEXT_COLOR) #8 bit effect?
    text_rect = text.get_rect(center = box_rect.center)
    window.blit(text, text_rect)

########################################
#handles events for keydown; passes to WASD_handler, R_handler, Q_handler
def keydown_handler(event, window, board_obj, width, height):
    #print("keydown called")
    if event.key in (pygame.K_w, pygame.K_a, pygame.K_s, pygame.K_d,
                     pygame.K_LEFT, pygame.K_UP, pygame.K_RIGHT, pygame.K_DOWN):
        #print("called WASD_handler")
        WASD_handler(event, board_obj)
    elif event.key == pygame.K_q:   #quit
        Q_handler(event, window, board_obj, width, height)
    elif event.key == pygame.K_r:   #reset
        R_handler(event, window, board_obj, width, height)
    elif event.key == pygame.K_p:
        print("printing board")
        board_obj.print_board()
    else:
        pass

######################################
def WASD_handler(event, board_obj):
    DIRECTIONS = {pygame.K_a : 0,
                  pygame.K_w : 1,
                  pygame.K_d : 2,
                  pygame.K_s : 3,
                  pygame.K_LEFT : 0,
                  pygame.K_UP : 1,
                  pygame.K_RIGHT : 2,
                  pygame.K_DOWN : 3}

    old_board = board_obj.board.copy()
    board_obj.move(DIRECTIONS[event.key])

    if not np.array_equal(old_board, board_obj.board):
        board_obj.fill_cell()

###########################################3
#reset the board?
def R_handler(event, window, board_obj, width, height):
    if ask_yes_or_no(window,
                     "Do you want to reset? [y/n]",
                     board_obj,
                     width,
                     height):
        display_prompt_and_render(window, "Resetting...", board_obj, width, height)
        board_obj.reset_board()
    else:
        display_prompt_and_render(window, "A(board)ed", board_obj, width, height)


#quit the game?
def Q_handler(event, window, board_obj, width, height):
    if ask_yes_or_no(window,
                     "Do you want to quit? [y/n]",
                     board_obj,
                     width,
                     height):
        display_prompt_and_render(window, "Quitting, Goodbye", board_obj, width, height)
        pygame.quit()
        sys.exit()  #triggers warnings ... ok
    else:
        display_prompt_and_render(window, "A(board)ed", board_obj, width, height)

#helper funtion for R_handler, Q_handler
def display_prompt_and_render(window, prompt, board_obj, width, height):
    draw_board(window, board_obj, width, height)
    display_prompt(window, prompt, width, height)
    pygame.display.flip()
    pygame.time.wait(1000)

############################################
#handles yes or no questions for prompts
def ask_yes_or_no(window, prompt, board_obj, width, height):
    #print(prompt) #placeholder till i get a graphics display going
    waiting = True

    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  #triggers warnings ... ok
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True
                elif event.key == pygame.K_n:
                    return False

        draw_board(window, board_obj, width, height)
        display_prompt(window, prompt, width, height)
        pygame.display.flip()
