from graphs.createGraph import create_graph
from vertex_cover.main import vertex_cover

graph = create_graph("../data.txt")
graph.plot_graph()
vertex_cover(graph)
