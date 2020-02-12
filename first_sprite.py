#USEFUL TERMINOLOGY
#sprites - 2D bitmap used to represent objects
#assets - sounds and art

import pygame as pg
import random
import os

#--- config ---
WIDTH = 800
HEIGHT = 600
FPS = 60

game_folder = os.path.dirname(__file__) #current dir
img_folder = os.path.join(game_folder, "img")

class Player(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self) #base class constructor
        self.image = pg.Surface((50, 50)) #or image.load(..).convert() - converts to Python-friendly format
        #self.image.set_colorkey(...) - which color to make transparent
        self.image.fill((0, 255, 255))
        self.rect = self.image.get_rect() #rectangle enclosing the sprite
                            #get_rect determines rect size automatically
        self.rect.center = (WIDTH / 2, HEIGHT / 2)

    def update(self):
        self.rect.x += 5
        if self.rect.left > WIDTH:
            self.rect.right = 0

#--- initial setup ---
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("Pac-Man")
clock = pg.time.Clock()

all_sprites = pg.sprite.Group() #collection used to simplify sprites manipulation
player = Player()
all_sprites.add(player)

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
