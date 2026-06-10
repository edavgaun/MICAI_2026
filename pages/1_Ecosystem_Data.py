import streamlit as st
import pandas as pd

# ==============================================================================
# MÓDULO DE OPERACIONES, CARGA DE DATOS Y CONTROL DE LAYOUT DE LA APP
# ==============================================================================

@st.cache_data
def load_clean_data():
    """Carga el CSV de datos limpios proveniente de Colab."""
    df = pd.read_csv("Data/data.csv")
    df['year'] = df['year'].astype(int)
    return df
