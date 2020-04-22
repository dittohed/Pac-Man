from math import sqrt

def find_shortest(start_x, start_y, end_v, vertices):
    # calculate euclidean distance to the player (end_v)
    for v in vertices:
        v.euclidean_distance = sqrt((v.x - end_v.x) ** 2 + (v.y - end_v.y) ** 2)

    while popped != end_v:
        
