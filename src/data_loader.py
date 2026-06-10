import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    # Ruta relativa apuntando a tu carpeta data/
    df = pd.read_csv("Data/data.csv")
    # Asegúrate de que el año sea entero
    df['year'] = df['year'].astype(int)
    return df
