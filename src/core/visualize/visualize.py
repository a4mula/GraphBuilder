"""
Graph Visualization Module

Handles standard graph visualizations with enhanced visual cues for nodes and edges.
"""

import networkx as nx
import matplotlib.pyplot as plt


def visualize_graph(graph, title="Graph Visualization"):
    """
    Visualize the graph with enhanced visual cues.

    Args:
        graph (networkx.Graph): The graph to visualize.
        title (str): Title of the plot.

    Returns:
        None
    """
    pos = nx.spring_layout(graph)  # Dynamic positions for all nodes

    # Node sizes based on degree
    node_sizes = [700 + (graph.degree(node) * 100) for node in graph.nodes]

    # Edge colors based on weight
    edge_weights = [d['weight'] for _, _, d in graph.edges(data=True)]
    edge_colors = ["red" if weight > 10 else "blue" for weight in edge_weights]

    # Draw graph
    nx.draw(
        graph, pos, with_labels=True, node_size=node_sizes, node_color="lightgreen",
        edge_color=edge_colors, width=[w / 10 for w in edge_weights],
    )

    # Add edge weights as labels
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels)

    plt.title(title)
    filename = f"output/{title.replace(' ', '_').lower()}.png"
    plt.savefig(filename)
    print(f"Graph visualization saved as {filename}")
    plt.show()
