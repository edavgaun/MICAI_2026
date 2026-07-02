import pandas as pd
import networkx as nx
import numpy as np

def load_clean_data():
    """Loads and returns the processed DataFrame from your storage."""
    # Place your actual data loading logic here
    # Must return a pandas DataFrame containing: 'year', 'research_area', 'institution_clean', 'Country', 'title'
    pass

def calcular_layout_fijo(df):
    """Calculates a global, static coordinate layout for all unique nodes."""
    G = build_network(df)
    # Returns a dictionary of {node: (x, y)} using spring_layout or your preferred placement
    return nx.spring_layout(G, seed=42)

def build_network(df):
    """Constructs a NetworkX Graph based on co-authorship interactions."""
    G = nx.Graph()
    # Your logic that populates nodes and edge ['weight'] metrics from the filtered DataFrame
    return G
