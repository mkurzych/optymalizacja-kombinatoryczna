import matplotlib.pyplot as plt
import networkx as nx
import itertools as it


def chinese_postman(graph, source):
    plot_graphs(graph)

    if not nx.is_eulerian(graph):
        print("Graph has odd degrees")
        odd_nodes = nx.Graph()
        for node in graph.nodes:
            if graph.degree(node) % 2 != 0:
                odd_nodes.add_node(node)
        new = list(odd_nodes.nodes)
        graph = nx.MultiGraph(graph)
        for i in range(len(new)):
            for j in range(i + 1, len(new)):
                weight = 0
                shortest_path = nx.shortest_path(graph, weight="weight", source=new[i], target=new[j])
                for k in range(len(shortest_path) - 1):
                    weight += graph[shortest_path[k]][shortest_path[k + 1]][0]["weight"]
                odd_nodes.add_edge(new[i], new[j], weight=weight)
        matching = nx.min_weight_matching(odd_nodes)
        plot_graph(odd_nodes, matching)
        for edge in matching:
            shortest_path = nx.shortest_path(graph, weight="weight", source=edge[0], target=edge[1])
            for k in range(len(shortest_path) - 1):
                weight = graph[shortest_path[k]][shortest_path[k + 1]][0]["weight"]
                graph.add_edge(shortest_path[k], shortest_path[k + 1], weight=weight)
        plot_graphs(graph)

    else:
        print("Graph has all even degrees")
    print("Finding Eulerian path")
    eulerian = list(nx.eulerian_circuit(graph))

    if source in eulerian:
        start_index = next(i for i, edge in enumerate(eulerian) if edge[0] == source)
        eulerian = eulerian[start_index:] + eulerian[:start_index]

    path = ''
    weight = 0
    for edge in eulerian:
        weight += graph[edge[0]][edge[1]][0]['weight']
        path += edge[0]
        path += ' -> '
    path += eulerian[-1][1]
    return weight, path


def plot_graph(graph, path=None):
    pos = nx.shell_layout(graph)
    edge_labels = nx.get_edge_attributes(graph, "weight")
    edge_colors = ['red' if path and (u, v) in path or (v, u) in path else 'black' for u, v in graph.edges(data=False)]

    nx.draw_networkx_nodes(graph, pos)
    nx.draw_networkx_edges(graph, pos, edge_color=edge_colors)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    nx.draw_networkx_labels(graph, pos)
    plt.show()


def plot_graphs(graph):
    connectionstyle = [f"arc3,rad={r}" for r in it.accumulate([0.15] * 4)]
    pos = nx.shell_layout(graph)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6))

    edge_labels = nx.get_edge_attributes(graph, "weight")

    edge_colors1 = []
    seen_edges = set()
    for u, v in graph.edges(data=False):
        if (u, v) in seen_edges or (v, u) in seen_edges:
            edge_colors1.append('black')
        else:
            edge_colors1.append('red' if graph.number_of_edges(u, v) > 1 else 'black')
            seen_edges.add((u, v))

    edge_colors2 = ['red' if graph.number_of_edges(u, v) > 1 else 'black' for u, v in graph.edges(data=False)]

    nx.draw_networkx_nodes(graph, pos, ax=ax1)
    nx.draw_networkx_edges(graph, pos, connectionstyle=connectionstyle, arrows=True, edge_color=edge_colors1, ax=ax1)
    nx.draw_networkx_labels(graph, pos, ax=ax1)

    nx.draw_networkx_nodes(graph, pos, ax=ax2)
    nx.draw_networkx_edges(graph, pos, edge_color=edge_colors2, ax=ax2)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, ax=ax2)
    nx.draw_networkx_labels(graph, pos, ax=ax2)

    plt.show()