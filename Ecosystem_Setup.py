import pandas as pd
import networkx as nx
import itertools

def load_clean_data():
    """Lee el dataset generado en Colab desde la carpeta local."""
    df = pd.read_csv("Data/data.csv")
    df['year'] = df['year'].astype(int)
    return df

def build_network(df_periodo):
    """Tu lógica exacta de Colab para construir las conexiones."""
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
    """Calcula las posiciones espaciales base usando tus parámetros de Colab."""
    G_total = build_network(df_final)
    pos = nx.spring_layout(
        G_total,
        seed=42,
        k=1.8,
        iterations=400,
        scale=3.0
    )
    return pos

def obtener_mapeo_paises(df_final):
    """Diccionario para saber qué país le corresponde a cada institución."""
    return (
        df_final[['institution_clean', 'Country']]
        .dropna()
        .drop_duplicates()
        .groupby('institution_clean')['Country']
        .first()
        .to_dict()
    )
