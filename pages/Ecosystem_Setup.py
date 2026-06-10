import streamlit as st
import pandas as pd

# ==============================================================================
# MÓDULO DE OPERACIONES, CARGA DE DATOS Y CONTROL DE LAYOUT
# ==============================================================================

@st.cache_data
def load_clean_data():
    """Carga el CSV de datos limpios proveniente de Colab."""
    df = pd.read_csv("Data/data.csv")
    df['year'] = df['year'].astype(int)
    return df


def set_layout():
    """Controla la configuración estructural de la interfaz de Streamlit."""
    st.set_page_config(layout="wide")
    st.markdown("""
        <style>
            .block-container {
                padding-top: 1.5rem;
                padding-bottom: 1rem;
                padding-left: 2rem;
                padding-right: 2rem;
            }
            [data-testid="stSidebarUserContent"] {
                padding-top: 1.5rem;
            }
        </style>
    """, unsafe_allow_html=True)


def show_header(text_title):
    """Muestra el título de la página y los créditos académicos del proyecto."""
    st.title(text_title)
    st.caption("📘 Based on: Edgar Avalos-Gauna (2026), *Evolution of the Mexican AI Ecosystem*")
    st.caption("Avalos-Gauna, E. (2026). *Tracing Institutional Collaboration and Temporal Dynamics Across the Mexican AI Landscape*. Proceedings of the Mexican International Conference on Artificial Intelligence (MICAI, 2026).")


def show_main_instructions():
    """Muestra las instrucciones globales de navegación y las eras analíticas."""
    st.markdown("""
    ### 🧭 Choose a Visualization Tool

    This dashboard suite helps you explore the Artificial Intelligence research ecosystem in Mexico through bibliometric analysis and co-authorship networks.

    - 📊 **Ecosystem Overview** Explore the general distribution of papers and national versus international author collaboration patterns.  

    - 🕸️ **Institutional Collaboration Network** Visualize dynamic networks of research centers and their evolutionary connections over time.  

    ---

    ### ⏳ Temporal Evolution (Analytical Eras)
    The historical development of the Mexican AI ecosystem is analyzed across **four distinct eras**:
    * **Era 1: The Islands** (1997–2008)
    * **Era 2: The Bridges** (2009–2019)
    * **Era 3: Forced Virtualization** (2020–2022)
    * **Era 4: Solid Networks** (2023–2026)
    """, unsafe_allow_html=True)
    st.markdown("---")
