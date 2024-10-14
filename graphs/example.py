from graphs.createGraph import create_graph

graph = create_graph("data.txt")
graph.plot_graph()
print('Min degree:', graph.get_min_degree())
print('Max degree:', graph.get_max_degree())
print('Even degrees:', graph.get_even_degrees())
print('Odd degrees:', graph.get_odd_degrees())
print('Sorted degrees:', graph.get_degrees())
print('Degree of node f:', graph.get_degree("f"))
