import matplotlib.pyplot as plt
import networkx as nx

def draw_network(G, pos, node_sizes, node_colors, edge_colors, edge_widths, labels=None):

    plt.figure(figsize=(16, 12))

    nx.draw_networkx_edges(
        G, pos,
        width=edge_widths,
        edge_color=edge_colors,
        alpha=0.5
    )

    nx.draw_networkx_nodes(
        G, pos,
        node_size=node_sizes,
        node_color=node_colors,
        edgecolors="black",
        alpha=0.7
    )

    if labels:
        nx.draw_networkx_labels(G, pos, labels=labels, font_size=9)

    plt.axis("off")
    return plt
