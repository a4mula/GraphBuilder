import networkx as nx
import matplotlib.pyplot as plt
from src.edge_model import unidirectional_wave, edge_intensity, merged_intensity

def main():
    print("Welcome to GraphBuilder!")

    # Create a directed graph
    G = nx.DiGraph()

    # Add nodes
    G.add_nodes_from(["A", "B", "C", "D"])

    # Define relationships with intensities
    freq_a_b, amp_a_b = 5, 2
    freq_b_a, amp_b_a = 3, 4
    freq_b_d, amp_b_d = 2, 5
    freq_c_d, amp_c_d = 1, 3

    # Add bi-directional edge: A <-> B
    intensity_a_b = merged_intensity(freq_a_b, amp_a_b, freq_b_a, amp_b_a)
    G.add_edge("A", "B", weight=intensity_a_b)
    G.add_edge("B", "A", weight=intensity_a_b)

    # Add directional edges
    intensity_b_d = edge_intensity(freq_b_d, amp_b_d)
    intensity_c_d = edge_intensity(freq_c_d, amp_c_d)
    G.add_edge("B", "D", weight=intensity_b_d)
    G.add_edge("C", "D", weight=intensity_c_d)

    # Visualize the graph
    visualize_graph(G)

def visualize_graph(G):
    """Visualize the graph with matplotlib."""
    pos = nx.spring_layout(G)  # Positions for all nodes

    # Draw nodes and edges
    nx.draw(G, pos, with_labels=True, node_size=700, node_color="lightblue")
    
    # Add edge weights as labels
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    # Adjust edge thickness based on weight
    edges = G.edges(data=True)
    nx.draw_networkx_edges(
        G, pos, edgelist=edges,
        width=[d['weight'] / 10 for _, _, d in edges]  # Scale edge thickness
    )

    plt.title("Graph Visualization with Edge Intensities")
    plt.show()

if __name__ == "__main__":
    main()

