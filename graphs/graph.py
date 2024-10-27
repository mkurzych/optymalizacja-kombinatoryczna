import matplotlib.pyplot as plt
import networkx as nx
import itertools as it


class Graph:
    def __init__(self):
        self.type = "N"
        self.matrix = []
        self.nodes = []

    def add_node(self, label):
        self.matrix.append([0 for i in range(len(self.nodes) + 1)])
        for i in range(len(self.nodes)):
            self.matrix[i].append(0)
        self.nodes.append(label)

    def remove_node(self, label):
        if label in self.nodes:
            node = self.nodes.index(label)
            self.nodes.pop(node)
            self.matrix.pop(node)
            for i in range(len(self.nodes)):
                self.matrix[i].pop(node)

    def add_edge(self, label1, label2):
        if label1 in self.nodes and label2 in self.nodes:
            node1 = self.nodes.index(label1)
            node2 = self.nodes.index(label2)
            self.matrix[node1][node2] += 1
            self.matrix[node2][node1] += 1

    def remove_edge(self, label1, label2):
        if label1 in self.nodes and label2 in self.nodes:
            node1 = self.nodes.index(label1)
            node2 = self.nodes.index(label2)
            if self.matrix[node1][node2] > 0:
                self.matrix[node1][node2] -= 1
                self.matrix[node2][node1] -= 1

    def get_degree(self, label):
        if label in self.nodes:
            node = self.nodes.index(label)
            return sum(self.matrix[node])

    def get_degrees(self):
        degrees = []
        for i in range(len(self.nodes)):
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
        for i in range(len(self.nodes)):
            plot.add_node(self.nodes[i])
        for i in range(len(self.nodes)):
            for j in range(i, len(self.nodes)):
                if self.matrix[i][j] > 0:
                    for k in range(self.matrix[i][j]):
                        plot.add_edge(self.nodes[i], self.nodes[j])
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

    def get_edges(self):
        edges = 0
        for i in range(len(self.nodes)):
            edges += sum(self.matrix[i])
        return edges

