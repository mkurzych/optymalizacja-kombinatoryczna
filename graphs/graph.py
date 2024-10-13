import matplotlib.pyplot as plt
import networkx as nx
import itertools as it


class Graph:
    def __init__(self):
        self.matrix = []
        self.nodes = 0

    def add_node(self):
        self.matrix.append([0 for i in range(self.nodes + 1)])
        for i in range(self.nodes):
            self.matrix[i].append(0)
        self.nodes += 1

    def remove_node(self, node):
        if node < self.nodes:
            self.nodes -= 1
            self.matrix.pop(node)
            for i in range(self.nodes):
                self.matrix[i].pop(node)

    def add_edge(self, node1, node2):
        if node1 < self.nodes and node2 < self.nodes:
            self.matrix[node1][node2] += 1
            self.matrix[node2][node1] += 1

    def remove_edge(self, node1, node2):
        if node1 < self.nodes and node2 < self.nodes and self.matrix[node1][node2] > 0:
            self.matrix[node1][node2] -= 1
            self.matrix[node2][node1] -= 1

    def get_degree(self, node):
        if node < self.nodes:
            return sum(self.matrix[node])

    def get_degrees(self):
        degrees = []
        for i in range(self.nodes):
            degrees.append(sum(self.matrix[i]))
        return sorted(degrees, reverse=True)

    def get_min_degree(self):
        return self.get_degrees()[-1]

    def get_max_degree(self):
        return self.get_degrees()[0]

    def get_even_degrees(self):
        return sum([1 for degree in self.get_degrees() if degree % 2 == 0])

    def get_odd_degrees(self):
        return sum([1 for degree in self.get_degrees() if degree % 2 != 0])

    def plot_graph(self):
        plot = nx.MultiGraph()
        for i in range(self.nodes):
            plot.add_node(i)
        for i in range(self.nodes):
            for j in range(i, self.nodes):
                if self.matrix[i][j] > 0:
                    for k in range(self.matrix[i][j]):
                        plot.add_edge(i, j)
        connectionstyle = [f"arc3,rad={r}" for r in it.accumulate([0.15] * 4)]
        pos = nx.shell_layout(plot)
        nx.draw_networkx_nodes(plot, pos)
        nx.draw_networkx_edges(
            plot, pos, connectionstyle=connectionstyle
        )
        nx.draw_networkx_labels(plot, pos)
        plt.show()

    def get_matrix(self):
        return self.matrix

