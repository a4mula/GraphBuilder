"""
Graph refinement utilities.

Provides the main logic for refining a graph, including pruning, 
reconnecting isolated nodes, and validating connectivity.
"""

from .adjust_weights import adjust_edge_weights
from .connectivity import reconnect_isolated_nodes, validate_graph_connectivity
from .thresholding import prune_edges, calculate_threshold


def refine_graph(graph, threshold_factor=0.5, weight_factor=1.1):
    """
    Refine the graph by pruning weak edges, reconnecting isolated nodes, 
    and adjusting weights. Includes connectivity validation.

    Args:
        graph (networkx.DiGraph): The directed graph to be refined.
        threshold_factor (float): Factor to compute the pruning threshold.
        weight_factor (float): Multiplier to increment edge weights.

    Returns:
        None
    """
    if graph.number_of_edges() == 0:
        print("No edges to refine.")
        return

    # Calculate the dynamic threshold using the graph
    threshold = calculate_threshold(graph, threshold_factor)
    print(f"Dynamic threshold: {threshold:.2f}")

    # Apply the refinement steps
    prune_edges(graph, threshold)
    reconnect_isolated_nodes(graph)
    adjust_edge_weights(graph, factor=weight_factor)
    validate_graph_connectivity(graph)

