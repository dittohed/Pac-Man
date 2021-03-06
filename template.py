#USEFUL TERMINOLOGY
#sprites - 2D bitmap used to represent objects

import pygame as pg
import random

#--- config ---
WIDTH = 480
HEIGHT = 360
FPS = 60

#--- initial setup ---
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Pac-Man")
clock = pg.time.Clock()

all_sprites = pg.sprite.Group() #collection used to simplify sprites manipulation

#--- gameloop ---
running = True
while running:
    clock.tick(FPS) #pause, so there could be only 60 loops per second

    #--- process events ---
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    #--- update ---
    all_sprites.update()

    #--- draw ---
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    #pg uses double buffering (likewise whiteboard flipping - draw and then flip the board)
    pg.display.flip()

pg.quit()
