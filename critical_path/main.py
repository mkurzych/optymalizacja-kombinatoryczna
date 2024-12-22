import networkx as nx
import matplotlib.pyplot as plt
from prettytable import PrettyTable
import itertools as it


def create_task(task_id, duration, predecessors=None):
    return {
        'id': task_id,
        'duration': duration,
        'predecessors': predecessors or []
    }


def build_network(tasks):
    g = nx.DiGraph()

    for task_id, task in tasks.items():
        g.add_node(task_id, duration=task['duration'])

    for task_id, task in tasks.items():
        if task['predecessors']:
            for pred in task['predecessors']:
                g.add_edge(pred, task_id)

    return g


def calculate_network_properties(tasks, graph):
   # najwcześniejszy czas startu
    earliest_start_times = {}
    sorted_nodes = list(nx.topological_sort(graph))

    for node in sorted_nodes:
        predecessors = list(graph.predecessors(node))

        if not predecessors:
            earliest_start_times[node] = 0
        else:
            max_predecessor_finish = max(
                earliest_start_times[pred] + tasks[pred]['duration']
                for pred in predecessors
            )
            earliest_start_times[node] = max_predecessor_finish

    # długość uszeregowania
    project_duration = max(
        earliest_start_times[node] + tasks[node]['duration']
        for node in graph.nodes
    )

    # najpóźniejszy czas startu
    latest_start_times = {}
    sorted_nodes_reversed = list(reversed(list(nx.topological_sort(graph))))

    for node in sorted_nodes_reversed:
        successors = list(graph.successors(node))

        if not successors:
            latest_start_times[node] = project_duration - tasks[node]['duration']
        else:
            min_successor_start = min(
                latest_start_times[s] - tasks[node]['duration']
                for s in successors
            )
            latest_start_times[node] = min_successor_start

    critical_path = [
        node for node, task in tasks.items()
        if (latest_start_times[node] == earliest_start_times[node])
    ]

    return earliest_start_times, latest_start_times, critical_path, project_duration


def get_schedule(tasks, earliest_start_times):
    return {
        task_id: (
            earliest_start_times[task_id],
            earliest_start_times[task_id] + task['duration']
        )
        for task_id, task in tasks.items()
    }


def visualize_network(graph, tasks, critical_path):
    plt.figure(figsize=(14, 10))
    connectionstyle = [f"arc3,rad={r}" for r in it.accumulate([0.15] * 4)]
    pos = nx.spring_layout(graph, k=1.5, iterations=50)

    nx.draw(
        graph,
        pos,
        node_color=['red' if node in critical_path else 'skyblue' for node in graph.nodes],
        node_size=2500,
        font_size=10,
        font_weight="bold",
        edge_color='black',
        width=1.5,
        connectionstyle=connectionstyle
    )

    labels = {
        node: f"{node}, {tasks[node]['duration']}"
        for node in graph.nodes
    }
    nx.draw_networkx_labels(graph, pos, labels, font_size=9, font_weight="bold")
    plt.axis('off')
    plt.show()
    plt.close()


def create_gantt_chart(schedule, critical_path):

    task_assignments = []
    task_to_machine = {}

    for task_id, (start, end) in sorted(schedule.items(), key=lambda x: x[1][0]):
        for machine_idx, machine_tasks in enumerate(task_assignments):
            if all(end <= t_start or start >= t_end for t_start, t_end in machine_tasks):
                machine_tasks.append((start, end))
                task_to_machine[task_id] = machine_idx
                break
        else:
            task_assignments.append([(start, end)])
            task_to_machine[task_id] = len(task_assignments) - 1

    plt.figure(figsize=(12, 6))

    for task_id, (start, end) in schedule.items():
        machine_idx = task_to_machine[task_id]
        color = 'red' if task_id in critical_path else 'skyblue'

        plt.barh(machine_idx, end - start, left=start, color=color, edgecolor='black', align='center', alpha=0.8)

        plt.text(start + (end - start) / 2, machine_idx, f"{task_id}, {end - start}",
                 ha='center', va='center', color='white', fontweight='bold')

    plt.xlabel("Czas")
    plt.ylabel("Maszyny")
    plt.yticks(range(len(task_assignments)), [f"{i + 1}" for i in range(len(task_assignments))])
    plt.grid(axis='x', linestyle='--', alpha=0.7)
    plt.show()
    plt.close()


def print_analysis(tasks, earliest_start_times, latest_start_times, critical_path, project_duration):
    print("=== Analiza Ścieżki Krytycznej ===\n")

    project_table = PrettyTable()
    project_table.field_names = ["Całkowity czas trwania projektu"]
    project_table.add_row([project_duration])
    print(project_table)

    print()
    critical_path_table = PrettyTable()
    critical_path_table.field_names = ["Zadania na ścieżce krytycznej"]
    critical_path_table.add_row([", ".join(critical_path)])
    print(critical_path_table)

    print("\nSzczegóły zadań:")
    table = PrettyTable()
    table.field_names = ["Zadanie", "Czas trwania", "Najwcześniejszy start", "Najpóźniejszy start", "Rezerwa czasu"]

    for task_id in tasks:
        duration = tasks[task_id]['duration']
        earliest_start = earliest_start_times[task_id]
        latest_start = latest_start_times[task_id]
        slack = latest_start - earliest_start
        table.add_row([task_id, duration, earliest_start, latest_start, slack])

    print(table)


def analyze_critical_path(tasks):
    graph = build_network(tasks)

    earliest_start_times, latest_start_times, critical_path, project_duration = (
        calculate_network_properties(tasks, graph)
    )

    print_analysis(tasks, earliest_start_times, latest_start_times, critical_path, project_duration)

    visualize_network(graph, tasks, critical_path)

    schedule = get_schedule(tasks, earliest_start_times)
    create_gantt_chart(schedule, critical_path)

    return earliest_start_times, latest_start_times, critical_path, project_duration


def parse_data(file_path):
    tasks = {}
    with open(file_path, 'r') as file:
        data = file.readlines()
        for line in data:
            parts = line.strip().split()
            task = parts[0]
            duration = int(parts[1])
            dependencies = parts[2:] if len(parts) > 2 else []
            tasks[task] = create_task(task, duration, dependencies)
    return tasks


def example_usage():

    tasks = parse_data('data.txt')
    analyze_critical_path(tasks)


example_usage()