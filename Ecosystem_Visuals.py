import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from matplotlib.lines import Line2D
import streamlit as st

def draw_network_graph(G_filtrado, pos_fija, institution_country_map, df_periodo, has_focus, focus_nodes, selected_institutions):
    """Generates and displays the localized NetworkX collaboration map."""
    fig_red, ax_red = plt.subplots(figsize=(20, 11))
    fig_red.subplots_adjust(left=0.01, right=0.99, top=0.93, bottom=0.01)

    paper_count = df_periodo.groupby('institution_clean')['title'].nunique().to_dict()
    edges_active, widths_active, colors_active = [], [], []
    edges_bg, widths_bg, colors_bg = [], [], []

    for u, v in G_filtrado.edges():
        cu = institution_country_map.get(u, "Unknown")
        cv = institution_country_map.get(v, "Unknown")
        w = 1 + np.log1p(G_filtrado[u][v]["weight"])
        
        edge_color = "tab:green" if cu == "Mexico" and cv == "Mexico" else "lightgray" if cu != "Mexico" and cv != "Mexico" else "tab:orange"
        
        if not has_focus or (u in selected_institutions or v in selected_institutions):
            edges_active.append((u, v))
            widths_active.append(w)
            colors_active.append(edge_color)
        else:
            edges_bg.append((u, v))
            widths_bg.append(w)
            colors_bg.append(edge_color)

    nodes_active, sizes_active, colors_active_nodes = [], [], []
    nodes_bg, sizes_bg, colors_bg_nodes = [], [], []

    all_nodes = list(G_filtrado.nodes())
    if all_nodes:
        sizes_raw = np.array([paper_count.get(n, 0) for n in all_nodes])
        sizes_log = np.log1p(sizes_raw)
        sizes_norm = (sizes_log - sizes_log.min()) / (sizes_log.max() - sizes_log.min() + 1e-9)
        node_sizes_dict = {n: 300 + sizes_norm[i] * 3500 for i, n in enumerate(all_nodes)}
        
        for n in all_nodes:
            n_color = "tab:green" if institution_country_map.get(n, "Unknown") == "Mexico" else "#EBF6FF"
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
        if edges_bg: nx.draw_networkx_edges(G_filtrado, pos_fija, edgelist=edges_bg, width=widths_bg, edge_color=colors_bg, alpha=0.02, ax=ax_red)
        if nodes_bg: nx.draw_networkx_nodes(G_filtrado, pos_fija, nodelist=nodes_bg, node_size=sizes_bg, node_color=colors_bg_nodes, edgecolors='black', alpha=0.12, ax=ax_red)
    
    if edges_active: nx.draw_networkx_edges(G_filtrado, pos_fija, edgelist=edges_active, width=widths_active, edge_color=colors_active, alpha=0.4, ax=ax_red)
    if nodes_active: nx.draw_networkx_nodes(G_filtrado, pos_fija, nodelist=nodes_active, node_size=sizes_active, node_color=colors_active_nodes, edgecolors='black', alpha=0.8, ax=ax_red)

    degree = dict(G_filtrado.degree())
    labels = {node: node for node in G_filtrado.nodes() if (has_focus and node in focus_nodes) or (not has_focus and degree.get(node, 0) >= 4)}
    nx.draw_networkx_labels(G_filtrado, pos_fija, labels=labels, font_size=9, font_weight='bold', ax=ax_red)

    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Mexican Institution', markerfacecolor='tab:green', markersize=12, markeredgecolor='black'),
        Line2D([0], [0], marker='o', color='w', label='International Institution', markerfacecolor='#EBF6FF', markersize=12, markeredgecolor='black'),
        Line2D([0], [0], color='tab:green', lw=3, label='Mexico ↔ Mexico'),
        Line2D([0], [0], color='tab:orange', lw=3, label='Mexico ↔ International')
    ]
    ax_red.legend(handles=legend_elements, loc='upper left', fontsize=11, title='Collaboration Type')

    x_coords = [coords[0] for coords in pos_fija.values()]
    y_coords = [coords[1] for coords in pos_fija.values()]
    ax_red.set_xlim(min(x_coords) - 0.2, max(x_coords) + 0.2)
    ax_red.set_ylim(min(y_coords) - 0.2, max(y_coords) + 0.2)

    mexican_nodes = sum(institution_country_map.get(n) == "Mexico" for n in G_filtrado.nodes())
    international_nodes = G_filtrado.number_of_nodes() - mexican_nodes
    ax_red.set_title(f"Institutions: {G_filtrado.number_of_nodes()} (Mex: {mexican_nodes} | Int: {international_nodes}) | Edges: {G_filtrado.number_of_edges()}", fontsize=14, fontweight='bold')
    ax_red.axis("off")
    
    st.pyplot(fig_red, use_container_width=True)

def draw_volume_bars(df_periodo, institution_country_map, has_focus, focus_nodes):
    """Generates and displays the Top 10 frequency bar chart."""
    top_instituciones = df_periodo['institution_clean'].value_counts().head(10)

    if not top_instituciones.empty:
        fig_barras, ax_barras = plt.subplots(figsize=(4, 5))
        y_labels = top_instituciones.index[::-1]
        x_values = top_instituciones.values[::-1]
        
        bar_colors = ["tab:green" if institution_country_map.get(inst, "Unknown") == "Mexico" else "#EBF6FF" for inst in y_labels]
        bar_alphas = [1.0 if not has_focus or inst in focus_nodes else 0.15 for inst in y_labels]
        
        bars = ax_barras.barh(y_labels, x_values, color=bar_colors, edgecolor='black', height=0.5)
        for i, bar in enumerate(bars): bar.set_alpha(bar_alphas[i])
        
        ax_barras.tick_params(axis='both', labelsize=10)
        ax_barras.spines['top'].set_visible(False)
        ax_barras.spines['right'].set_visible(False)
        ax_barras.spines['left'].set_color('#cccccc')
        ax_barras.spines['bottom'].set_color('#cccccc')
        
        ax_barras.bar_label(bars, padding=5, fontsize=10, fontweight='bold', color='#333333')
        ax_barras.xaxis.grid(True, linestyle='--', alpha=0.3, color='#999999')
        ax_barras.set_axisbelow(True)
        
        fig_barras.tight_layout()
        st.pyplot(fig_barras, use_container_width=True)
