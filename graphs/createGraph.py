from graphs.graph import Graph
from graphs.directedGraph import DirectedGraph
import networkx as nx



def create_graph(file_path):

    weighted = False

    with open(file_path, "r") as file:
        data = file.readlines()
        for i in range(len(data)):
            data[i] = data[i].rstrip('\n')
            data[i] = data[i].split(" ")

        if data[0][0] == "N":
            graph = Graph()
        elif data[0][0] == "D":
            graph = DirectedGraph()
        elif data[0][0] == "W":
            graph = nx.Graph()
            weighted = True
        else:
            print("Invalid graph type")
            exit()

        edges = data[1:]
        nodes = list(set([item for sublist in edges for item in sublist[:2]]))

        for i in range(len(nodes)):
            graph.add_node(nodes[i])

        if weighted:
            for edge in edges:
                graph.add_edge(edge[0], edge[1], weight=int(edge[2]))
        else:
            for edge in edges:
                graph.add_edge(edge[0], edge[1])

        return graph, weighted



