"""
USEFUL TERMINOLOGY:
sprites - 2D bitmap used to represent objects
assets - sounds and art
"""

# TODO:
# 1. Move vertices part to the seperate file (calculate this in Game.load_data())
# 2. Create determine_neighbors_dir(), determine_neighbors() functions

import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from vertex import *

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

                if tile in ['.', 'P']:
                    neigh_directions = set()

                    if col > 0 and self.map_data[row][col - 1] in ['.', 'P']: # check left
                        neigh_directions.add("left")
                    if col < GRID_WIDTH - 1 and self.map_data[row][col + 1] in ['.', 'P']: # check right
                        neigh_directions.add("right")
                    if row > 0 and self.map_data[row - 1][col] in ['.', 'P']: # check up
                        neigh_directions.add("up")
                    if row < GRID_HEIGHT - 1 and self.map_data[row + 1][col] in ['.', 'P']: # check down
                        neigh_directions.add("down")

                    # check if either y or x condition is met
                    if (("left" in neigh_directions or "right" in neigh_directions)
                            and ("up" in neigh_directions or "down" in neigh_directions)):
                        self.vertices.add(Vertex((col, row), neigh_directions))

        # build adjacency lists
        for v1 in self.vertices:
            INF = 10000 # any actual distance will be lesser than 10000
            currently_closest = {"left": [None, INF], # instead of [tuple(), INF]
                "right": [None INF],
                "up": [None, INF],
                "down": [None, INF]}

            for v2 in self.vertices:
                if v1 == v2:
                    continue

                if "left" in v1.neigh_directions:
                    if v1.y == v2.y and v1.x > v2.x and currently_closest["left"][1] > v1.x - v2.x:
                        currently_closest["left"][0] = v2 # instead of (v2.x, v2.y)
                        currently_closest["left"][1] = v1.x - v2.x
                if "right" in v1.neigh_directions:
                    if v1.y == v2.y and v1.x < v2.x and currently_closest["right"][1] > v2.x - v1.x:
                        currently_closest["right"][0] = v2 # instead of (v2.x, v2.y)
                        currently_closest["right"][1] = v2.x - v1.x
                if "up" in v1.neigh_directions:
                    if v1.x == v2.x and v1.y > v2.y and currently_closest["up"][1] > v1.y - v2.y:
                        currently_closest["up"][0] = v2 # instead of (v2.x, v2.y)
                        currently_closest["up"][1] = v1.y - v2.y
                if "down" in v1.neigh_directions:
                    if v1.x == v2.x and v1.y < v2.y and currently_closest["down"][1] > v2.y - v1.y:
                        currently_closest["down"][0] = v2 # instead of (v2.x, v2.y)
                        currently_closest["down"][1] = v2.y - v1.y

            for key in currently_closest.keys():
                if currently_closest[key][0]: # instead of if key in v1.neigh_directions:
                    v1.adj.append(tuple(currently_closest[key]))

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
            pg.draw.rect(self.screen, (255, 0, 0),
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
    g.run()
    g.show_game_over_screen()
