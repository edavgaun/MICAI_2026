import streamlit as st
import pandas as pd
import networkx as nx
import itertools

# ==============================================================================
# MÓDULO DE CONFIGURACIÓN, CARGA DE DATOS Y OPERACIONES
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
    st.caption("Avalos-Gauna, E. (2026). *Tracing Institutional Collaboration and Temporal Dynamics Across the Mexican AI Landscape*. Proceedings of the Mexican International Conference on Artificial Intelligence (MICAI).")

def show_main_instructions():
    """Muestra las instrucciones globales de navegación y las eras analíticas."""
    st.markdown("""
    ### 🧭 Choose a Visualization Tool

    This dashboard suite helps you explore the Artificial Intelligence research ecosystem in Mexico through bibliometric analysis and co-authorship networks.

    - 📊 **Ecosystem Overview** Explore the general distribution of papers and national versus international author collaboration patterns.  

    - 🕸️ **Institutional Collaboration Network** Visualize dynamic networks of research centers and their evolutionary connections over time.  

    ---

    ### 🖥️ Sidebar Control Center
    > 💡 **Navigation & Controls Location:** All analytical pages, metric filters, time sliders, and search parameters are located in the **collapsible dashboard panel strictly on the left side** of your screen. You can expand or hide this control menu using the arrow button at the top-left corner.

    ---

    ### ⏳ Temporal Evolution (Analytical Eras)
    The historical development of the Mexican AI ecosystem is analyzed across **four distinct eras**:
    * **Era 1: The Islands** (1997–2008)
    * **Era 2: The Bridges** (2009–2019)
    * **Era 3: Forced Virtualization** (2020–2022)
    * **Era 4: Solid Networks** (2023–2026)
    """, unsafe_allow_html=True)
    st.markdown("---")

def build_network(df_periodo):
    """Construye la estructura matemática de la red para el periodo dado."""
    G = nx.Graph()
    for _, grupo in df_periodo.groupby('title'):
        instituciones = grupo['institution_clean'].dropna().unique()
        for a, b in itertools.combinations(instituciones, 2):
            if G.has_edge(a, b):
                G[a][b]['weight'] += 1
            else:
                G.add_edge(a, b, weight=1)
        if len(instituciones) == 1:
            G.add_node(instituciones[0])
    return G


def calcular_layout_fijo(df_final):
    """Calcula las coordenadas (x, y) de los nodos de forma matemática pura."""
    G_total = build_network(df_final)
    pos = nx.spring_layout(G_total, seed=42, k=1.8, iterations=400, scale=3.0)
    return pos
