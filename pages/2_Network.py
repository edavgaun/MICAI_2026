import streamlit as st

# Importaciones locales desde tu arquitectura src/
from src.data_loader import load_data
from src.network import build_network, calcular_layout_fijo
from src.visualization import draw_network

st.set_page_config(layout="wide")
st.title("🕸️ Collaboration Network Discovery")

# 1. Cargar Datos Globales
df_final = load_data()
pos_fija = calcular_layout_fijo(df_final)

# Mapeos auxiliares
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

# 2. UI - Filtros en la barra lateral
st.sidebar.header("Network Controls")
year = st.sidebar.slider("Select Year Cutoff:", int(df_final.year.min()), int(df_final.year.max()), int(df_final.year.max()))
area = st.sidebar.selectbox("Research Area:", ['All Areas'] + areas)

# 3. Filtrado dinámico
df_periodo = df_final[df_final["year"] <= year]
if area != 'All Areas':
    df_periodo = df_periodo[df_periodo['research_area'] == area]

G_filtrado = build_network(df_periodo)

# 4. Validar y Renderizar
if G_filtrado.number_of_nodes() == 0:
    st.warning("No data found for the selected combination.")
else:
    mexican_nodes = sum(institution_country_map.get(n) == "Mexico" for n in G_filtrado.nodes())
    international_nodes = G_filtrado.number_of_nodes() - mexican_nodes
    etapa_text = obtener_etapa(year)

    # Llamamos al módulo de visualización pasando los parámetros requeridos
    fig = draw_network(
        G_filtrado, pos_fija, df_periodo, 
        institution_country_map, etapa_text, 
        year, area, mexican_nodes, international_nodes
    )
    
    # Mostrar el lienzo final de matplotlib en tu frontend
    st.pyplot(fig)
