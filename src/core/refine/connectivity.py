"""
Connectivity utilities for graph refinement.

Provides functions to reconnect isolated nodes and ensure graph connectivity.
"""

import networkx as nx


def reconnect_isolated_nodes(graph):
    """
    Reconnect isolated nodes or subgraphs to ensure the graph is fully connected.

    Args:
        graph (networkx.DiGraph): The directed graph to process.

    Returns:
        None
    """
    # Identify connected components in the undirected view of the graph
    subgraphs = list(nx.connected_components(graph.to_undirected()))
    if len(subgraphs) <= 1:
        print("Graph is already fully connected.")
        return

    print(f"Found {len(subgraphs)} disconnected subgraphs. Reconnecting...")

    # Sort subgraphs by size (largest first)
    subgraphs.sort(key=len, reverse=True)
    largest_subgraph = subgraphs[0]

    # Connect smaller subgraphs to the largest one
    for subgraph in subgraphs[1:]:
        largest_node = max(largest_subgraph, key=lambda n: graph.degree(n))
        subgraph_node = max(subgraph, key=lambda n: graph.degree(n))
        print(f"Connecting {subgraph_node} to {largest_node}")
        graph.add_edge(subgraph_node, largest_node, weight=1.0, age=0)


def validate_graph_connectivity(graph):
    """
    Ensure the graph is fully connected. Prints a warning if not.

    Args:
        graph (networkx.DiGraph): The directed graph to validate.

    Returns:
        None
    """
    if nx.is_connected(graph.to_undirected()):
        print("Graph is fully connected.")
    else:
        print("Warning: Graph is not fully connected.")

