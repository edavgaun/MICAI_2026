import altair as alt
import numpy as np
import networkx as nx
import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network

@st.cache_data
def calcular_metricas_periodo(df_periodo):
    """🧠 Almacena el conteo de papers en caché para evitar recalcular el groupby con cada filtro."""
    return df_periodo.groupby('institution_clean')['title'].nunique().to_dict()

def draw_network_graph(G, pos, institution_country_map, df_periodo, has_focus, focus_nodes, selected_institutions):
    """Dibuja la red interactiva con el tamaño de nodos corregido y rendimiento optimizado."""
    nt = Network(height="750px", width="100%", bgcolor="#ffffff", font_color="#333333")
    
    paper_count = calcular_metricas_periodo(df_periodo)
    num_nodos = len(G.nodes())
    
    # 🛠️ CONSTRUCCIÓN EXPLÍCITA: Añadimos los nodos uno por uno controlando sus propiedades reales
    for i, node_id in enumerate(G.nodes()):
        country = institution_country_map.get(node_id, "Unknown")
        is_mexico = country == "Mexico"
        p_count = paper_count.get(node_id, 1)
        
        # Fórmula original exacta para el tamaño (pequeño para 1 paper, escala controlada para más)
        size_value = 10 + (np.log1p(p_count) * 10)
        
        # Posicionamiento estático
        if node_id in pos:
            x_pos = pos[node_id][0] * 300
            y_pos = pos[node_id][1] * 300
        else:
            angulo = i * (2 * np.pi / max(num_nodos, 1))
            x_pos = np.cos(angulo) * 650
            y_pos = np.sin(angulo) * 650
            
        # Color base
        bg_color = "#2ca02c" if is_mexico else "#EBF6FF"
        border_color = "black"
        font_color = "#333333"
        
        # Filtro de enfoque
        if has_focus and node_id not in focus_nodes:
            bg_color = "rgba(200, 200, 200, 0.1)"
            border_color = "rgba(0,0,0,0.1)"
            font_color = "rgba(0,0,0,0.1)"
            
        nt.add_node(
            node_id,
            label=node_id,
            size=size_value,
            x=x_pos,
            y=y_pos,
            physics=False,
            borderWidth=1.5,
            color={'background': bg_color, 'border': border_color},
            font={'color': font_color},
            title=f"Institución: {node_id}\nPaís: {country}\nPapers: {p_count}"
        )

    # Añadimos las aristas de forma explícita
    for u, v in G.edges():
        edge_data = G.get_edge_data(u, v) or G.get_edge_data(v, u) or {}
        peso = edge_data.get("weight", 1)
        width_value = 1 + np.log1p(peso)
        
        country_u = institution_country_map.get(u, "Unknown")
        country_v = institution_country_map.get(v, "Unknown")
        
        if country_u == "Mexico" and country_v == "Mexico":
            edge_color = "rgba(44, 160, 44, 0.6)"
        elif country_u != "Mexico" and country_v != "Mexico":
            edge_color = "rgba(211, 211, 211, 0.4)"
        else:
            edge_color = "rgba(255, 127, 14, 0.6)"

        if has_focus and (u not in selected_institutions and v not in selected_institutions):
            edge_color = "rgba(200, 200, 200, 0.02)"
            
        nt.add_edge(u, v, width=width_value, color=edge_color)

    # Configuración estática ultra-veloz
    nt.set_options("""
    {
      "physics": {
        "enabled": false
      },
      "interaction": {
        "hover": true,
        "tooltipDelay": 100,
        "hideEdgesOnDrag": true,
        "hideEdgesOnZoom": true
      }
    }
    """)
    
    nt.save_graph("temp_network.html")
    with open("temp_network.html", 'r', encoding='utf-8') as f:
        components.html(f.read(), height=760)

def draw_volume_bars(df_periodo, institution_country_map, has_focus, focus_nodes):
    counts = df_periodo['institution_clean'].value_counts().head(10).reset_index()
    counts.columns = ['Institución', 'Papers']
    
    counts['Color'] = counts['Institución'].apply(lambda x: '#2ca02c' if institution_country_map.get(x, 'Unknown') == 'Mexico' else '#EBF6FF')
    counts['Opacity'] = counts['Institución'].apply(lambda x: 1.0 if not has_focus or x in focus_nodes else 0.15)

    if not counts.empty:
        chart = alt.Chart(counts).mark_bar(stroke='black', strokeWidth=1).encode(
            x=alt.X('Papers:Q', title='Papers'),
            y=alt.Y('Institución:N', sort='-x', title=None),
            color=alt.Color('Color:N', scale=None),
            opacity=alt.Opacity('Opacity:Q', scale=None),
            tooltip=['Institución', 'Papers']
        ).properties(width='container', height=400)
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("Sin suficientes datos.")
