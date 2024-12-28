import networkx as nx
import matplotlib.pyplot as plt
import itertools as it


def identify_graph_type(graph):
    in_degrees = dict(graph.in_degree())
    out_degrees = dict(graph.out_degree())

    roots = [node for node, deg in in_degrees.items() if deg == 0]
    leaves = [node for node, deg in out_degrees.items() if deg == 0]

    one_parent = all(deg == 1 for node, deg in in_degrees.items() if node not in roots)
    one_child = all(deg == 1 for node, deg in out_degrees.items() if node not in leaves)

    if not nx.is_directed_acyclic_graph(graph):
        return "invalid", None

    if len(roots) == 1 and len(leaves) >= 1 and one_parent:
        return "out-tree", roots[0]
    elif len(leaves) == 1 and len(roots) >= 1 and one_child:
        return "in-tree", leaves[0]
    elif len(roots) > 1 and one_parent:
        return "out-forest", roots
    elif len(leaves) > 1 and one_child:
        return "in-forest", leaves
    else:
        return "invalid", None


def add_super_root(graph, roots):
    super_root = "super_root"
    graph.add_node(super_root)
    for root in roots:
        graph.add_edge(root, super_root)
    return super_root


def flip_graph(graph):
    return graph.reverse(copy=True)


def build_network(tasks):
    g = nx.DiGraph()
    for (task_id, pred) in tasks:
        g.add_node(task_id)
    for (task_id, preds) in tasks:
        if preds:
            for pred in preds:
                g.add_edge(pred, task_id)
    return g


def visualize_network(graph):
    plt.figure(figsize=(14, 10))
    connectionstyle = [f"arc3,rad={r}" for r in it.accumulate([0.15] * 4)]
    pos = nx.nx_agraph.graphviz_layout(graph, prog='dot')

    nx.draw(
        graph,
        pos,
        node_color='skyblue',
        node_size=2500,
        font_size=10,
        font_weight="bold",
        edge_color='black',
        width=1.5,
        connectionstyle=connectionstyle
    )
    try:
        labels = {
            node: f"{node}\nl: {graph.nodes[node]['level']}"
            for node in graph.nodes
        }
        nx.draw_networkx_labels(graph, pos, labels, font_size=9, font_weight="bold")
    except KeyError:
        labels = {node: node for node in graph.nodes}
        nx.draw_networkx_labels(graph, pos, labels, font_size=9, font_weight="bold")
    plt.axis('off')
    plt.show()
    plt.close()


def create_gantt_chart(time_slots, m, mirror=False, ignore_node=None):
    task_times = {}
    for time_idx, tasks in enumerate(time_slots):
        for task in tasks:
            if task == ignore_node:
                continue
            if task not in task_times:
                task_times[task] = {'start': time_idx, 'end': time_idx + 1}
            else:
                task_times[task]['end'] = time_idx + 1

    if mirror:
        max_time = max(times['end'] for times in task_times.values())
        for task in task_times:
            old_start = task_times[task]['start']
            old_end = task_times[task]['end']
            task_times[task]['start'] = max_time - old_end
            task_times[task]['end'] = max_time - old_start

    task_to_machine = {}
    current_machine = 0
    sorted_tasks = sorted(task_times.items(), key=lambda x: (x[1]['start'], x[0]))

    for task, _ in sorted_tasks:
        task_to_machine[task] = current_machine
        current_machine = (current_machine + 1) % m

    plt.figure(figsize=(12, 6))
    for task, times in task_times.items():
        machine_idx = task_to_machine[task]
        duration = times['end'] - times['start']
        plt.barh(machine_idx, duration, left=times['start'],
                 color='skyblue', edgecolor='black',
                 align='center', alpha=0.8)
        plt.text(times['start'] + duration / 2, machine_idx,
                 f"{task}", ha='center', va='center',
                 color='white', fontweight='bold')

    plt.xlabel("Time")
    plt.ylabel("Machines")
    plt.yticks(range(m), [f"Machine {i + 1}" for i in range(m)])
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    max_time = max(times['end'] for times in task_times.values())
    plt.xlim(-0.1, max_time + 0.1)
    plt.tight_layout()
    plt.show()
    plt.close()


def label_tree_levels(graph, root=None):
    nodes = graph.nodes()
    roots = [node for node, out_degree in graph.out_degree() if out_degree == 0]

    if root is not None:
        roots = [root]

    layers = list(nx.bfs_layers(graph.to_undirected(), roots))

    for i in range(len(layers)):
        for node in layers[i]:
            graph.nodes[node]['level'] = i

    print(layers)

    return graph


def parse_data(file_path):
    tasks = []
    with open(file_path, 'r') as file:
        data = file.readlines()
        for line in data:
            parts = line.strip().split()
            task = parts[0]
            dependencies = parts[1:] if len(parts) > 1 else []
            tasks.append((task, dependencies))

    return tasks


def hu_algorithm(graph):
    t = 0
    diagram = []

    while graph.nodes:
        busy = 0
        print(f"Time: {t}")
        to_remove = []
        sorted_nodes = sorted(graph.nodes(data=True),
                              key=lambda x: x[1]['level'],
                              reverse=True)

        for task in sorted_nodes:
            if graph.in_degree(task[0]) == 0 and busy < m:
                busy += 1
                print(f"Task {task[0]} started, level: {task[1]['level']}")
                to_remove.append(task)

        temp = []
        for task in to_remove:
            temp.append(task[0])
            graph.remove_node(task[0])
        diagram.append(temp)

        if graph.nodes:
            visualize_network(graph)

        t += 1

    return diagram


def main():
    data = input("Enter the file path: ")
    m = int(input("Enter the number of machines: "))
    tasks = parse_data(data)
    original_graph = build_network(tasks)

    visualize_network(original_graph)

    graph_type, special_node = identify_graph_type(original_graph)

    if graph_type == "invalid":
        print("Error: Input graph must be an in-tree, out-tree, in-forest, or out-forest")
        return

    print(f"Detected graph type: {graph_type}")

    working_graph = original_graph.copy()
    mirror_gantt = False
    ignore_super_root = None

    if graph_type == "out-tree":
        working_graph = flip_graph(working_graph)
        mirror_gantt = True
    elif graph_type == "in-forest":
        ignore_super_root = add_super_root(working_graph, special_node)
    elif graph_type == "out-forest":
        working_graph = flip_graph(working_graph)
        ignore_super_root = add_super_root(working_graph, special_node)
        mirror_gantt = True

    if ignore_super_root:
        working_graph = label_tree_levels(working_graph, "super_root")
    else:
        working_graph = label_tree_levels(working_graph)

    visualize_network(working_graph)

    diagram = hu_algorithm(working_graph)

    create_gantt_chart(diagram, m, mirror=mirror_gantt, ignore_node=ignore_super_root)


if __name__ == "__main__":
    main()
