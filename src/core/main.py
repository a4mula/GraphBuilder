"""
Main entry point for the GraphBuilder application.

This module provides functions for initializing new projects,
analyzing existing ones, and refining their graph structures.
"""

import os
import json
import networkx as nx
from src import (
    refine_graph,
    visualize_graph,
    visualize_latent_space,
    render_clusters,
    edge_intensity,
    find_modules_and_functions,
    display_project_structure,
    find_function_calls,
    build_graph_from_relationships,
)


def load_project_graph(file_path):
    """
    Load nodes and edges from a JSON file to build the project graph.

    Args:
        file_path (str): Path to the JSON file containing graph data.

    Returns:
        networkx.DiGraph: The generated graph.
    """
    print(f"\nLoading project graph from: {file_path}")
    with open(file_path, "r", encoding="utf-8") as file:
        data = json.load(file)

    graph = nx.DiGraph()

    # Add nodes
    nodes = data.get("nodes", [])
    graph.add_nodes_from(nodes)
    print(f"Added nodes: {nodes}")

    # Add edges with weights
    edges = data.get("edges", [])
    for edge in edges:
        weight = edge_intensity(edge.get("frequency", 1), edge.get("amplitude", 1))
        graph.add_edge(edge["from"], edge["to"], weight=weight)
        print(f"Added edge: {edge['from']} -> {edge['to']} (weight={weight})")

    return graph


def analyze_existing_project():
    """
    Analyze an existing project structure, generate relationships, and visualize the graph.

    Returns:
        None
    """
    project_root = input("Enter the path to the project directory (default: src): ") or "src"

    if not os.path.isdir(project_root):
        print(f"Error: Directory '{project_root}' does not exist.")
        return

    print("Analyzing project structure...")
    project_structure = find_modules_and_functions(project_root)
    display_project_structure(project_structure)

    # Gather all function relationships
    all_relationships = []
    for module, functions in project_structure.items():
        module_path = os.path.join(project_root, module.replace(".", os.sep) + ".py")
        if os.path.exists(module_path):
            print(f"Analyzing function calls in {module}...")
            relationships = find_function_calls(module_path, functions)
            all_relationships.extend(relationships)

    # Build a graph from the relationships
    print("\nBuilding graph from relationships...")
    graph = build_graph_from_relationships(all_relationships)

    # Refine the graph through iterative pruning
    refine_graph(graph)

    # Visualize the refined graph
    visualize_graph(graph, title="Refined Function Call Graph")

    # Render clusters
    render_clusters(graph, title="Clustered Function Call Graph")

    # Visualize the latent space graph
    visualize_latent_space(graph, title="Latent Space Function Call Graph")

    # Save the graph to JSON
    save_graph_to_json(graph, "output/function_call_graph.json")


def save_graph_to_json(graph, filename):
    """
    Save the graph structure to a JSON file.

    Args:
        graph (networkx.DiGraph): The graph to save.
        filename (str): Path to the output JSON file.

    Returns:
        None
    """
    graph_data = {
        "nodes": list(graph.nodes),
        "edges": [
            {"from": u, "to": v, "weight": d["weight"]}
            for u, v, d in graph.edges(data=True)
        ],
    }
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(graph_data, file, indent=4)
    print(f"Graph saved to {filename}")


def initialize_new_project():
    """
    Initialize a new project with default nodes and edges.

    Returns:
        None
    """
    print("Initializing a new project...")
    graph = nx.DiGraph()

    # Example of default nodes and edges
    graph.add_nodes_from(["main.py", "utils.py", "edge_model.py"])
    graph.add_edge("main.py", "edge_model.py", weight=10)
    graph.add_edge("edge_model.py", "utils.py", weight=8)

    # Visualize the initial graph
    visualize_graph(graph, title="New Project Graph")


def main():
    """
    Main entry point for the application.

    Returns:
        None
    """
    print("Welcome to GraphBuilder!")
    print("Select an option:")
    print("1. Start a New Project")
    print("2. Analyze an Existing Project")
    choice = input("Enter your choice (1 or 2): ")

    if choice == "1":
        initialize_new_project()
    elif choice == "2":
        analyze_existing_project()
    else:
        print("Invalid choice. Exiting...")


if __name__ == "__main__":
    main()

