import networkx as nx
import matplotlib.pyplot as plt

def plot_graph(graph, path=None):
    pos = nx.shell_layout(graph)
    edge_labels = nx.get_edge_attributes(graph, "weight")

    edge_colors = ['red' if path and ((u, v) in path or (v, u) in path) else 'black' for u, v in
                   graph.edges(data=False)]

    nx.draw_networkx_nodes(graph, pos)
    nx.draw_networkx_edges(graph, pos, edge_color=edge_colors)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)
    nx.draw_networkx_labels(graph, pos)
    plt.show()


def is_full(graph):
    n = len(graph.nodes)
    return all(graph.has_edge(u, v) for u in graph.nodes for v in graph.nodes if u != v)


def check_triangle_sides_condition(graph):
    for clique in nx.enumerate_all_cliques(graph):
        if len(clique) == 3:
            u, v, w = clique
            if (graph[u][v]['weight'] + graph[u][w]['weight'] < graph[v][w]['weight'] or
                    graph[u][v]['weight'] + graph[v][w]['weight'] < graph[u][w]['weight'] or
                    graph[u][w]['weight'] + graph[v][w]['weight'] < graph[u][v]['weight']):
                return False
    return True


def build_multigraph(tree, matching, graph):
    h = nx.MultiGraph(tree)
    for u, v in matching:
        h.add_edge(u, v, weight=graph[u][v]['weight'])
    return h


def find_minimal_matching(graph, odd_nodes):
    subgraph = nx.Graph()
    for i in range(len(odd_nodes)):
        for j in range(1, len(odd_nodes)):
            u, v = odd_nodes[i], odd_nodes[j]
            if graph.has_edge(u, v):
                subgraph.add_edge(u, v, weight=graph[u][v]['weight'])
    return nx.min_weight_matching(subgraph, weight='weight')


def christofides(graph, source):
    plot_graph(graph)

    if not is_full(graph):
        print("Graph is not full")
        return None, "No path possible"

    if not check_triangle_sides_condition(graph):
        print("Triangle sides condition not satisfied")
        return None, "No path possible"

    t = nx.minimum_spanning_tree(graph)
    plot_graph(t)

    odd_nodes = []
    for node in t.nodes:
        if t.degree(node) % 2 != 0:
            odd_nodes.append(node)

    m = find_minimal_matching(graph, odd_nodes)
    h = build_multigraph(t, m, graph)
    plot_graph(h, m)

    eulerian = list(nx.eulerian_circuit(h))
    visited = set()
    path = []
    for u, v in eulerian:
        if u not in visited:
            path.append(u)
            visited.add(u)
        if v not in visited:
            path.append(v)
            visited.add(v)

    path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
    path_edges.append((path[-1], path[0]))
    weight = 0
    for edge in path_edges:
        weight += graph[edge[0]][edge[1]]['weight']

    plot_graph(graph, path_edges)

    if source in path:
        start_index = path.index(source)
        path = path[start_index:] + path[:start_index] + [source]

    path_str = ' -> '.join(path)

    return weight, path_str



