import streamlit as st
import Ecosystem_Setup as backend
import Ecosystem_Content as text
import Ecosystem_Visuals as visuals

st.set_page_config(layout="wide")

# CSS: Ajuste de márgenes superiores y tamaño estándar para botones de navegación
st.markdown("""
    <style>
        [data-testid="stImage"], [data-testid="stFigureGrid"], .stPlotlyChart { width: 100% !important; max-width: 100% !important; }
        .block-container { 
            padding-left: 2rem !important; 
            padding-right: 2rem !important; 
            padding-top: 3.5rem !important; 
        }
        div.stButton > button {
            height: 45px !important;
            line-height: 45px !important;
            padding: 0px 25px !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
        }
    </style>
""", unsafe_allow_html=True)

# Carga de datos optimizada e inicialización de estados persistentes
df_final = backend.load_clean_data()

if "pos_fija" not in st.session_state:
    st.session_state["pos_fija"] = backend.calcular_layout_fijo(df_final)
pos_fija = st.session_state["pos_fija"]

institution_country_map = backend.obtener_mapeo_paises(df_final)
areas = sorted(df_final['research_area'].dropna().unique())

if "active_tab" not in st.session_state:
    st.session_state["active_tab"] = "Home"

# BARRA DE NAVEGACIÓN SUPERIOR
nav_col1, nav_col2, _ = st.columns([1.5, 2.0, 6.5])
with nav_col1:
    if st.button("🏠 Home Overview", key="btn_home"): 
        st.session_state["active_tab"] = "Home"
with nav_col2:
    if st.button("🕸️ Network Discovery", key="btn_network"): 
        st.session_state["active_tab"] = "Network"

st.markdown("---")

# ==============================================================================
# ENRUTADOR PRINCIPAL
# ==============================================================================
if st.session_state["active_tab"] == "Home":
    st.title(text.HOME_TITLE)
    st.markdown(text.HOME_INTRO)
    st.markdown("---")
    
    # Despliegue del diagrama horizontal desde tu carpeta assets
    st.image("assets/4_stages.png", use_container_width=True)

elif st.session_state["active_tab"] == "Network":
    st.title(text.APP_TITLE)
    st.caption(text.APP_SUBTITLE)
    
    # Línea de tiempo interactiva por año
    min_year, max_year = int(df_final['year'].min()), int(df_final['year'].max())
    selected_year = st.slider("Selecciona el año de corte:", min_year, max_year, max_year)
    
    # Título de la Era dinámico según el año del slider
    st.subheader(f"📖 {text.obtener_info_era(selected_year)}")

    # Selectores horizontales de filtros
    filter_col1, filter_col2 = st.columns(2)
    with filter_col1:
        dropdown_area = st.selectbox("Filtrar por Área de Investigación:", ['All Areas'] + areas)
    with filter_col2:
        global_institutions = sorted(df_final['institution_clean'].dropna().unique())
        selected_institutions = st.multiselect("🔍 Resaltar Entidades de la Red:", options=global_institutions)

    # Filtrado temporal y por área
    df_periodo = df_final[df_final["year"] <= selected_year]
    if dropdown_area != 'All Areas':
        df_periodo = df_periodo[df_periodo['research_area'] == dropdown_area]

    G_filtrado = backend.build_network(df_periodo)

    # Lógica de enfoque y aislamiento de nodos
    has_focus = len(selected_institutions) > 0
    focus_nodes = set(selected_institutions)
    if has_focus:
        for n in selected_institutions:
            if n in G_filtrado: 
                focus_nodes.update(G_filtrado.neighbors(n))

    # Renderizado de componentes gráficos de la Red
    if G_filtrado.number_of_nodes() == 0:
        st.warning(text.EMPTY_DATA_WARNING)
    else:
        col_red, col_barras = st.columns([7.5, 2.5])
        
        with col_red:
            # El grafo interactivo se mantiene a la izquierda (ahora recibe año y área para la exportación)
            visuals.draw_network_graph(
                G_filtrado, 
                pos_fija, 
                institution_country_map, 
                df_periodo, 
                has_focus, 
                focus_nodes, 
                selected_institutions,
                selected_year,
                dropdown_area
            )
        with col_barras:
            # 1. Caja de Leyenda Técnica (Arriba)
            st.markdown(text.LEGEND_HTML, unsafe_allow_html=True)
            
            # 2. Separador visual limpio
            st.markdown("<br>", unsafe_allow_html=True)
            
            # 3. Gráfica de Barras Desplazada (Abajo)
            st.markdown(text.BAR_CHART_TITLE)
            visuals.draw_volume_bars(df_periodo, institution_country_map, has_focus, focus_nodes)
