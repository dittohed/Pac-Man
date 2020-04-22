class Vertex:
    def __init__(self, coords, neigh_directions, left = None, right = None, up = None, down = None, left_d = None, right_d = None, up_d = None, down_d = None):
        self.coords = coords
        self.neigh_directions = neigh_directions # list of 4 booleans - each one containing information if this vertex # has a neighbor on the [left, right, up, down]

        # neighbors coordinates
        self.left = left
        self.right = right
        self.up = up
        self.down = down

        # distance to neighbors
        self.left_d = left_d
        self.right_d = right_d
        self.up_d = up_d
        self.down_d = down_d

        self.real_distance = None # ?
