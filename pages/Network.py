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

# ==============================================================================
# CONTROLES LATERALES
# ==============================================================================
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

# Filtrado inicial de datos según controles de tiempo/área
df_periodo = df_final[df_final["year"] <= slider_year]
if dropdown_area != 'All Areas':
    df_periodo = df_periodo[df_periodo['research_area'] == dropdown_area]

G_filtrado = build_network(df_periodo)

# ==============================================================================
# HIGHLIGHT CONTROLS FIXED (PREVENTS STATE LOSS)
# ==============================================================================
# Pulling options from global df_final array so choices never disappear dynamically
global_institutions = sorted(df_final['institution_clean'].dropna().unique())

st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Highlight Entities")
selected_institutions = st.sidebar.multiselect(
    "Select to isolate on plots:",
    options=global_institutions,
    key="network_highlight_search_stable",
    help="Leave empty to see the full network. Select one or more to highlight them along with their partners."
)

# Lógica de enfoque extendido (Nodos seleccionados + Vecinos)
has_focus = len(selected_institutions) > 0
focus_nodes = set(selected_institutions)
if has_focus:
    for n in selected_institutions:
        if n in G_filtrado:
            focus_nodes.update(G_filtrado.neighbors(n))

# ==============================================================================
# DIBUJO FINAL Y PROCESAMIENTO VISUAL VECTORIAL
# ==============================================================================
if G_filtrado.number_of_nodes() == 0:
    st.warning("No data found for the selected combination.")
else:
    mexican_nodes = sum(institution_country_map.get(n) == "Mexico" for n in G_filtrado.nodes())
    international_nodes = G_filtrado.number_of_nodes() - mexican_nodes
    etapa_text = obtener_etapa(slider_year)

    # Integración en columnas (75% Red, 25% Barras)
    col_red, col_barras = st.columns([7.5, 2.5])

    # --- COLUMNA IZQUIERDA: EL GRAFO DE LA RED ---
    with col_red:
        fig_red, ax_red = plt.subplots(figsize=(14, 10))
        fig_red.subplots_adjust(left=0.01, right=0.99, top=0.92, bottom=0.01)

        # Diccionario de volúmenes de papers para el mapeo de tamaños de nodos
        paper_count = df_periodo.groupby('institution_clean')['title'].nunique().to_dict()
        
        # Mapeos de aristas: Separamos en activas (iluminadas) y fondo (atenuadas)
        edges_active = []
        widths_active = []
        colors_active = []
        
        edges_bg = []
        widths_bg = []
        colors_bg = []

        for u, v in G_filtrado.edges():
            cu = institution_country_map.get(u, "Unknown")
            cv = institution_country_map.get(v, "Unknown")
            w = 1 + np.log1p(G_filtrado[u][v]["weight"])
            
            if cu == "Mexico" and cv == "Mexico": edge_color = "tab:green"
            elif cu != "Mexico" and cv != "Mexico": edge_color = "lightgray"
            else: edge_color = "tab:orange"
            
            # Clasificación por pertenencia al foco de búsqueda
            if not has_focus or (u in selected_institutions or v in selected_institutions):
                edges_active.append((u, v))
                widths_active.append(w)
                colors_active.append(edge_color)
            else:
                edges_bg.append((u, v))
                widths_bg.append(w)
                colors_bg.append(edge_color)

        # Mapeos de nodos: Separamos en activos y fondo
        nodes_active = []
        sizes_active = []
        colors_active_nodes = []
        
        nodes_bg = []
        sizes_bg = []
        colors_bg_nodes = []

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
                    sizes_bg.append
