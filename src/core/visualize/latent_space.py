"""
Latent Space Visualization Module

Handles 2D projections of graph structures into a latent space 
using dimensionality reduction techniques like t-SNE.
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE


def visualize_latent_space(graph, title="Latent Space Graph"):
    """
    Map the graph to a 2D latent space using t-SNE for dimensionality reduction.

    Args:
        graph (networkx.Graph): The graph to visualize in latent space.
        title (str): Title of the plot.

    Returns:
        None
    """
    print("\nMapping graph to latent space...")
    
    nodes = list(graph.nodes)
    feature_matrix = np.zeros((len(nodes), len(nodes)))

    for i, u in enumerate(nodes):
        for j, v in enumerate(nodes):
            if graph.has_edge(u, v):
                feature_matrix[i, j] = graph[u][v]['weight']

    perplexity = min(5, len(nodes) - 1)
    tsne = TSNE(n_components=2, random_state=42, perplexity=perplexity)
    embeddings = tsne.fit_transform(feature_matrix)

    plt.figure(figsize=(10, 6))
    for i, node in enumerate(nodes):
        plt.scatter(embeddings[i, 0], embeddings[i, 1], label=node)
        plt.text(embeddings[i, 0], embeddings[i, 1], node, fontsize=12)

    plt.title(title)
    plt.legend()
    plt.grid(True)

    filename = f"output/{title.replace(' ', '_').lower()}.png"
    plt.savefig(filename)
    print(f"Latent space graph saved as {filename}")

    plt.show()
