from graphs import graph
import random


def vertex_cover(graph):
    cover = []
    matrix = graph.get_matrix()
    nodes = len(graph.get_nodes())
    edge = 0
    while edge != 0:
        node1 = random.randint(0, nodes - 1)
        node2 = random.randint(0, nodes - 1)
        while  matrix[node1][node2] == 0:
            node1 = random.randint(0, nodes - 1)
            node2 = random.randint(0, nodes - 1)





