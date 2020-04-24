from math import sqrt
from vertex import *
from settings import *
import pygame as pg

def find_shortest(start_x, start_y, player_x, player_y, game):

    # determine neighbors for starting position and create temporary start vertex
    start_v = determine_neighbors_dir(start_x // TILE_SIZE, start_y // TILE_SIZE,
                                        game.map_data, game.vertices, dynamic = True)
    start_v.current_shortest[0] = 0
    print(start_v.neigh_directions)

    # determine neighbors for current end (player) position and create temporary end vertex
    end_v = determine_neighbors_dir(player_x // TILE_SIZE, player_y // TILE_SIZE,
                                        game.map_data, game.vertices, dynamic = True)
    end_v.current_shortest[0] = 0

    # calculate euclidean distance to the player (end_v) for each vertex
    for v in game.vertices:
        v.euclidean_distance = sqrt((v.x - end_v.x) ** 2 + (v.y - end_v.y) ** 2)

    q = [[start_v.current_shortest[0] + start_v.euclidean_distance, start_v]]
    # Priority queue implemented using a list (sorting each insert / update) ~ O(nlogn).
    # Each queue object is a 2 element list [distace_to_the_vertex, vertex],
    # this allows to sort lists inside a queue.

    # Check this A* implementation
    already_popped = set()
    popped = None

    while popped != end_v:
        popped = q.pop(0)[1]
        print(f"{popped.x}{popped.y} vertex popped!")

        # visit all the neighbors
        for neighbor in popped.adj:
            v = neighbor[0]
            distance = neighbor[1]

            if v in already_popped:
                continue

            if popped.current_shortest + distance < v.current_shortest:
                v.current_shortest[0] = popped.current_shortest + distance
                v.predecessor = popped

            if v not in q and v not in already_popped:
                q.append([v.current_shortest[0] + v.euclidean_distance, v])

            q.sort() # sorting forces a priority queue functionality

        already_popped.add(popped)

    # print shortest path
    v = end_v
    while predecessor != None:
        pg.draw.rect(self.screen, (255, 0, 0),
            pg.Rect(v.x * TILE_SIZE, v.y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
        print(f"My coordinates: ({v.x}, {v.y})")
        print(f"My predecessor coordinates: ({v.predecessor.x}, {v.predecessor.y})")
        v = v.predecessor
