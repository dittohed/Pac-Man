class Vertex:
    def __init__(self, number, str):
        self.x = [number]
        self.text = str

import heapq

q = []

v1 = Vertex(3, "v1")
v2 = Vertex(2, "v2")

q.append([v1.x, v1])
q.append([v2.x, v2])
q.sort()

print(q)

v1.x[0] = 1
q.sort()

print(q)

print(q.pop(0)[1].text)
