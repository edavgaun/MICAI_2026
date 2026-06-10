import streamlit as st

# Importamos exclusivamente las herramientas reales desde tu setup
from pages.Ecosystem_Setup import load_clean_data

# ==============================================================================
# 1. CARGA DE DATOS Y MAPEOS AUXILIARES
# ==============================================================================
# Recuperamos el DataFrame (usa la caché compartida de RAM de forma instantánea)
df_final = load_clean_data()

# Mapeo para identificar el país de procedencia de cada institución
institution_country_map = (
    df_final[['institution_clean', 'Country']]
    .dropna()
    .drop_duplicates()
    .groupby('institution_clean')['Country']
    .first()
    .to_dict()
)

# Extraemos la lista única de áreas de investigación para el filtro
areas = sorted(df_final['research_area'].dropna().unique())


def obtener_etapa(year):
    """Determina la era histórica según el año seleccionado."""
    if year <= 2008: 
        return "Era 1: The Islands (1997–2008)"
    elif year <= 2019: 
        return "Era 2: The Bridges (2009–2019)"
    elif year <= 2022: 
        return "Era 3: Forced Virtualization (2020–2022)"
    else: 
        return "Era 4: Solid Networks (2023–2026)"


# ==============================================================================
# 2. INTERFAZ DE USUARIO (CONTROLES LATERALES)
# ==============================================================================
st.title("🕸️ Collaboration Network Discovery")
st.markdown("---")

st.sidebar.header("Network Controls")

slider_year = st.sidebar.slider(
    "Select Year Cutoff:", 
    int(df_final.year.min()), 
    int(df_final.year.max()), 
    int(df_final.year.max())
)

dropdown_area = st.sidebar.selectbox(
    "Research Area:", 
    ['All Areas'] + areas
)

# ==============================================================================
# 3. FILTRADO TEMPORAL Y TEMÁTICO DE LOS DATOS
# ==============================================================================
df_periodo = df_final[df_final["year"] <= slider_year]
if dropdown_area != 'All Areas':
    df_periodo = df_periodo[df_periodo['research_area'] == dropdown_area]

# ==============================================================================
# 4. CONTENEDOR DE MONITOREO Y FUTURA VISUALIZACIÓN
# ==============================================================================
# Marcamos provisionalmente el espacio para asegurar que la lógica de conteo responda
if df_periodo.empty:
    st.warning("No data found for the selected combination.")
else:
    # Extraemos las instituciones únicas presentes en este corte específico
    nodos_actuales = df_periodo['institution_clean'].dropna().unique()
    
    mexican_nodes = sum(institution_country_map.get(n) == "Mexico" for n in nodos_actuales)
    international_nodes = len(nodos_actuales) - mexican_nodes
    etapa_text = obtener_etapa(slider_year)

    # Bloque informativo de control (Para validar en tiempo real el comportamiento de los filtros)
    st.info(
        f"**Current Era:** {etapa_text}  \n"
        f"**Active Filters:** Up to year {slider_year} | Area: {dropdown_area}  \n"
        f"**Detected Entities:** Total Institutions: {len(nodos_actuales)} "
        f"(🇲🇽 Mexican: {mexican_nodes} | 🌍 International: {international_nodes})"
    )
    
    # [Aquí se integrará la función de dibujo en el siguiente paso]
