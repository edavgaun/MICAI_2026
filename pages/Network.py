import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.lines import Line2D

# Importación directa desde el setup estático
from pages.Ecosystem_Setup import load_clean_data, build_network, calcular_layout_fijo
from pages.network_renderer import draw_network

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

    fig_red = draw_network(
        G_filtrado=G_filtrado,
        pos_fija=pos_fija,
        institution_country_map=institution_country_map,
        df_periodo=df_periodo,
        title=(
            f"{etapa_text}\n"
            f"Institutions: {G_filtrado.number_of_nodes()} "
            f"(Mex: {mexican_nodes} | Int: {international_nodes}) "
            f"| Edges: {G_filtrado.number_of_edges()}"
        ),
        selected_institutions=selected_institutions
    )

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
