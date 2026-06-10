import streamlit as st

# Importamos las funciones de configuración e instrucciones desde tu script setup
from pages.1_Ecosystem_Setup import set_layout, show_header, show_main_instructions, load_clean_data

# 1. Configurar el layout ancho y los estilos CSS
set_layout()

# 2. Desplegar el encabezado con tu título y créditos académicos
show_header("🇲🇽 Evolution of the Mexican AI Ecosystem")

# 3. Mostrar las instrucciones globales y las eras analíticas
show_main_instructions()

# 4. Carga de datos global (opcional por si quieres validar el estado en la portada)
try:
    df = load_clean_data()
    st.sidebar.success(f"📈 Dataset online: {df.shape[0]} registros listos.")
except Exception as e:
    st.sidebar.error(f"⚠️ Error al conectar con data.csv: {e}")
