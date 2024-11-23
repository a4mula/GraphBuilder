import networkx as nx
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import numpy as np
import json
import os
from src.edge_model import edge_intensity, merged_intensity
from extract_structure import (
    find_modules_and_functions,
    display_project_structure,
    find_function_calls,
    build_graph_from_relationships
)


def load_project_graph(file_path):
    """
    Load nodes and edges from a JSON file to build the project graph.
    """
    print(f"\nLoading project graph from: {file_path}")
    with open(file_path, "r") as f:
        data = json.load(f)

    G = nx.DiGraph()

    # Add nodes
    nodes = data.get("nodes", [])
    G.add_nodes_from(nodes)
    print(f"Added nodes: {nodes}")

    # Add edges with weights
    edges = data.get("edges", [])
    for edge in edges:
        freq = edge.get("frequency", 1)
        amp = edge.get("amplitude", 1)
        weight = edge_intensity(freq, amp)
        G.add_edge(edge["from"], edge["to"], weight=weight)
        print(f"Added edge: {edge['from']} -> {edge['to']} (weight={weight})")

    return G


def reconnect_isolated_nodes(G):
    """
    Reconnect isolated nodes to the node with the highest out-degree.
    """
    isolated_nodes = [node for node in G.nodes if G.degree(node) == 0]
    if not isolated_nodes:
        return

    # Find the node with the highest out-degree
    target_node = max(G.nodes, key=lambda n: G.out_degree(n))
    for node in isolated_nodes:
        print(f"Reconnecting isolated node {node} to {target_node}")
        G.add_edge(node, target_node, weight=1.0, age=0)  # Default weight and reset age


def refine_graph(G, iterations=3):
    """
    Refine the graph by adjusting edge weights, reconnecting nodes,
    and dynamically recalculating thresholds.
    """
    for i in range(iterations):
        print(f"\nIteration {i + 1}: Refining graph...")

        # Calculate mean edge weight as dynamic threshold
        weights = [d["weight"] for _, _, d in G.edges(data=True)]
        if weights:
            threshold = sum(weights) / len(weights)
        else:
            threshold = 0
        print(f"Dynamic threshold: {threshold:.2f}")

        # Remove edges below the threshold
        edges_to_remove = [(u, v) for u, v, d in G.edges(data=True) if d["weight"] < threshold]
        for edge in edges_to_remove:
            print(f"Removing edge: {edge} (weight < {threshold:.2f})")
        G.remove_edges_from(edges_to_remove)

        # Reconnect isolated nodes
        reconnect_isolated_nodes(G)

        # Adjust weights and track age
        for u, v, d in G.edges(data=True):
            d["weight"] *= 1.1  # Increase weight by 10%
            d["age"] = d.get("age", 0) + 1  # Increment age
            print(f"Adjusted weight for edge {u} -> {v}: {d['weight']:.2f}, Age: {d['age']}")


def visualize_graph(G, title="Graph Visualization"):
    """Visualize the graph with enhanced visual cues."""
    pos = nx.spring_layout(G)  # Dynamic positions for all nodes

    # Node sizes based on degree
    node_sizes = [700 + (G.degree(node) * 100) for node in G.nodes]

    # Edge colors based on weight
    edge_weights = [d["weight"] for _, _, d in G.edges(data=True)]
    edge_colors = ["red" if weight > 10 else "blue" for weight in edge_weights]

    # Draw graph
    nx.draw(
        G,
        pos,
        with_labels=True,
        node_size=node_sizes,
        node_color="lightgreen",
        edge_color=edge_colors,
        width=[w / 10 for w in edge_weights],
    )

    # Add edge weights as labels
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.title(title)
    plt.show()


def analyze_existing_project():
    """
    Analyze an existing project structure, generate relationships, and visualize the graph.
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
    G = build_graph_from_relationships(all_relationships)

    # Visualize the graph
    visualize_graph(G, title="Function Call Graph")
    save_graph_to_json(G, "output/function_call_graph.json")


def save_graph_to_json(G, filename):
    graph_data = {
        "nodes": list(G.nodes),
        "edges": [
            {"from": u, "to": v, "weight": d["weight"]}
            for u, v, d in G.edges(data=True)
        ],
    }
    with open(filename, "w") as f:
        json.dump(graph_data, f, indent=4)
    print(f"Graph saved to {filename}")


def initialize_new_project():
    print("Initializing a new project...")
    G = nx.DiGraph()

    # Example of default nodes and edges
    G.add_nodes_from(["main.py", "utils.py", "edge_model.py"])
    G.add_edge("main.py", "edge_model.py", weight=10)
    G.add_edge("edge_model.py", "utils.py", weight=8)

    # Visualize the initial graph
    visualize_graph(G, title="New Project Graph")


def main():
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

