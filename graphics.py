#TODO: add openGL graphics//pygame

import pygame

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

    #event loop
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                print(f"Keypress : {event.key}")

        window.fill(WHITE)

        #events happen here TODO

        pygame.display.flip()

    pygame.quit()
