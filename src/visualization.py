import matplotlib.pyplot as plt
import networkx as nx

def draw_network(G, pos, node_sizes, node_colors, edge_colors, edge_widths, labels=None):

    fig, ax = plt.subplots(figsize=(16, 12))

    # EDGES (esto es clave)
    nx.draw_networkx_edges(
        G, pos,
        ax=ax,
        width=edge_widths,
        edge_color=edge_colors,
        alpha=0.5
    )

    # NODES
    nx.draw_networkx_nodes(
        G, pos,
        ax=ax,
        node_size=node_sizes,
        node_color=node_colors,
        edgecolors="black",
        alpha=0.8
    )

    # LABELS (ANTES NO LOS ESTABAS DIBUJANDO)
    if labels:
        nx.draw_networkx_labels(
            G,
            pos,
            labels=labels,
            ax=ax,
            font_size=9,
            font_weight="bold"
        )

    ax.set_axis_off()

    return fig
