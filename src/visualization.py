import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from matplotlib.lines import Line2D

def draw_network(G, pos, df_periodo, institution_country_map, etapa_titulo, year, area, mexican_nodes, international_nodes):
    fig, ax = plt.subplots(figsize=(16, 12))

    # 1. Tamaño de nodos (Logarítmico)
    paper_count = df_periodo.groupby('institution_clean')['title'].nunique().to_dict()
    sizes_raw = np.array([paper_count.get(n, 0) for n in G.nodes()])
    sizes_log = np.log1p(sizes_raw)
    
    if sizes_log.max() - sizes_log.min() == 0:
        node_sizes = np.full_like(sizes_raw, 300)
    else:
        sizes_norm = (sizes_log - sizes_log.min()) / (sizes_log.max() - sizes_log.min() + 1e-9)
        node_sizes = 300 + sizes_norm * 3500

    # 2. Color de nodos
    node_colors = [
        "tab:green" if institution_country_map.get(n, "Unknown") == "Mexico" else "#EBF6FF"
        for n in G.nodes()
    ]

    # 3. Aristas
    edge_widths = [1 + np.log1p(G[u][v]["weight"]) for u, v in G.edges()]
    edge_colors = []
    for u, v in G.edges():
        cu = institution_country_map.get(u, "Unknown")
        cv = institution_country_map.get(v, "Unknown")
        if cu == "Mexico" and cv == "Mexico":
            edge_colors.append("tab:green")
        elif cu != "Mexico" and cv != "Mexico":
            edge_colors.append("lightgray")
        else:
            edge_colors.append("tab:orange")

    # 4. Dibujar elementos
    nx.draw_networkx_edges(G, pos, width=edge_widths, edge_color=edge_colors, alpha=0.5, ax=ax)
    nx.draw_networkx_nodes(G, pos, node_size=node_sizes, node_color=node_colors, edgecolors='black', alpha=0.7, ax=ax)

    # 5. Etiquetas (Grado >= 4)
    degree = dict(G.degree())
    labels = {node: node for node, deg in degree.items() if deg >= 4}
    nx.draw_networkx_labels(G, pos, labels=labels, font_size=10, font_weight='bold', ax=ax)

    # 6. Leyendas y Títulos
    legend_elements = [
        Line2D([0], [0], color='tab:green', lw=3, label='Mexico ↔ Mexico'),
        Line2D([0], [0], color='tab:orange', lw=3, label='Mexico ↔ International'),
        Line2D([0], [0], color='lightgray', lw=3, label='International ↔ International')
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=12, title='Type of Collaboration', title_fontsize=14)

    ax.set_title(
        f"{etapa_titulo}\n\n"
        f"Year: {year} | Area: {area} | Institutions: {G.number_of_nodes()} |\n"
        f"Mexicans: {mexican_nodes} | Internationals: {international_nodes} | Collaborations: {G.number_of_edges()}",
        fontsize=16
    )
    ax.axis("off")
    fig.tight_layout()
    return fig
