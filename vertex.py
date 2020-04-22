class Vertex:
    def __init__(self, coords, neigh_directions):
        self.x = coords[0]
        self.y = coords[1]
        self.neigh_directions = neigh_directions
                # set of where neighbors appear (to the "left" or "right" or ...)

        self.adj = [] # adjacency list storing neighbors tuples ((x_neigh, y_neigh), distance)

        self.euclidean_distance = None # distance to the player
                               # this will be calculated dynamically (during the game as the player moves)
