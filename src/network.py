import networkx as nx
import itertools

def build_network(df):
    G = nx.Graph()

    for _, grupo in df.groupby("title"):
        institutions = grupo["institution_clean"].dropna().unique()

        for a, b in itertools.combinations(institutions, 2):
            if G.has_edge(a, b):
                G[a][b]["weight"] += 1
            else:
                G.add_edge(a, b, weight=1)

        if len(institutions) == 1:
            G.add_node(institutions[0])

    return G
