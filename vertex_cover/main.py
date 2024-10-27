import random


def vertex_cover(graph):
    cover = []
    counter = 1
    while graph.get_edges() != 0:
        nodes = len(graph.nodes)
        edge = 0
        node1 = 0
        node2 = 0
        while edge == 0:
            node1 = random.randint(0, nodes - 1)
            node2 = random.randint(0, nodes - 1)
            while node1 == node2:
                node2 = random.randint(0, nodes - 1)
            edge = graph.get_matrix()[node1][node2]
        print("Edge", counter, ":", graph.nodes[node1], graph.nodes[node2])
        cover.append(graph.nodes[node1])
        cover.append(graph.nodes[node2])
        if node1 > node2:
            graph.remove_node(graph.nodes[node1])
            graph.remove_node(graph.nodes[node2])
        else:
            graph.remove_node(graph.nodes[node2])
            graph.remove_node(graph.nodes[node1])
        counter += 1
        graph.plot_graph()
    return cover






