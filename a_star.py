from math import sqrt

def find_shortest(start_x, start_y, end_v, vertices):

    # calculate euclidean distance to the player (end_v) for each vertex
    for v in vertices:
        v.euclidean_distance = sqrt((v.x - end_v.x) ** 2 + (v.y - end_v.y) ** 2)

    # determine neighbors for starting position (this vertex is created dynamically)
    start_v = Vertex((start_x, start_y), ...)
    start_v.current_shortest[0] = 0

    q = [[start_v.current_shortest + start_v.euclidean_distance, start_v]]
    # Priority queue as a list (with a frequent sorting) ~ O(nlogn).
    # Each queue object is a 2 element list [distace_to_the_vertex, vertex],
    # this allows us to sort lists inside a queue.

    # TODO: finish start_v section along with the end_v section
    # TODO: change adj elements structure to (Vertex, distance)

    # Check this A* implementation
    visited = set()

    while popped != end_v:
        popped = q.pop(0)[1]

        # visit all the neighbors
        for neighbor in popped.adj:
            v = neighbor[0]
            distance = neighbor[1]

            if v in visited:
                continue

            if popped.current_shortest + distance < v.current_shortest:
                v.current_shortest[0] = popped.current_shortest + distance
                v.predecessor = popped

            q.append([v.current_shortest + v.euclidean_distance, v])
            q.sort() # sorting forces a priority queue functionality

        visited.add(popped)
