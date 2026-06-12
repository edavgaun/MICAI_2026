import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.lines import Line2D


def draw_network(
    G_filtrado,
    pos_fija,
    institution_country_map,
    df_periodo,
    title,
    selected_institutions=None
):

    if selected_institutions is None:
        selected_institutions = []

    has_focus = len(selected_institutions) > 0

    focus_nodes = set(selected_institutions)

    if has_focus:
        for n in selected_institutions:
            if n in G_filtrado:
                focus_nodes.update(G_filtrado.neighbors(n))

    fig_red, ax_red = plt.subplots(figsize=(20, 11))
    fig_red.subplots_adjust(
        left=0.01,
        right=0.99,
        top=0.93,
        bottom=0.01
    )

    paper_count = (
        df_periodo
        .groupby("institution_clean")["title"]
        .nunique()
        .to_dict()
    )

    all_nodes = list(G_filtrado.nodes())

    sizes_raw = np.array([
        paper_count.get(n, 0)
        for n in all_nodes
    ])

    sizes_log = np.log1p(sizes_raw)

    sizes_norm = (
        sizes_log - sizes_log.min()
    ) / (
        sizes_log.max() - sizes_log.min() + 1e-9
    )

    node_sizes_dict = {
        n: 300 + sizes_norm[i] * 3500
        for i, n in enumerate(all_nodes)
    }

    edges_active = []
    widths_active = []
    colors_active = []

    edges_bg = []
    widths_bg = []
    colors_bg = []

    for u, v in G_filtrado.edges():

        cu = institution_country_map.get(u, "Unknown")
        cv = institution_country_map.get(v, "Unknown")

        w = 1 + np.log1p(
            G_filtrado[u][v]["weight"]
        )

        if cu == "Mexico" and cv == "Mexico":
            edge_color = "tab:green"
        elif cu != "Mexico" and cv != "Mexico":
            edge_color = "lightgray"
        else:
            edge_color = "tab:orange"

        if (
            not has_focus
            or u in selected_institutions
            or v in selected_institutions
        ):
            edges_active.append((u, v))
            widths_active.append(w)
            colors_active.append(edge_color)

        else:
            edges_bg.append((u, v))
            widths_bg.append(w)
            colors_bg.append(edge_color)

    nodes_active = []
    sizes_active = []
    colors_active_nodes = []

    nodes_bg = []
    sizes_bg = []
    colors_bg_nodes = []

    for n in all_nodes:

        n_color = (
            "tab:green"
            if institution_country_map.get(n) == "Mexico"
            else "#EBF6FF"
        )

        n_size = node_sizes_dict[n]

        if not has_focus or n in focus_nodes:
            nodes_active.append(n)
            sizes_active.append(n_size)
            colors_active_nodes.append(n_color)

        else:
            nodes_bg.append(n)
            sizes_bg.append(n_size)
            colors_bg_nodes.append(n_color)

    if has_focus:

        if edges_bg:
            nx.draw_networkx_edges(
                G_filtrado,
                pos_fija,
                edgelist=edges_bg,
                width=widths_bg,
                edge_color=colors_bg,
                alpha=0.02,
                ax=ax_red
            )

        if nodes_bg:
            nx.draw_networkx_nodes(
                G_filtrado,
                pos_fija,
                nodelist=nodes_bg,
                node_size=sizes_bg,
                node_color=colors_bg_nodes,
                edgecolors="black",
                alpha=0.12,
                ax=ax_red
            )

    nx.draw_networkx_edges(
        G_filtrado,
        pos_fija,
        edgelist=edges_active,
        width=widths_active,
        edge_color=colors_active,
        alpha=0.4,
        ax=ax_red
    )

    nx.draw_networkx_nodes(
        G_filtrado,
        pos_fija,
        nodelist=nodes_active,
        node_size=sizes_active,
        node_color=colors_active_nodes,
        edgecolors="black",
        alpha=0.8,
        ax=ax_red
    )

    degree = dict(G_filtrado.degree())

    labels = {}

    for node in G_filtrado.nodes():

        if has_focus:
            if node in focus_nodes:
                labels[node] = node

        else:
            if degree.get(node, 0) >= 4:
                labels[node] = node

    nx.draw_networkx_labels(
        G_filtrado,
        pos_fija,
        labels=labels,
        font_size=9,
        font_weight="bold",
        ax=ax_red
    )

    legend_elements = [
        Line2D(
            [0],
            [0],
            marker='o',
            color='w',
            label='Mexican Institution',
            markerfacecolor='tab:green',
            markersize=12,
            markeredgecolor='black'
        ),
        Line2D(
            [0],
            [0],
            marker='o',
            color='w',
            label='International Institution',
            markerfacecolor='#EBF6FF',
            markersize=12,
            markeredgecolor='black'
        )
    ]

    ax_red.legend(
        handles=legend_elements,
        loc="upper left"
    )

    x_coords = [v[0] for v in pos_fija.values()]
    y_coords = [v[1] for v in pos_fija.values()]

    ax_red.set_xlim(
        min(x_coords) - 0.2,
        max(x_coords) + 0.2
    )

    ax_red.set_ylim(
        min(y_coords) - 0.2,
        max(y_coords) + 0.2
    )

    ax_red.set_title(
        title,
        fontsize=14,
        fontweight="bold"
    )

    ax_red.axis("off")

    return fig_red
