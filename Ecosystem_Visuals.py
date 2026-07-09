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

def draw_network_graph(G, pos, institution_country_map, df_periodo, has_focus, focus_nodes, selected_institutions, selected_year, dropdown_area):
    """Dibuja la red interactiva con tamaños jerárquicos reales y un botón para descargar como imagen con nomenclatura."""
    nt = Network(height="750px", width="100%", bgcolor="#ffffff", font_color="#333333")
    
    paper_count = calcular_metricas_periodo(df_periodo)
    num_nodos = len(G.nodes())
    
    # 1. CONSTRUCCIÓN DE NODOS CON TAMAÑOS REALES Y JERÁRQUICOS
    for i, node_id in enumerate(G.nodes()):
        country = institution_country_map.get(node_id, "Unknown")
        is_mexico = country == "Mexico"
        p_count = paper_count.get(node_id, 1)
        
        if p_count == 1:
            size_value = 6
        else:
            size_value = 8 + (np.log1p(p_count) * 8)
        
        if node_id in pos:
            x_pos = pos[node_id][0] * 250
            y_pos = pos[node_id][1] * 250
        else:
            angulo = i * (2 * np.pi / max(num_nodos, 1))
            x_pos = np.cos(angulo) * 550
            y_pos = np.sin(angulo) * 550
            
        bg_color = "#2ca02c" if is_mexico else "#EBF6FF"
        border_color = "black"
        font_color = "#333333"
        
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
            borderWidth=1.2,
            color={'background': bg_color, 'border': border_color},
            font={'size': 11, 'color': font_color},
            title=f"Institución: {node_id}\nPaís: {country}\nPapers: {p_count}"
        )

    # 2. CONSTRUCCIÓN DE ARISTAS
    for u, v in G.edges():
        edge_data = G.get_edge_data(u, v) or G.get_edge_data(v, u) or {}
        peso = edge_data.get("weight", 1)
        width_value = 1 + np.log1p(peso)
        
        country_u = institution_country_map.get(u, "Unknown")
        country_v = institution_country_map.get(v, "Unknown")
        
        if country_u == "Mexico" and country_v == "Mexico":
            edge_color = "rgba(44, 160, 44, 0.5)"
        elif country_u != "Mexico" and country_v != "Mexico":
            edge_color = "rgba(211, 211, 211, 0.3)"
        else:
            edge_color = "rgba(255, 127, 14, 0.5)"

        if has_focus and (u not in selected_institutions and v not in selected_institutions):
            edge_color = "rgba(200, 200, 200, 0.01)"
            
        nt.add_edge(u, v, width=width_value, color=edge_color)

    # 3. FÍSICAS DE ESTABILIZACIÓN ULTRA-RÁPIDAS
    nt.set_options("""
    {
      "physics": {
        "enabled": true,
        "barnesHut": {
          "gravitationalConstant": -4000,
          "centralGravity": 0.15,
          "springLength": 90,
          "springConstant": 0.05,
          "damping": 0.09
        },
        "stabilization": {
          "enabled": true,
          "iterations": 100,
          "updateInterval": 25
        }
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
    
    # 4. INYECCIÓN JAVASCRIPT PARA BOTÓN DE DESCARGA Y NOMENCLATURA
    with open("temp_network.html", 'r', encoding='utf-8') as f:
        html_content = f.read()

    js_injection = f"""
    <div id="download-container" style="position: absolute; top: 15px; right: 15px; z-index: 9999;">
        <button id="download-btn" style="
            background-color: #ff4b4b; 
            color: white; 
            border: none; 
            padding: 10px 18px; 
            border-radius: 6px; 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; 
            font-size: 14px; 
            cursor: pointer; 
            font-weight: 600;
            box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
            transition: background 0.2s;
        " onmouseover="this.style.backgroundColor='#e03e3e'" onmouseout="this.style.backgroundColor='#ff4b4b'">
            📸 Descargar Red (PNG)
        </button>
    </div>
    <script>
    document.getElementById('download-btn').addEventListener('click', function() {{
        var originalCanvas = document.querySelector('canvas');
        if (!originalCanvas) {{
            alert('Error al acceder al lienzo del mapa.');
            return;
        }}
        
        // Crear un lienzo temporal para componer la imagen final
        var tempCanvas = document.createElement('canvas');
        tempCanvas.width = originalCanvas.width;
        tempCanvas.height = originalCanvas.height;
        var ctx = tempCanvas.getContext('2d');
        
        // Fondo blanco sólido para que no sea transparente
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(0, 0, tempCanvas.width, tempCanvas.height);
        
        # Dibujar la red actual tal y como está posicionada por el usuario
        ctx.drawImage(originalCanvas, 0, 0);
        
        // --- TEXTO DE METADATOS (Esquina Superior Izquierda) ---
        ctx.fillStyle = '#1e1e1e';
        ctx.font = 'bold 24px sans-serif';
        ctx.fillText('Ecosistema de IA en México', 35, 50);
        
        ctx.font = '15px sans-serif';
        ctx.fillStyle = '#555555';
        ctx.fillText('Año de corte: ' + "{selected_year}", 35, 80);
        ctx.fillText('Área de Investigación: ' + "{dropdown_area}", 35, 105);
        
        // --- CUADRO DE LEYENDA / NOMENCLATURA (Esquina Inferior Izquierda) ---
        var boxWidth = 280;
        var boxHeight = 180;
        var x = 35;
        var y = tempCanvas.height - boxHeight - 35;
        
        // Fondo del cuadro
        ctx.fillStyle = '#f8f9fa';
        ctx.strokeStyle = '#e0e0e0';
        ctx.lineWidth = 1.5;
        if (ctx.roundRect) {{
            ctx.beginPath(); ctx.roundRect(x, y, boxWidth, boxHeight, 10); ctx.fill(); ctx.stroke();
        }} else {{
            ctx.fillRect(x, y, boxWidth, boxHeight); ctx.strokeRect(x, y, boxWidth, boxHeight);
        }}
        
        // Título de la Guía
        ctx.fillStyle = '#222222';
        ctx.font = 'bold 15px sans-serif';
        ctx.fillText('📍 Guía de la Red', x + 15, y + 28);
        
        // Línea decorativa verde
        ctx.strokeStyle = '#2ca02c';
        ctx.lineWidth = 2.5;
        ctx.beginPath(); ctx.moveTo(x + 15, y + 36); ctx.lineTo(x + 130, y + 36); ctx.stroke();
        
        ctx.font = '13px sans-serif';
        
        // Nodo México
        ctx.fillStyle = '#2ca02c';
        ctx.strokeStyle = '#000000';
        ctx.lineWidth = 1;
        ctx.beginPath(); ctx.arc(x + 25, y + 60, 7, 0, 2 * Math.PI); ctx.fill(); ctx.stroke();
        ctx.fillStyle = '#333333'; ctx.fillText('Institución México', x + 45, y + 64);
        
        // Nodo Extranjero
        ctx.fillStyle = '#EBF6FF';
        ctx.beginPath(); ctx.arc(x + 25, y + 82, 7, 0, 2 * Math.PI); ctx.fill(); ctx.stroke();
        ctx.fillStyle = '#333333'; ctx.fillText('Institución Extranjero', x + 45, y + 86);
        
        // Arista Nacional (Mx-Mx)
        ctx.strokeStyle = 'rgba(44, 160, 44, 0.8)'; ctx.lineWidth = 3.5;
        ctx.beginPath(); ctx.moveTo(x + 15, y + 112); ctx.lineTo(x + 35, y + 112); ctx.stroke();
        ctx.fillStyle = '#333333'; ctx.fillText('Colaboración Nacional (Mx-Mx)', x + 45, y + 116);
        
        // Arista Internacional (Mx-Ext)
        ctx.strokeStyle = 'rgba(255, 127, 14, 0.8)';
        ctx.beginPath(); ctx.moveTo(x + 15, y + 134); ctx.lineTo(x + 35, y + 134); ctx.stroke();
        ctx.fillStyle = '#333333'; ctx.fillText('Colaboración Internacional (Mx-Ext)', x + 45, y + 138);
        
        // Arista Global (Ext-Ext)
        ctx.strokeStyle = 'rgba(211, 211, 211, 0.7)';
        ctx.beginPath(); ctx.moveTo(x + 15, y + 156); ctx.lineTo(x + 35, y + 156); ctx.stroke();
        ctx.fillStyle = '#333333'; ctx.fillText('Colaboración Global (Ext-Ext)', x + 45, y + 160);
        
        // --- DETONAR DESCARGA ---
        var safeAreaName = "{dropdown_area}".replace(/[^a-zA-Z0-9]/g, "_");
        var link = document.createElement('a');
        link.download = 'Red_IA_Mexico_' + "{selected_year}" + '_' + safeAreaName + '.png';
        link.href = tempCanvas.toDataURL('image/png');
        link.click();
    }});
    </script>
    """
    
    # Insertar el código justo antes del cierre de la etiqueta body
    html_content = html_content.replace("</body>", js_injection + "</body>")
    
    components.html(html_content, height=760)
def draw_volume_bars(df_periodo, institution_country_map, has_focus, focus_nodes):
    # Ajuste metodológico: Conteo por títulos únicos para corregir el sesgo de coautorías internas
    counts = df_periodo.groupby('institution_clean')['title'].nunique().reset_index()
    counts.columns = ['Institución', 'Papers']
    counts = counts.sort_values(by='Papers', ascending=False).head(10)
    
    counts['Color'] = counts['Institución'].apply(lambda x: '#2ca02c' if institution_country_map.get(x, 'Unknown') == 'Mexico' else '#EBF6FF')
    counts['Opacity'] = counts['Institución'].apply(lambda x: 1.0 if not has_focus or x in focus_nodes else 0.15)

    if not counts.empty:
        chart = alt.Chart(counts).mark_bar(stroke='black', strokeWidth=1).encode(
            x=alt.X('Papers:Q', title='Papers'),
            y=alt.Y('Institución:N', sort='-x', title=None),
            color=alt.Color('Color:N', scale=None),
            opacity=alt.Opacity('Opacity:Q', scale=None),
            tooltip=['Institución', 'Papers']
        ).properties(
            width='container',
            height=350  # Reducido ligeramente para dar espacio a la leyenda
        )
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("Sin suficientes datos.")
