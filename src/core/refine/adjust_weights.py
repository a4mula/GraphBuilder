"""
Edge weight adjustment utilities for graph refinement.

Provides functions to incrementally adjust edge weights for reinforcement.
"""


def adjust_edge_weights(graph, factor=1.1):
    """
    Incrementally adjust edge weights by a factor to simulate reinforcement.

    Args:
        graph (networkx.DiGraph): The directed graph whose edge weights are to be adjusted.
        factor (float): The multiplier to increment edge weights.

    Returns:
        None
    """
    for u, v, data in graph.edges(data=True):
        old_weight = data.get("weight", 1.0)
        data["weight"] = old_weight * factor
        print(
            f"Adjusted weight for edge {u} -> {v}: {old_weight:.2f} -> {data['weight']:.2f}"
        )

