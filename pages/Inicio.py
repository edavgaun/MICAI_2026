import streamlit as st
from pages.Ecosystem_Setup import show_header, show_main_instructions, load_clean_data

# Desplegamos tu contenido en la pantalla principal
show_header("🇲🇽 Evolution of the Mexican AI Ecosystem")
show_main_instructions()

# Carga limpia de datos
df = load_clean_data()
st.sidebar.success(f"📈 Dataset listo: {df.shape[0]} registros.")
