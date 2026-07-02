import streamlit as st

# Conexión directa a tus submódulos limpios
import Ecosystem_Setup as backend
import Ecosystem_Content as text
import Ecosystem_Visuals as visuals

st.set_page_config(layout="wide")

# CSS Real para controlar el tamaño de los botones de navegación sin que se estiren horrible
st.markdown("""
    <style>
        [data-testid="stImage"], [data-testid="stFigureGrid"], .stPlotlyChart { width: 100% !important; max-width: 100% !important; }
        .block-container { padding-left: 2rem !important; padding-right: 2rem !important; padding-top: 1rem !important; }
        
        /* Forzamos a que el contenedor de las columnas de navegación no estire los elementos */
        [data-testid="stHorizontalBlock"] {
            align-items: center;
        }
        /* Diseñamos los botones para que actúen como pestañas de menú reales */
        div.stButton > button {
            width: auto !important;
            padding: 0.5rem 1.5rem !important;
            border-radius: 4px !important;
            border: 1px solid #e0e0e0 !important;
            background-color: #f8f9fa !important;
            color: #333333 !important;
            font-weight: 500 !important;
        }
        /* Efecto sutil al pasar el cursor */
        div.stButton > button:hover {
            border-color: #a0a0a0 !important;
            background-color: #f1f3f5 !important;
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

# Cambiamos las columnas a proporciones pequeñas y compactas a la izquierda [1, 1, 8]
# Esto evita que se dispersen o se ensanchen por toda la pantalla wide.
if "active_tab" not in st.session_state:
    st.session_state["active_tab"] = "Home"

nav_col1, nav_col2, _ = st.columns([1.2, 1.4, 7.4])
with nav_col1:
    if st.button("🏠 Home", key="btn_home"): 
        st.session_state["active_tab"] = "Home"
with nav_col2:
    if st.button("🕸️ Network Discovery", key="btn_network"): 
        st.session_state["active_tab"] = "Network"

st.markdown("---")

# ==============================================================================
# ENRUTADOR PRINCIPAL (El resto del archivo se queda exactamente igual)
# ==============================================================================
if st.session_state["active_tab"] == "Home":
    st.title(text.HOME_TITLE)
    st.markdown(text.HOME_INTRO)

elif st.session_state["active_tab"] == "Network":
    st.title(text.APP_TITLE)
    st.caption(text.APP_SUBTITLE)
    
    if "current_era_step" not in st.session_state:
        st.session_state["current_era_step"] = 1

    # Botones de Era
    col_back, col_spacer, col_next = st.columns([2, 6, 2])
    with col_back:
        if st.button("⬅️ Anterior Era", key="era_back") and st.session_state["current_era_step"] > 1: 
            st.session_state["current_era_step"] -= 1
    with col_next:
        if st.button("Siguiente Era ➡️", key="era_next") and st.session_state["current_era_step"] < 4: 
            st.session_state["current_era_step"] < 4
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

    # Filtrado temporal
    df_periodo = df_final[df_final["year"] <= slider_year]
    if dropdown_area != 'All Areas':
        df_periodo = df_periodo[df_periodo['research_area'] == dropdown_area]

    G_filtrado = backend.build_network(df_periodo)

    # Lógica de foco
    has_focus = len(selected_institutions) > 0
    focus_nodes = set(selected_institutions)
    if has_focus:
        for n in selected_institutions:
            if n in G_filtrado: 
                focus_nodes.update(G_filtrado.neighbors(n))

    # Inyección en layout final
    if G_filtrado.number_of_nodes() == 0:
        st.warning(text.EMPTY_DATA_WARNING)
    else:
        col_red, col_barras = st.columns([7.5, 2.5])
        with col_red:
            visuals.draw_network_graph(G_filtrado, pos_fija, institution_country_map, df_periodo, has_focus, focus_nodes, selected_institutions)
        with col_barras:
            st.markdown(text.BAR_CHART_TITLE)
            visuals.draw_volume_bars(df_periodo, institution_country_map, has_focus, focus_nodes)
