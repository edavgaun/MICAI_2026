import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.lines import Line2D

# Importamos la carga de datos del setup y los cálculos matemáticos de tu utilería de red
from pages.Ecosystem_Setup import load_clean_data
from pages.Network_Utils import build_network, calcular_layout_fijo

# ==============================================================================
# INTERFAZ DE USUARIO Y RENDERIZADO
# ==============================================================================
st.title("🕸️ Collaboration Network Discovery")
st.markdown("---")

# Carga de datos y cálculo seguro de posiciones fijas
df_final = load_clean_data()
pos_fija = calcular_layout_fijo(df_final)

# Mapeos y extracción de filtros
institution_country_map = (
    df_final[['institution_clean', 'Country']]
    .dropna()
    .drop_duplicates()
    .groupby('institution_clean')['Country']
    .first()
    .to_dict()
)
areas = sorted(df_final['research_area'].dropna().unique())

def obtener_etapa(year):
    if year <= 2008: return "Era 1: The Islands (1997–2008)"
    elif year <= 2019: return "Era 2: The Bridges (2009–2019)"
    elif year <= 2022: return "Era 3: Forced Virtualization (2020–2022)"
    else: return "Era 4: Solid Networks (2023–2026)"

# Filtros en la barra lateral
st.sidebar.header("Network Controls")
slider_year = st.sidebar.slider("Select Year Cutoff:", int(df_final.year.min()), int(df_final.year.max()), int(df_final.year.max()))
dropdown_area = st.sidebar.selectbox("Research Area:", ['All Areas'] + areas)

# Filtrado de datos según controles
df_periodo = df_final[df_final["year"] <= slider_year]
if dropdown_area != 'All Areas':
    df_periodo = df_periodo[df_periodo['research_area'] == dropdown_area]

G_filtrado = build_network(df_periodo)

# Dibujo final del lienzo de Matplotlib
if G_filtrado.number_of_nodes() == 0:
    st.warning("No data found for the selected combination.")
else:
    mexican_nodes = sum(institution_country_map.get(n) == "Mexico" for n in G_filtrado.nodes())
    international_nodes = G_filtrado.number_of_nodes() - mexican_nodes
    etapa_text = obtener_etapa(slider_year)

    fig, ax = plt.subplots(figsize=(16, 12))

    # Tamaños basados en volumen
    paper_count = df_periodo.groupby('institution_clean')['title'].nunique().to_dict()
    sizes_raw = np.array([paper_count.get(n, 0) for n in G_filtrado.nodes()])
    sizes_log = np.log1p(sizes_raw)
    sizes_norm = (sizes_log - sizes_log.min()) / (sizes_log.max() - sizes_log.min() + 1e-9)
    node_sizes = 300 + sizes_norm * 3500

    # Colores por país
    node_colors = [
        "tab:green" if institution_country_map.get(n, "Unknown") == "Mexico" else "#EBF6FF"
        for n in G_filtrado.nodes()
    ]

    # Aristas y pesos
    edge_widths = [1 + np.log1p(G_filtrado[u][v]["weight"]) for u, v in G_filtrado.edges()]
    edge_colors = []
    for u, v in G_filtrado.edges():
        cu = institution_country_map.get(u, "Unknown")
        cv = institution_country_map.get(v, "Unknown")
        if cu == "Mexico" and cv == "Mexico": edge_colors.append("tab:green")
        elif cu != "Mexico" and cv != "Mexico": edge_colors.append("lightgray")
        else: edge_colors.append("tab:orange")

    # Renderizado sobre el eje ax
    nx.draw_networkx_edges(G_filtrado, pos_fija, width=edge_widths, edge_color=edge_colors, alpha=0.4, ax=ax)
    nx.draw_networkx_nodes(G_filtrado, pos_fija, node_size=node_sizes, node_color=node_colors, edgecolors='black', alpha=0.8, ax=ax)

    # Etiquetas filtradas (Grado >= 4)
    degree = dict(G_filtrado.degree())
    labels = {node: node for node, deg in degree.items() if deg >= 4}
    nx.draw_networkx_labels(G_filtrado, pos_fija, labels=labels, font_size=9, font_weight='bold', ax=ax)

    # Leyenda
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Mexican Institution', markerfacecolor='tab:green', markersize=12, markeredgecolor='black'),
        Line2D([0], [0], marker='o', color='w', label='International Institution', markerfacecolor='#EBF6FF', markersize=12, markeredgecolor='black'),
        Line2D([0], [0], color='tab:green', lw=3, label='Mexico ↔ Mexico'),
        Line2D([0], [0], color='tab:orange', lw=3, label='Mexico ↔ International')
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=11, title='Collaboration Type')

    ax.set_title(
        f"{etapa_text}\n"
        f"Institutions: {G_filtrado.number_of_nodes()} (Mex: {mexican_nodes} | Int: {international_nodes}) | Edges: {G_filtrado.number_of_edges()}",
        fontsize=14, fontweight='bold'
    )
    ax.axis("off")
    fig.tight_layout()

    st.pyplot(fig)
