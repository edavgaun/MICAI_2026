import streamlit as st

# Conexión directa a tus submódulos limpios
import Ecosystem_Setup as backend
import Ecosystem_Content as text
import Ecosystem_Visuals as visuals

st.set_page_config(layout="wide")

# CSS Ajustado: Le damos 3.5rem de espacio arriba para BAJAR los botones y que no se corten
st.markdown("""
    <style>
        [data-testid="stImage"], [data-testid="stFigureGrid"], .stPlotlyChart { width: 100% !important; max-width: 100% !important; }
        .block-container { 
            padding-left: 2rem !important; 
            padding-right: 2rem !important; 
            padding-top: 3.5rem !important; /* Esto empuja los botones hacia abajo de forma segura */
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

# Carga e inicialización de estados persistentes
df_final = backend.load_clean_data()

if "pos_fija" not in st.session_state:
    st.session_state["pos_fija"] = backend.calcular_layout_fijo(df_final)
pos_fija = st.session_state["pos_fija"]

institution_country_map = backend.obtener_mapeo_paises(df_final)
areas = sorted(df_final['research_area'].dropna().unique())

# Inicializamos el estado de la pestaña activa si no existe
if "active_tab" not in st.session_state:
    st.session_state["active_tab"] = "Home"

# BARRA DE NAVEGACIÓN SUPERIOR
nav_col1, nav_col2, _ = st.columns([1.5, 2.0, 6.5])
with nav_col1:
    if st.button("🏠 Home Overview", key="btn_home_v2"): 
        st.session_state["active_tab"] = "Home"
with nav_col2:
    if st.button("🕸️ Network Discovery", key="btn_network_v2"): 
        st.session_state["active_tab"] = "Network"

st.markdown("---")

# ==============================================================================
# ENRUTADOR PRINCIPAL (Todo el código que se había borrado)
# ==============================================================================
if st.session_state["active_tab"] == "Home":
    st.title(text.HOME_TITLE)
    st.markdown(text.HOME_INTRO)

elif st.session_state["active_tab"] == "Network":
    st.title(text.APP_TITLE)
    st.caption(text.APP_SUBTITLE)
    
    if "current_era_step" not in st.session_state:
        st.session_state["current_era_step"] = 1

    # Navegación interna de Eras
    col_back, col_spacer, col_next = st.columns([2, 6, 2])
    with col_back:
        if st.button("⬅️ Anterior Era", key="era_back") and st.session_state["current_era_step"] > 1: 
            st.session_state["current_era_step"] -= 1
    with col_next:
        if st.button("Siguiente Era ➡️", key="era_next") and st.session_state["current_era_step"] < 4: 
            st.session_state["current_era_step"] += 1

    active_step = st.session_state["current_era_step"]
    slider_year = text.ERAS[active_step]["year"]
    st.subheader(f"📖 {text.ERAS[active_step]['name']}")

    # Selectores en cuadrícula horizontal
    filter_col1, filter_col2 = st.columns(2)
    with filter_col1:
        dropdown_area = st.selectbox("Filtrar por Área de Investigación:", ['All Areas'] + areas)
    with filter_col2:
        global_institutions = sorted(df_final['institution_clean'].dropna().unique())
        selected_institutions = st.multiselect("🔍 Resaltar Entidades de la Red:", options=global_institutions)

    # Filtrado temporal según el corte de la Era
    df_periodo = df_final[df_final["year"] <= slider_year]
    if dropdown_area != 'All Areas':
        df_periodo = df_periodo[df_periodo['research_area'] == dropdown_area]

    G_filtrado = backend.build_network(df_periodo)

    # Lógica de foco para aislamiento
    has_focus = len(selected_institutions) > 0
    focus_nodes = set(selected_institutions)
    if has_focus:
        for n in selected_institutions:
            if n in G_filtrado: 
                focus_nodes.update(G_filtrado.neighbors(n))

    # Inyección en el layout visual
    if G_filtrado.number_of_nodes() == 0:
        st.warning(text.EMPTY_DATA_WARNING)
    else:
        col_red, col_barras = st.columns([7.5, 2.5])
        with col_red:
            visuals.draw_network_graph(G_filtrado, pos_fija, institution_country_map, df_periodo, has_focus, focus_nodes, selected_institutions)
        with col_barras:
            st.markdown(text.BAR_CHART_TITLE)
            visuals.draw_volume_bars(df_periodo, institution_country_map, has_focus, focus_nodes)
