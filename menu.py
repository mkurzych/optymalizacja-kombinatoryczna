import networkx as nx

from chinese_postman.main import chinese_postman
from graphs import graph, directedGraph, createGraph
from vertex_cover.main import vertex_cover
from christofides.main import christofides
import matplotlib.pyplot as plt

weighted = False


def plot_graph(graph):
    pos = nx.shell_layout(graph)
    edge_labels = nx.get_edge_attributes(graph, "weight")

    nx.draw_networkx_nodes(graph, pos)
    nx.draw_networkx_edges(graph, pos)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    nx.draw_networkx_labels(graph, pos)
    plt.show()


def print_menu():
    print("1. Add node")
    print("2. Remove node")
    print("3. Add edge")
    print("4. Remove edge")
    print("5. Get degree (Graph only)")
    print("6. Get out degree (DirectedGraph only)")
    print("7. Get in degree (DirectedGraph only)")
    print("8. Get degrees (Graph only)")
    print("9. Get min degree (Graph only)")
    print("10. Get max degree (Graph only)")
    print("11. Get even degrees (Graph only)")
    print("12. Get odd degrees (Graph only)")
    print("13. Run vertex cover (Graph only)")
    print("14. Find chinese postman path (WeightedGraph only)")
    print("15. Run salesman problem (WeightedGraph only)")
    print("16. Plot graph")
    print("17. Exit")

file_or_input = input("Do you want to read from file or input? (f/i): ")
if file_or_input == "f":
    file_path = input("Enter file path: ")
    data = createGraph.create_graph(file_path)
    graph = data[0]
    weighted = data[1]
    if not weighted:
        graph.plot_graph()
elif file_or_input == "i":
    while True:
        graph_type = input("Enter graph type (N/D/W): ")
        if graph_type == "N":
            graph = graph.Graph()
            break
        elif graph_type == "D":
            graph = directedGraph.DirectedGraph()
            break
        elif graph_type == "W":
            weighted = True
            graph = nx.Graph()
            break
        else:
            print("Invalid graph type")
    nodes = int(input("Enter number of nodes: "))
    for i in range(nodes):
        label = input(f"Enter label for node {i+1}: ")
        if label == "":
            print("Invalid input")
            label = input(f"Enter label for node {i + 1}: ")
            i -= 1
            continue
        graph.add_node(label)
    while True:
        edge = input("Enter edge (format: node1 node2) or 'done' to finish: ")
        if edge == "done":
            break
        try:
            node1, node2 = edge.split()
        except ValueError:
            print("Invalid input")
            continue
        if weighted:
            weight = int(input("Enter weight: "))
            graph.add_edge(node1, node2, weight=weight)
        else:
            graph.add_edge(node1, node2)
    if not weighted:
        graph.plot_graph()
else:
    print("Invalid input")

while True:
    print_menu()
    choice = input("Enter your choice: ")
    if choice == "1":
        label = input("Enter node label: ")
        graph.add_node(label)
        if weighted:
            plot_graph(graph)
        else:
            graph.plot_graph()
    elif choice == "2":
        label = input("Enter node label: ")
        graph.remove_node(label)
        if weighted:
            plot_graph(graph)
        else:
            graph.plot_graph()
    elif choice == "3":
        node1 = input("Enter first node label: ")
        node2 = input("Enter second node label: ")
        if weighted:
            weight = int(input("Enter weight: "))
            graph.add_edge(node1, node2, weight=weight)
            plot_graph(graph)
        else:
            graph.add_edge(node1, node2)
            graph.plot_graph()
    elif choice == "4":
        node1 = input("Enter first node label: ")
        node2 = input("Enter second node label: ")
        graph.remove_edge(node1, node2)
        if weighted:
            plot_graph(graph)
        else:
            graph.plot_graph()
    elif choice == "5" and graph.type == "N":
        label = input("Enter node label: ")
        print("Degree:", graph.get_degree(label))
    elif choice == "6" and graph.type == "D":
        label = input("Enter node label: ")
        print("Out degree:", graph.get_out_degree(label))
    elif choice == "7" and graph.type == "D":
        label = input("Enter node label: ")
        print("In degree:", graph.get_in_degree(label))
    elif choice == "8" and graph.type == "N":
        print("Degrees:", graph.get_degrees())
    elif choice == "9" and graph.type == "N":
        print("Min degree:", graph.get_min_degree())
    elif choice == "10" and graph.type == "N":
        print("Max degree:", graph.get_max_degree())
    elif choice == "11" and graph.type == "N":
        print("Even degrees:", graph.get_even_degrees())
    elif choice == "12" and graph.type == "N":
        print("Odd degrees:", graph.get_odd_degrees())
    elif choice == "13" and graph.type == "N":
        cover = vertex_cover(graph)
        print("Cover:", cover)
    elif choice == "14" and weighted:
        source = input("Enter source node: ")
        weight, path = chinese_postman(graph, source)
        print("Path:", path)
        print("Weight:", weight)
    elif choice == "15" and weighted:
        source = input("Enter source node: ")
        weight, path = christofides(graph, source)
        print("Path:", path)
        if weight:
            print("Weight:", weight)
    elif choice == "16" and not weighted:
        graph.plot_graph()
    elif choice == "17":
        break
    else:
        print("Invalid choice or method not available for this graph type.")
    input("Press enter to continue...")