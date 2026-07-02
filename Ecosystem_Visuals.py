import altair as alt
import numpy as np
import networkx as nx
import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network

def draw_network_graph(G, pos, institution_country_map, df_periodo, has_focus, focus_nodes, selected_institutions):
    """Dibuja la red interactiva con físicas moleculares en pantalla usando Pyvis."""
    nt = Network(height="750px", width="100%", bgcolor="#ffffff", font_color="#333333")
    nt.from_nx(G)
    
    paper_count = df_periodo.groupby('institution_clean')['title'].nunique().to_dict()
    all_nodes = list(G.nodes())
    
    # Estilos de nodos
    for node in nt.nodes:
        node_id = node['id']
        country = institution_country_map.get(node_id, "Unknown")
        is_mexico = country == "Mexico"
        
        node['color'] = {
            'background': "#2ca02c" if is_mexico else "#EBF6FF",
            'border': "black"
        }
        node['borderWidth'] = 1.5
        
        p_count = paper_count.get(node_id, 1)
        node['size'] = 15 + (np.log1p(p_count) * 15)
        node['title'] = f"<b>{node_id}</b><br>País: {country}<br>Papers: {p_count}"
        
        if has_focus:
            if node_id in focus_nodes:
                node['color']['background'] = "#2ca02c" if is_mexico else "#EBF6FF"
            else:
                node['color']['background'] = "rgba(200, 200, 200, 0.1)"
                node['color']['border'] = "rgba(0,0,0,0.1)"
                node['font'] = {'color': 'rgba(0,0,0,0.1)'}

    # Estilos de aristas utilizando consultas seguras
    for edge in nt.edges:
        u, v = edge['from'], edge['to']
        country_u = institution_country_map.get(u, "Unknown")
        country_v = institution_country_map.get(v, "Unknown")
        
        if country_u == "Mexico" and country_v == "Mexico":
            edge['color'] = "rgba(44, 160, 44, 0.6)"
        elif country_u != "Mexico" and country_v != "Mexico":
            edge['color'] = "rgba(211, 211, 211, 0.4)"
        else:
            edge['color'] = "rgba(255, 127, 14, 0.6)"
            
        # SOLUCIÓN DEFINITIVA: Buscamos los datos de la arista de forma segura en NetworkX
        edge_data = G.get_edge_data(u, v) or G.get_edge_data(v, u) or {}
        peso = edge_data.get("weight", 1)

        edge['width'] = 1 + np.log1p(peso)
        
        if has_focus:
            if u not in selected_institutions and v not in selected_institutions:
                edge['color'] = "rgba(200, 200, 200, 0.02)"

    # Físicas de la red
    nt.set_options("""
    var options = {
      "physics": {
        "barnesHut": {
          "gravitationalConstant": -6000,
          "centralGravity": 0.2,
          "springLength": 120,
          "springConstant": 0.04
        },
        "minVelocity": 0.75
      },
      "nodes": {
        "font": { "size": 12, "face": "sans-serif" }
      }
    }
    """)
    
    nt.save_graph("temp_network.html")
    with open("temp_network.html", 'r', encoding='utf-8') as f:
        html_source = f.read()
        
    components.html(html_source, height=760)


def draw_volume_bars(df_periodo, institution_country_map, has_focus, focus_nodes):
    """Muestra el top 10 de volumen de forma interactiva usando Altair nativo."""
    counts = df_periodo['institution_clean'].value_counts().head(10).reset_index()
    counts.columns = ['Institución', 'Papers']
    
    counts['Color'] = counts['Institución'].apply(
        lambda x: '#2ca02c' if institution_country_map.get(x, 'Unknown') == 'Mexico' else '#EBF6FF'
    )
    counts['Opacity'] = counts['Institución'].apply(
        lambda x: 1.0 if not has_focus or x in focus_nodes else 0.15
    )

    if not counts.empty:
        chart = alt.Chart(counts).mark_bar(stroke='black', strokeWidth=1).encode(
            x=alt.X('Papers:Q', title='Cantidad de Papers'),
            y=alt.Y('Institución:N', sort='-x', title=None),
            color=alt.Color('Color:N', scale=None),
            opacity=alt.Opacity('Opacity:Q', scale=None),
            tooltip=['Institución', 'Papers']
        ).properties(
            width='container',
            height=400
        )
        
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("Sin suficientes datos.")
