"""
USEFUL TERMINOLOGY:
sprites - 2D bitmap used to represent objects
assets - sounds and art
"""

import pygame as pg
import sys
from settings import *
from sprites import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGTH))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(300, 100) #after 0.3s delay repeat key each 0.1 if held
        self.load_data()

    def load_data(self):
        pass

    def new(self):
        #setup for a new round
        self.all_sprites = pg.sprite.Group() #collection used to simplify sprites manipulation
        self.walls = pg.sprite.Group()

        self.player = Player(self, 0, 0)
        for x in range(10, 20):
            Wall(self, x, 5)

    def run(self):
        #game loop
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000 #pause, so there could be only 60 loops per second
            self.events()
            self.update()
            self.draw()

    def quit(self):
        pg.quit()
        sys.exit()

    def update(self):
        self.all_sprites.update()

    def draw_grid(self):
        for x in range(0, WIDTH, TILE_SIZE):
            pg.draw.line(self.screen, (110, 110, 110), (x, 0), (x, HEIGTH)) #draw vertical lines

        for y in range(0, HEIGTH, TILE_SIZE):
            pg.draw.line(self.screen, (110, 110, 110), (0, y), (WIDTH, y)) #draw horizontal lines

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        #pg uses double buffering (likewise whiteboard flipping - draw and then flip the board)
        pg.display.flip()

    def events(self):
        #catch player input
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()
                if event.key == pg.K_LEFT:
                    self.player.move(dx = -1)
                if event.key == pg.K_RIGHT:
                    self.player.move(dx = 1)
                if event.key == pg.K_UP:
                    self.player.move(dy = -1)
                if event.key == pg.K_DOWN:
                    self.player.move(dy = 1)

    def show_start_screen(self):
        pass

    def show_game_over_screen(self):
        pass

# --- GAME STARTS HERE ---
g = Game()
g.show_start_screen()

while True:
    g.new()
    g.run()
    g.show_game_over_screen()
