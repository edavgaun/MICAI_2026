import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.lines import Line2D

# Importación directa desde el setup estático
from pages.Ecosystem_Setup import load_clean_data, build_network, calcular_layout_fijo

# ==============================================================================
# INTERFAZ DE USUARIO Y CONFIGURACIÓN DE PANTALLA
# ==============================================================================
st.title("🕸️ Collaboration Network Discovery")
st.markdown("---")

# Carga de datos y cálculo matemático de posiciones
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

min_year = int(df_final.year.min())
max_year = int(df_final.year.max())

slider_year = st.sidebar.slider(
    "Select Year Cutoff:", 
    min_value=min_year, 
    max_value=max_year, 
    value=min_year
)
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

    # CAMBIO 1: Ajustamos tamaño de figura más panorámico (24x10) para llenar pantallas wide
    fig, ax = plt.subplots(figsize=(24, 10))
    
    # Eliminación absoluta de márgenes perimetrales de Matplotlib
    fig.subplots_adjust(left=0.0, right=1.0, top=0.90, bottom=0.0)

    # Tamaños basados en volumen
    paper_count = df_periodo.groupby('institution_clean')['title'].nunique().to_dict()
    sizes_raw = np.array([paper_count.get(n, 0) for n in G_filtrado.nodes()])
    sizes_log = np.log1p(sizes_raw)
    sizes_norm = (sizes_log - sizes_log.min()) / (sizes_log.max() - sizes_log.min() + 1e-9)
    node_sizes = 400 + sizes_norm * 4500  # Escalado de nodos ligeramente más grande

    # Colores por país
    node_colors = [
        "tab:green" if institution_country_map.get(n, "Unknown") == "Mexico" else "#EBF6FF"
        for n in G_filtrado.nodes()
    ]

    # Aristas y pesos
    edge_widths = [1.5 + np.log1p(G_filtrado[u][v]["weight"]) * 2 for u, v in G_filtrado.edges()]
    edge_colors = []
    for u, v in G_filtrado.edges():
        cu = institution_country_map.get(u, "Unknown")
        cv = institution_country_map.get(v, "Unknown")
        if cu == "Mexico" and cv == "Mexico": edge_colors.append("tab:green")
        elif cu != "Mexico" and cv != "Mexico": edge_colors.append("#D3D3D3")
        else: edge_colors.append("tab:orange")

    # Renderizado sobre el eje ax
    nx.draw_networkx_edges(G_filtrado, pos_fija, width=edge_widths, edge_color=edge_colors, alpha=0.35, ax=ax)
    nx.draw_networkx_nodes(G_filtrado, pos_fija, node_size=node_sizes, node_color=node_colors, edgecolors='black', alpha=0.85, ax=ax)

    # CAMBIO 2: Textos institucionales notablemente más grandes (font_size=12) y legibles
    degree = dict(G_filtrado.degree())
    labels = {node: node for node, deg in degree.items() if deg >= 4}
    nx.draw_networkx_labels(G_filtrado, pos_fija, labels=labels, font_size=12, font_weight='bold', ax=ax)

    # CAMBIO 3: Escala de textos en Leyenda ampliada
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', label='Mexican Institution', markerfacecolor='tab:green', markersize=14, markeredgecolor='black'),
        Line2D([0], [0], marker='o', color='w', label='International Institution', markerfacecolor='#EBF6FF', markersize=14, markeredgecolor='black'),
        Line2D([0], [0], color='tab:green', lw=4, label='Mexico ↔ Mexico'),
        Line2D([0], [0], color='tab:orange', lw=4, label='Mexico ↔ International')
    ]
    ax.legend(handles=legend_elements, loc='upper left', fontsize=13, title='Collaboration Type', title_fontsize=15)

    # Forzar límites estrictos basados en la dispersión espacial real
    x_coords = [coords[0] for coords in pos_fija.values()]
    y_coords = [coords[1] for coords in pos_fija.values()]
    ax.set_xlim(min(x_coords) - 0.1, max(x_coords) + 0.1)
    ax.set_ylim(min(y_coords) - 0.1, max(y_coords) + 0.1)

    # CAMBIO 4: Título gigante e informativo para romper la escala pequeña previa
    ax.set_title(
        f"{etapa_text}\n"
        f"Institutions: {G_filtrado.number_of_nodes()} (Mex: {mexican_nodes} | Int: {international_nodes}) | Edges: {G_filtrado.number_of_edges()}",
        fontsize=20, fontweight='bold', pad=20
    )
    ax.axis("off")

    # CAMBIO 5: bbox_inches='tight' recorta cualquier espacio en blanco remanente a los costados
    st.pyplot(fig, use_container_width=True, bbox_inches='tight')
