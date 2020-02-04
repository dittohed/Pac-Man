import pygame as pg
import random

#--- config ---
WIDTH = 480
HEIGHT = 360
FPS = 60

#--- initial setup ---
pg.init()
pg.mixer.init()
window = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Pac-Man")
clock = pg.time.Clock()

#--- gameloop ---
running = True
while running:
    clock.tick(FPS) #pause, so there could be only 60 loops per second

    #--- process events ---
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    #--- update ---

    #--- draw ---
    window.fill((0, 0, 0))
    #pg uses double buffering (likewise whiteboard flipping - draw and then flip the board)
    pg.display.flip()

pg.quit()
