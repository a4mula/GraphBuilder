"""
This module contains utilities for calculating thresholds
for graph refinement operations.
"""

def calculate_threshold(graph, factor=0.5):
    """
    Calculate the dynamic threshold for pruning edges
    based on the average edge weight.

    Args:
        graph (networkx.Graph): The graph to process.
        factor (float): The multiplier for the mean edge weight.

    Returns:
        float: The calculated threshold.
    """
    weights = [data["weight"] for _, _, data in graph.edges(data=True)]
    if not weights:
        print("No edges found in the graph.")
        return 0.0

    mean_weight = sum(weights) / len(weights)
    threshold = mean_weight * factor
    print(f"Calculated dynamic threshold: {threshold:.2f}")
    return threshold


def prune_edges(graph, threshold):
    """
    Remove edges with weights below the specified threshold.

    Args:
        graph (networkx.Graph): The graph to process.
        threshold (float): The threshold value for pruning edges.

    Returns:
        None
    """
    edges_to_remove = [
        (u, v) for u, v, data in graph.edges(data=True)
        if data["weight"] < threshold
    ]
    for edge in edges_to_remove:
        print(
            f"Removing edge {edge} "
            f"(weight={graph[edge[0]][edge[1]]['weight']:.2f} < threshold={threshold:.2f})"
        )
    graph.remove_edges_from(edges_to_remove)

