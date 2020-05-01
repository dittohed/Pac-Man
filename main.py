"""
USEFUL TERMINOLOGY:
sprites - 2D bitmap used to represent objects
assets - sounds and art
"""

# TODO:
# 1. Move vertices part to the seperate file (calculate this in Game.load_data())
# 2. Why does start_v has an empty adj list?

import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from vertex import *
from a_star import *

class Game:
    def __init__(self):
        pg.init()
        self.screen = pg.display.set_mode((WIDTH, HEIGTH))
        pg.display.set_caption(TITLE)
        self.clock = pg.time.Clock()
        pg.key.set_repeat(1, 100) # after 1 ms delay repeat key each 100ms if held
        self.load_data()
        self.vertices = set() # set containing Vertex objects (vertices for path-finding)

    def load_data(self):
        game_folder = path.dirname(__file__)

        f = open(path.join(game_folder, "map.txt"), "r")
        self.map_data = f.readlines()

    def new(self):
        # setup for a new round
        self.all_sprites = pg.sprite.Group() # simplify sprites manipulation
        self.walls = pg.sprite.Group()

        # enumarate assings indices to objects in iterable
        # in general: for index, item in enumerate(iterable):
        for row, tiles in enumerate(self.map_data):
            for col, tile in enumerate(tiles):
                if tile == 'W':
                    Wall(self, col, row)
                if tile == 'P':
                    self.player = Player(self, col, row)

                # Let's determine graph vertices for path-finding basing on map file.
                # What is typical of vertices?
                # It enables you to go either y or x direction (make them available)!

                if tile == '.':
                    determine_neighbors_dir(col, row, self.map_data, self.vertices)
                    # This function determines all possible neighbors directions and creates a vertex if it enables
                    # you to go either y or x direction.

        for v in self.vertices:
            v.build_adj_list(self.vertices) # build adjacency lists

    def run(self):
        # game loop
        self.playing = True
        while self.playing:
            self.clock.tick(FPS)

        # tick() method computes how many miliseconds have passed since the previous call
        # (previous frame length).
        # Using the argument makes the function delay to keep the game running slower than
        # the given ticks per second. This can be used to help limit the runtime speed of a game.
        # For example, by calling Clock.tick(40) once per frame, the program will never run
        # at more than 40 frames per second.

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

    def draw_vertices(self):
        for v in self.vertices:
            pg.draw.rect(self.screen, (160, 160, 160),
                pg.Rect(v.x * TILE_SIZE, v.y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    def draw(self):
        self.screen.fill((0, 0, 0))
        self.draw_grid()
        self.all_sprites.draw(self.screen)
        self.draw_vertices()
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
    # test - wypisz wierzchołki i ich sąsiadów

    for v in g.vertices:
        print(f"Vertex at ({v.x}, {v.y}), adjacency list: {v.adj}")

    # test - wyświetl najkrótszą ścieżkę do gracza z punktu (3, 1)
    find_shortest(32 * 3, 32, g.player.rect.x, g.player.rect.y, g)
    g.run()
    g.show_game_over_screen()
