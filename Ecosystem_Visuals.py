import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network

def draw_network_graph(G, pos, institution_country_map, df_periodo, has_focus, focus_nodes, selected_institutions):
    """Dibuja la red interactiva con físicas moleculares en pantalla."""
    nt = Network(height="750px", width="100%", bgcolor="#ffffff", font_color="#333333")
    nt.from_nx(G)
    
    paper_count = df_periodo.groupby('institution_clean')['title'].nunique().to_dict()
    all_nodes = list(G.nodes())
    
    # Aplicamos estilos interactivos, colores y hovers nodo por nodo
    for node in nt.nodes:
        node_id = node['id']
        country = institution_country_map.get(node_id, "Unknown")
        is_mexico = country == "Mexico"
        
        node['color'] = {
            'background': "tab:green" if is_mexico else "#EBF6FF",
            'border': "black"
        }
        node['borderWidth'] = 1.5
        
        p_count = paper_count.get(node_id, 1)
        node['size'] = 15 + (np.log1p(p_count) * 15)
        node['title'] = f"<b>{node_id}</b><br>País: {country}<br>Papers: {p_count}"
        
        # Efecto de transparencia si el usuario resalta una institución específica
        if has_focus:
            if node_id in focus_nodes:
                node['color']['background'] = "tab:green" if is_mexico else "#EBF6FF"
            else:
                node['color']['background'] = "rgba(200, 200, 200, 0.1)"
                node['color']['border'] = "rgba(0,0,0,0.1)"
                node['font'] = {'color': 'rgba(0,0,0,0.1)'}

    # Configuración visual de las líneas de conexión
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
            
        edge['width'] = 1 + np.log1p(G[u][v]["weight"])
        
        if has_focus:
            if u not in selected_institutions and v not in selected_institutions:
                edge['color'] = "rgba(200, 200, 200, 0.02)"

    # Ajustes del motor de física en tiempo real para evitar encimamientos
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
    """Muestra el top 10 lateral usando Matplotlib."""
    top_instituciones = df_periodo['institution_clean'].value_counts().head(10)

    if not top_instituciones.empty:
        fig_barras, ax_barras = plt.subplots(figsize=(4, 5))
        y_labels = top_instituciones.index[::-1]
        x_values = top_instituciones.values[::-1]
        
        bar_colors = ["tab:green" if institution_country_map.get(inst, "Unknown") == "Mexico" else "#EBF6FF" for inst in y_labels]
        bar_alphas = [1.0 if not has_focus or inst in focus_nodes else 0.15 for inst in y_labels]
        
        bars = ax_barras.barh(y_labels, x_values, color=bar_colors, edgecolor='black', height=0.5)
        for i, bar in enumerate(bars):
            bar.set_alpha(bar_alphas[i])
        
        ax_barras.tick_params(axis='both', labelsize=10)
        ax_barras.spines['top'].set_visible(False)
        ax_barras.spines['right'].set_visible(False)
        ax_barras.spines['left'].set_color('#cccccc')
        ax_barras.spines['bottom'].set_color('#cccccc')
        
        ax_barras.bar_label(bars, padding=5, fontsize=10, fontweight='bold', color='#333333')
        ax_barras.xaxis.grid(True, linestyle='--', alpha=0.3, color='#999999')
        ax_barras.set_axisbelow(True)
        
        fig_barras.tight_layout()
        st.pyplot(fig_barras, use_container_width=True)
    else:
        st.info("Sin suficientes datos.")
