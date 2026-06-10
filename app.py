import streamlit as st
from pages.Ecosystem_Setup import set_layout, show_header, show_main_instructions, load_clean_data

# Inicialización directa
set_layout()
show_header("🇲🇽 Evolution of the Mexican AI Ecosystem")
show_main_instructions()

# Carga de datos limpia y sin desconfianzas
df = load_clean_data()
st.sidebar.success(f"📈 Dataset listo: {df.shape[0]} papers analizados.")
