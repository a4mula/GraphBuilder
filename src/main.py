import networkx as nx
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import numpy as np
import json
from src.edge_model import edge_intensity, merged_intensity

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
        weights = [d['weight'] for _, _, d in G.edges(data=True)]
        if weights:
            threshold = sum(weights) / len(weights)
        else:
            threshold = 0
        print(f"Dynamic threshold: {threshold:.2f}")

        # Remove edges below the threshold
        edges_to_remove = [(u, v) for u, v, d in G.edges(data=True) if d['weight'] < threshold]
        for edge in edges_to_remove:
            print(f"Removing edge: {edge} (weight < {threshold:.2f})")
        G.remove_edges_from(edges_to_remove)

        # Reconnect isolated nodes
        reconnect_isolated_nodes(G)

        # Adjust weights and track age
        for u, v, d in G.edges(data=True):
            d['weight'] *= 1.1  # Increase weight by 10%
            d['age'] = d.get('age', 0) + 1  # Increment age
            print(f"Adjusted weight for edge {u} -> {v}: {d['weight']:.2f}, Age: {d['age']}")

def visualize_graph(G, title="Graph Visualization"):
    """Visualize the graph with enhanced visual cues."""
    pos = nx.spring_layout(G)  # Dynamic positions for all nodes

    # Node sizes based on degree
    node_sizes = [700 + (G.degree(node) * 100) for node in G.nodes]

    # Edge colors based on weight
    edge_weights = [d['weight'] for _, _, d in G.edges(data=True)]
    edge_colors = ["red" if weight > 10 else "blue" for weight in edge_weights]

    # Draw graph
    nx.draw(
        G, pos, with_labels=True, node_size=node_sizes, node_color="lightgreen",
        edge_color=edge_colors, width=[w / 10 for w in edge_weights]
    )

    # Add edge weights as labels
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    plt.title(title)
    plt.show()

def visualize_latent_space(G):
    """
    Map the graph to a 2D latent space using t-SNE for dimensionality reduction.
    """
    print("\nMapping graph to latent space...")
    
    # Extract nodes and edge weights to build a feature matrix
    nodes = list(G.nodes)
    feature_matrix = np.zeros((len(nodes), len(nodes)))

    for i, u in enumerate(nodes):
        for j, v in enumerate(nodes):
            if G.has_edge(u, v):
                feature_matrix[i, j] = G[u][v]['weight']

    # Use t-SNE for dimensionality reduction
    perplexity = min(5, len(nodes) - 1)  # Ensure perplexity is valid
    tsne = TSNE(n_components=2, random_state=42, perplexity=perplexity)
    embeddings = tsne.fit_transform(feature_matrix)

    # Plot the latent space
    plt.figure(figsize=(10, 6))
    for i, node in enumerate(nodes):
        plt.scatter(embeddings[i, 0], embeddings[i, 1], label=node)
        plt.text(embeddings[i, 0], embeddings[i, 1], node, fontsize=12)

    plt.title("Latent Space Representation of the Graph")
    plt.legend()
    plt.grid(True)
    plt.show()

def save_iterations(G, iterations=3, output_dir="output"):
    """Save each refinement iteration as a PNG."""
    import os
    os.makedirs(output_dir, exist_ok=True)

    for i in range(iterations):
        refine_graph(G, iterations=1)  # One step of refinement
        filename = os.path.join(output_dir, f"graph_iteration_{i + 1}.png")
        plt.figure()
        visualize_graph(G, title=f"Iteration {i + 1}")
        plt.savefig(filename)
        plt.close()
        print(f"Saved iteration {i + 1} to {filename}")

def main():
    print("Welcome to GraphBuilder!")

    # Load the project graph
    project_file = "src/project_data.json"  # Explicitly specify the correct path
    G = load_project_graph(project_file)

    # Visualize initial graph
    print("Initial Project Graph")
    visualize_graph(G, title="Initial Project Graph")

    # Save iterations
    save_iterations(G, iterations=3)

    # Visualize latent space
    visualize_latent_space(G)

if __name__ == "__main__":
    main()

