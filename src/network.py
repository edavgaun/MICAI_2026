import networkx as nx
import itertools
import streamlit as st

@st.cache_data
def build_network(df_periodo):
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

@st.cache_asset
def calcular_layout_fijo(df_final):
    """Calcula el layout usando TODO el dataset para que los nodos no bailen."""
    G_total = build_network(df_final)
    pos = nx.spring_layout(
        G_total,
        seed=42,
        k=1.8,              
        iterations=400,     
        scale=3.0           
    )
    return pos
