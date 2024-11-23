"""
Clustering Visualization Module

Handles clustering analysis and visualization for graphs using
Spectral Clustering or other clustering algorithms.
"""

import matplotlib.pyplot as plt
import networkx as nx
from sklearn.cluster import SpectralClustering


def render_clusters(graph, title="Clustered Function Call Graph"):
    """
    Render clusters in the graph using Spectral Clustering.

    Args:
        graph (networkx.Graph): The graph to cluster and visualize.
        title (str): Title of the plot.

    Returns:
        None
    """
    print("Performing spectral clustering on the graph...")

    adjacency_matrix = nx.adjacency_matrix(graph).toarray()
    adjacency_matrix = (adjacency_matrix + adjacency_matrix.T) / 2
    print("Symmetrized adjacency matrix.")

    clustering = SpectralClustering(n_clusters=3, affinity="precomputed", random_state=42)
    labels = clustering.fit_predict(adjacency_matrix)
    print(f"Clustering labels: {labels}")

    pos = nx.spring_layout(graph)
    plt.figure(figsize=(10, 6))
    nx.draw_networkx_nodes(graph, pos, node_size=700, cmap=plt.cm.Set1, node_color=labels)
    nx.draw_networkx_edges(graph, pos, alpha=0.5)
    nx.draw_networkx_labels(graph, pos, font_size=10)
    plt.title(title)

    filename = f"output/{title.replace(' ', '_').lower()}.png"
    plt.savefig(filename)
    print(f"Clustered graph saved as {filename}")
    plt.show()
