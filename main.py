"""
USEFUL TERMINOLOGY:
sprites - 2D bitmap used to represent objects
assets - sounds and art
"""

#TODO: czemu wywala mi pac-mana, skoro vel = 0

import pygame as pg
import sys
from os import path
from settings import *
from sprites import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGTH))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(1, 100) #after 1 ms delay repeat key each 100ms if held
        self.load_data()

    def load_data(self):
        game_folder = path.dirname(__file__)

        f = open(path.join(game_folder, "map.txt"), "r")
        self.map_data = f.readlines()

    def new(self):
        # setup for a new round
        self.all_sprites = pg.sprite.Group() #collection used to simplify sprites manipulation
        self.walls = pg.sprite.Group()

        # enumarate assings indices to objects in iterable
        # in general: for index, item in enumerate(iterable):
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == 'W':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)

    def run(self):
        # game loop
        self.playing = True
        while self.playing:
            self.dt = self.clock.tick(FPS) / 1000

            # tick() method computes how many miliseconds have passed since the previous call (previous frame length).
            # Using the argument makes the function delay to keep the game running slower than
            # the given ticks per second. This can be used to help limit the runtime speed of a game.
            # For example, by calling Clock.tick(40) once per frame, the program will never run
            # at more than 40 frames per second.

            # self.dt is useful for time-based movement (frame independent).
            # Otherwise going to 30 FPS instead of 60 will make sprites slower.
            # / 1000 to convert miliseconds to seconds.

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
            pg.draw.line(self.screen, (110, 110, 110), (x, 0), (x, HEIGTH)) # draw vertical lines

        for y in range(0, HEIGTH, TILE_SIZE):
            pg.draw.line(self.screen, (110, 110, 110), (0, y), (WIDTH, y)) # draw horizontal lines

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        # pg uses double buffering (likewise whiteboard flipping - draw and then flip the board)
        pg.display.flip()

    def events(self):
        # catch player input
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.quit()


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
