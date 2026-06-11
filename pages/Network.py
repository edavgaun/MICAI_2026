import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.lines import Line2D

# Importación directa desde el setup estático
from pages.Ecosystem_Setup import load_clean_data, build_network, calcular_layout_fijo

# Este bloque de CSS destruye los márgenes obligatorios que Streamlit le impone a los gráficos
st.markdown("""
    <style>
        /* Desbloquea el ancho máximo del contenedor de imágenes de Streamlit */
        [data-testid="stImage"], [data-testid="stFigureGrid"], .stPlotlyChart {
            width: 100% !important;
            max-width: 100% !important;
        }
        /* Elimina padding sobrante del bloque principal */
        .block-container {
            padding-left: 1rem !important;
            padding-right: 1rem !important;
        }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# INTERFAZ DE USUARIO Y CONFIGURACIÓN DE PANTALLA
# ==============================================================================
st.title("🕸️ Collaboration Network Discovery")
st.markdown("---")

# Carga de datos y cálculo matemático de posiciones
df_final = load_clean_data()

# Guarda las posiciones en la sesión para que solo se calculen UNA VEZ
if "pos_fija" not in st.session_state:
    st.session_state["pos_fija"] = calcular_layout_fijo(df_final)

pos_fija = st.session_state["pos_fija"]

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

# CORRECCIÓN 1: Cambiamos el 'value' para que por defecto inicie en el año mínimo
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

    # ==========================================================================
    # AQUÍ ENTRA LA INTEGRACIÓN EN COLUMNAS (A PARTIR DE LA LÍNEA 79 ORIGINAL)
    # ==========================================================================
    col_red, col_barras = st.columns([7.5, 2.5])

    # --- COLUMNA IZQUIERDA: EL GRAFO DE LA RED ---
    with col_red:
        fig_red, ax_red = plt.subplots(figsize=(14, 10))
        fig_red.subplots_adjust(left=0.01, right=0.99, top=0.92, bottom=0.01)

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

        # Renderizado sobre el eje ax_red
        nx.draw_networkx_edges(G_filtrado, pos_fija, width=edge_widths, edge_color=edge_colors, alpha=0.4, ax=ax_red)
        nx.draw_networkx_nodes(G_filtrado, pos_fija, node_size=node_sizes, node_color=node_colors, edgecolors='black', alpha=0.8, ax=ax_red)

        # Etiquetas filtradas (Grado >= 4)
        degree = dict(G_filtrado.degree())
        labels = {node: node for node, deg in degree.items() if deg >= 4}
        nx.draw_networkx_labels(G_filtrado, pos_fija, labels=labels, font_size=9, font_weight='bold', ax=ax_red)

        # Leyenda
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', label='Mexican Institution', markerfacecolor='tab:green', markersize=12, markeredgecolor='black'),
            Line2D([0], [0], marker='o', color='w', label='International Institution', markerfacecolor='#EBF6FF', markersize=12, markeredgecolor='black'),
            Line2D([0], [0], color='tab:green', lw=3, label='Mexico ↔ Mexico'),
            Line2D([0], [0], color='tab:orange', lw=3, label='Mexico ↔ International')
        ]
        ax_red.legend(handles=legend_elements, loc='upper left', fontsize=11, title='Collaboration Type')

        # Forzar límites de los ejes basados en los extremos reales de pos_fija
        x_coords = [coords[0] for coords in pos_fija.values()]
        y_coords = [coords[1] for coords in pos_fija.values()]
        ax_red.set_xlim(min(x_coords) - 0.2, max(x_coords) + 0.2)
        ax_red.set_ylim(min(y_coords) - 0.2, max(y_coords) + 0.2)

        ax_red.set_title(
            f"{etapa_text}\n"
            f"Institutions: {G_filtrado.number_of_nodes()} (Mex: {mexican_nodes} | Int: {international_nodes}) | Edges: {G_filtrado.number_of_edges()}",
            fontsize=14, fontweight='bold'
        )
        ax_red.axis("off")

        # Desplegamos la red en su columna
        st.pyplot(fig_red, use_container_width=True)

    # --- COLUMNA DERECHA: LAS BARRAS DINÁMICAS (TU TOP 10) ---
    with col_barras:
        st.markdown("### 📊 Top 10 Volumen")
        st.caption("Frecuencia absoluta en el periodo mostrado")

        # Hacemos el conteo agrupando sobre los mismos datos ya filtrados (df_periodo)
        top_instituciones = df_periodo['institution_clean'].value_counts().head(10)

        if not top_instituciones.empty:
            fig_barras, ax_barras = plt.subplots(figsize=(4, 6))
            
            y_labels = top_instituciones.index[::-1]
            x_values = top_instituciones.values[::-1]
            
            # Dibujamos las barras horizontales usando tu color base de forma limpia
            bars = ax_barras.barh(y_labels, x_values, color='#2b5c8f', edgecolor='black', alpha=0.85, height=0.5)
            
            # Formato estético sin marcos estorbosos
            ax_barras.tick_params(axis='both', labelsize=10)
            ax_barras.spines['top'].set_visible(False)
            ax_barras.spines['right'].set_visible(False)
            ax_barras.spines['left'].set_color('#cccccc')
            ax_barras.spines['bottom'].set_color('#cccccc')
            
            # Marcadores numéricos integrados a cada barra
            ax_barras.bar_label(bars, padding=5, fontsize=10, fontweight='bold', color='#333333')
            ax_barras.xaxis.grid(True, linestyle='--', alpha=0.3, color='#999999')
            ax_barras.set_axisbelow(True)
            
            fig_barras.tight_layout()
            
            # Desplegamos el gráfico de barras en su columna correspondiente
            st.pyplot(fig_barras, use_container_width=True)
        else:
            st.info("No hay suficientes datos en este corte.")
