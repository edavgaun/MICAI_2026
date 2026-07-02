import streamlit as st

# Conexión directa a tus submódulos limpios
import Ecosystem_Setup as backend
import Ecosystem_Content as text
import Ecosystem_Visuals as visuals

st.set_page_config(layout="wide")

# CSS Ajustado: Le damos 3.5rem de espacio arriba a toda la página para BAJAR los botones
st.markdown("""
    <style>
        [data-testid="stImage"], [data-testid="stFigureGrid"], .stPlotlyChart { width: 100% !important; max-width: 100% !important; }
        .block-container { 
            padding-left: 2rem !important; 
            padding-right: 2rem !important; 
            padding-top: 3.5rem !important; /* ⬅️ Esto baja la barra y evita que se corte arriba */
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
