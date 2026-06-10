import streamlit as st
import networkx as nx
import numpy as np

from src.data_loader import load_data
from src.network import build_network

st.title("🕸️ Collaboration Network")

df = load_data()

# filtros placeholder
year = st.slider("Year", int(df.year.min()), int(df.year.max()), int(df.year.max()))

df_filtered = df[df["year"] <= year]

G = build_network(df_filtered)

st.write("Nodes:", G.number_of_nodes())
st.write("Edges:", G.number_of_edges())

# layout fijo (importante)
pos = nx.spring_layout(G, seed=42, k=1.5, iterations=200)

# node sizes simple placeholder
degree = dict(G.degree())

labels = {
    n: n for n, d in degree.items() if d >= 4
}

node_sizes = [degree.get(n, 1) * 50 for n in G.nodes()]

node_colors = ["green" if "UNAM" in n else "lightblue" for n in G.nodes()]
edge_colors = ["gray"] * len(G.edges())
edge_widths = [1] * len(G.edges())

import matplotlib.pyplot as plt
from src.visualization import draw_network

fig = draw_network(
    G, pos,
    node_sizes=node_sizes,
    node_colors=node_colors,
    edge_colors=edge_colors,
    edge_widths=edge_widths
)

st.pyplot(fig)
