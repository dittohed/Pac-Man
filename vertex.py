from settings import *
INF = 10000

class Vertex:
    def __init__(self, coords, neigh_directions):
        self.x = coords[0]
        self.y = coords[1]
        self.neigh_directions = neigh_directions
                # set of where neighbors appear (to the "left" or "right" or ...)

        self.adj = [] # adjacency list storing neighbors tuples (Vertex, distance_to_this_Vertex)

        # calculated dynamically
        self.euclidean_distance = None # distance to the player
        self.current_shortest = [INF] # path length up to this vertex
                            # this has to be list, to get a "pointer" character of this attribute
                            # this is a must for a priority queue with decrementable keys
        self.predecessor = None

    def build_adj_list(self, vertices):
        INF = 10000 # any actual distance will be lesser than 10000
        currently_closest = {"left": [None, INF],
            "right": [None, INF],
            "up": [None, INF],
            "down": [None, INF]}

        for v in vertices:
            if v == self:
                continue

            if "left" in self.neigh_directions:
                if self.y == v.y and self.x > v.x and currently_closest["left"][1] > self.x - v.x:
                    currently_closest["left"][0] = v # instead of (v2.x, v2.y)
                    currently_closest["left"][1] = self.x - v.x
            if "right" in self.neigh_directions:
                if self.y == v.y and self.x < v.x and currently_closest["right"][1] > v.x - self.x:
                    currently_closest["right"][0] = v # instead of (v2.x, v2.y)
                    currently_closest["right"][1] = v.x - self.x
            if "up" in self.neigh_directions:
                if self.x == v.x and self.y > v.y and currently_closest["up"][1] > self.y - v.y:
                    currently_closest["up"][0] = v # instead of (v2.x, v2.y)
                    currently_closest["up"][1] = self.y - v.y
            if "down" in self.neigh_directions:
                if self.x == v.x and self.y < v.y and currently_closest["down"][1] > v.y - self.y:
                    currently_closest["down"][0] = v # instead of (v2.x, v2.y)
                    currently_closest["down"][1] = v.y - self.y

        for key in currently_closest.keys():
            if currently_closest[key][0]:
                self.adj.append(tuple(currently_closest[key]))

def determine_neighbors_dir(col, row, map_data, vertices, dynamic = False):
    neigh_directions = set()

    if col > 0 and map_data[row][col - 1] in ['.', 'P']: # check left
        neigh_directions.add("left")
    if col < GRID_WIDTH - 1 and map_data[row][col + 1] in ['.', 'P']: # check right
        neigh_directions.add("right")
    if row > 0 and map_data[row - 1][col] in ['.', 'P']: # check up
        neigh_directions.add("up")
    if row < GRID_HEIGHT - 1 and map_data[row + 1][col] in ['.', 'P']: # check down
        neigh_directions.add("down")

    if dynamic: # no check if either y or x condition is met
        new_v = Vertex((col, row), neigh_directions)
        vertices.add(new_v)
        return new_v

    # check if either y or x condition is met
    if (("left" in neigh_directions or "right" in neigh_directions)
            and ("up" in neigh_directions or "down" in neigh_directions)):
        new_v = Vertex((col, row), neigh_directions)
        vertices.add(new_v)
        return new_v

    return None
