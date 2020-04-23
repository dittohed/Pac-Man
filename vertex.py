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
