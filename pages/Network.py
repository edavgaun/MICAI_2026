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

# ==============================================================================
# FIXED SEARCH: Using global static choices + key to lock the state perfectly
# ==============================================================================
global_institutions = sorted(df_final['institution_clean'].dropna().unique())

st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Highlight Entities")
selected_institutions = st.sidebar.multiselect(
    "Select to isolate on plots:",
    options=global_institutions,
    key="network_highlight_search_stable_final",
    help="Leave empty to see the full network. Select one or more to highlight them along with their partners."
)

# Lógica de enfoque extendido (Nodos seleccionados + Vecinos)
has_focus = len(selected_institutions) > 0
focus_nodes = set(selected_institutions)
if has_focus:
    for n in selected_institutions:
        if n in G_filtrado:
            focus_nodes.update(G_filtrado.neighbors(n))

# Dibujo final del lienzo de Matplotlib
if G_filtrado.number_of_nodes() == 0:
    st.warning("No data found for the selected combination.")
else:
    mexican_nodes = sum(institution_country_map.get(n) == "Mexico" for n in G_filtrado.nodes())
    international_nodes = G_filtrado.number_of_nodes() - mexican_nodes
    etapa_text = obtener_etapa(slider_year)

    # CORRECCIÓN 2: RESTORED your panoramic widescreen layout split ratio
    col_red, col_barras = st.columns([7.5, 2.5])

    # --- COLUMNA IZQUIERDA: EL GRAFO DE LA RED ---
    with col_red:
        # RESTORED your layout canvas dimensions (20, 11) to fill the full container
        fig_red, ax_red = plt.subplots(figsize=(20, 11))
        fig_red.subplots_adjust(left=0.01, right=0.99, top=0.93, bottom=0.01)

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

        # Process vector-based alphas safely without slow loops
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
            
            if not has_focus or (u in selected_institutions or v in selected_institutions):
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

        # High-performance background/foreground split layers rendering
        if has_focus:
            if edges_bg:
                nx.draw_networkx_edges(G_filtrado, pos_fija, edgelist=edges_bg, width=widths_bg, edge_color=colors_bg, alpha=0.02, ax=ax_red)
            if nodes_bg:
                nx.draw_networkx_nodes(G_filtrado, pos_fija, nodelist=nodes_bg, node_size=sizes_bg, node_color=colors_bg_nodes, edgecolors='black', alpha=0.12, ax=ax_red)
        
        if edges_active:
            nx.draw_networkx_edges(G_filtrado, pos_fija, edgelist=edges_active, width=widths_active, edge_color=colors_active, alpha=0.4, ax=ax_red)
        if nodes_active:
            nx.draw_networkx_nodes(G_filtrado, pos_fija, nodelist=nodes_active, node_size=sizes_active, node_color=colors_active_nodes, edgecolors='black', alpha=0.8, ax=ax_red)

        # Etiquetas filtradas (Grado >= 4) o foco
        degree = dict(G_filtrado.degree())
        labels = {}
        for node in G_filtrado.nodes():
            if has_focus:
                if node in focus_nodes:
                    labels[node] = node
            else:
                if degree.get(node, 0) >= 4:
                    labels[node] = node
                    
        nx.draw_networkx_labels(G_filtrado, pos_fija, labels=labels, font_size=9, font_weight='bold', ax=ax_red)

        # Leyenda
        legend_elements = [
            Line2D([0], [0], marker='o', color='w', label='Mexican Institution', markerfacecolor='tab:green', markersize=12, markeredgecolor='black'),
            Line2D([0], [0], marker='o', color='w', label='International Institution', markerfacecolor='#EBF6FF', markersize=12, markeredgecolor='black'),
            Line2D([0], [0], color='tab:green', lw=3, label='Mexico ↔ Mexico'),
            Line2D([0], [0], color='tab:orange', lw=3, label='Mexico ↔ International')
        ]
        ax_red.legend(handles=legend_elements, loc='upper left', fontsize=11, title='Collaboration Type')

        # CORRECCIÓN 3: RESTORED your hard bounding box limits calculations
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

        # Render wide plot layout
        st.pyplot(fig_red, use_container_width=True)

    # --- COLUMNA DERECHA: LAS BARRAS DINÁMICAS CONSISTENTES ---
    with col_barras:
        st.markdown("### 📊 Top 10 Volumen")
        st.caption("Frecuencia absoluta en el periodo mostrado")

        top_instituciones = df_periodo['institution_clean'].value_counts().head(10)

        if not top_instituciones.empty:
            # RESTORED your optimal bar height dimensions (4, 5)
            fig_barras, ax_barras = plt.subplots(figsize=(4, 5))
            
            y_labels = top_instituciones.index[::-1]
            x_values = top_instituciones.values[::-1]
            
            # Mapeamos los colores de las barras de forma idéntica al grafo
            bar_colors = [
                "tab:green" if institution_country_map.get(inst, "Unknown") == "Mexico" else "#EBF6FF"
                for inst in y_labels
            ]
            
            bar_alphas = [
                1.0 if not has_focus or inst in focus_nodes else 0.15
                for inst in y_labels
            ]
            
            bars = ax_barras.barh(y_labels, x_values, color=bar_colors, edgecolor='black', height=0.5)
            for i, bar in enumerate(bars):
                bar.set_alpha(bar_alphas[i])
            
            # Formato estético sin marcos estorbosos
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
            
            st.caption("**Nota:** El asterisco (`*`) indica una institución internacional identificada con siglas reales, mientras que la tilde (`~`) representa una institución abreviada por el sistema (no siglas reales).")
        else:
            st.info("No hay suficientes datos en este corte.")
