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
    """Dibuja la red interactiva destacando con borde rojo los 5 nodos más grandes."""
    nt = Network(height="750px", width="100%", bgcolor="#ffffff", font_color="#333333")
    
    paper_count = calcular_metricas_periodo(df_periodo)
    num_nodos = len(G.nodes())
    
    # 🌟 FILTRO DE RELEVANCIA: Identificar las 5 instituciones más grandes (con más papers)
    top_5_grandes = set(sorted(paper_count, key=paper_count.get, reverse=True)[:5])
    
    # 1. CONSTRUCCIÓN DE NODOS CON TAMAÑOS REALES Y BORDES DESTACADOS
    for i, node_id in enumerate(G.nodes()):
        country = institution_country_map.get(node_id, "Unknown")
        is_mexico = country == "Mexico"
        p_count = paper_count.get(node_id, 1)
        
        if p_count == 1:
            size_value = 6
        else:
            size_value = 8 + (np.log1p(p_count) * 8)
            
        # Forzamos etiquetas vacías para mantener el diseño limpio que funcionó en tu captura
        label_text = ""  
        
        if node_id in pos:
            x_pos = pos[node_id][0] * 250
            y_pos = pos[node_id][1] * 250
        else:
            angulo = i * (2 * np.pi / max(num_nodos, 1))
            x_pos = np.cos(angulo) * 550
            y_pos = np.sin(angulo) * 550
            
        bg_color = "#2ca02c" if is_mexico else "#EBF6FF"
        
        # 🔴 LÓGICA DEL BORDE ROJO PARA EL TOP 5 MAS GRANDES
        if node_id in top_5_grandes:
            border_color = "#FF0000"  # Rojo brillante
            border_width = 3.5        # Más grueso para notar la jerarquía
        else:
            border_color = "#000000"  # Negro estándar para el resto
            border_width = 1.2
        
        # Si el usuario usa el buscador y resalta nodos, aplicamos la opacidad protectora
        if has_focus and node_id not in focus_nodes:
            bg_color = "rgba(200, 200, 200, 0.1)"
            border_color = "rgba(0,0,0,0.1)"
            border_width = 1.2
            
        nt.add_node(
            node_id,
            label=label_text,
            size=size_value,
            x=x_pos,
            y=y_pos,
            borderWidth=border_width,
            color={'background': bg_color, 'border': border_color},
            font={'size': 10, 'color': '#333333', 'face': 'sans-serif'},
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
    
    # 4. INYECCIÓN JAVASCRIPT CON PLAN DE RESPALDO (MODAL) CONTRA BLOQUEOS DE IFRAME
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
        try {{
            var originalCanvas = document.querySelector('.vis-network canvas') || document.querySelector('canvas');
            if (!originalCanvas) {{
                alert('El lienzo del grafo aún no está listo. Intenta de nuevo en unos segundos.');
                return;
            }}
            
            var tempCanvas = document.createElement('canvas');
            tempCanvas.width = originalCanvas.width;
            tempCanvas.height = originalCanvas.height;
            var ctx = tempCanvas.getContext('2d');
            
            ctx.fillStyle = '#ffffff';
            ctx.fillRect(0, 0, tempCanvas.width, tempCanvas.height);
            
            ctx.drawImage(originalCanvas, 0, 0);
            
            // --- TEXTO DE METADATOS ---
            ctx.fillStyle = '#1e1e1e';
            ctx.font = 'bold 24px sans-serif';
            ctx.fillText('Ecosistema de IA en México', 35, 50);
            
            ctx.font = '15px sans-serif';
            ctx.fillStyle = '#555555';
            ctx.fillText('Año de corte: ' + "{selected_year}", 35, 80);
            ctx.fillText('Área de Investigación: ' + "{dropdown_area}", 35, 105);
            
            // --- CUADRO DE LEYENDA / NOMENCLATURA ---
            var boxWidth = 290;
            var boxHeight = 185;
            var x = 35;
            var y = tempCanvas.height - boxHeight - 35;
            
            ctx.fillStyle = '#f8f9fa';
            ctx.strokeStyle = '#e0e0e0';
            ctx.lineWidth = 1.5;
            if (ctx.roundRect) {{
                ctx.beginPath(); ctx.roundRect(x, y, boxWidth, boxHeight, 10); ctx.fill(); ctx.stroke();
            }} else {{
                ctx.fillRect(x, y, boxWidth, boxHeight); ctx.strokeRect(x, y, boxWidth, boxHeight);
            }}
            
            ctx.fillStyle = '#222222';
            ctx.font = 'bold 15px sans-serif';
            ctx.fillText('📍 Guía de la Red', x + 15, y + 28);
            
            ctx.strokeStyle = '#2ca02c';
            ctx.lineWidth = 2.5;
            ctx.beginPath(); ctx.moveTo(x + 15, y + 36); ctx.lineTo(x + 130, y + 36); ctx.stroke();
            
            ctx.font = '13px sans-serif';
            
            ctx.fillStyle = '#2ca02c'; ctx.strokeStyle = '#000000'; ctx.lineWidth = 1;
            ctx.beginPath(); ctx.arc(x + 25, y + 60, 7, 0, 2 * Math.PI); ctx.fill(); ctx.stroke();
            ctx.fillStyle = '#333333'; ctx.fillText('Institución México', x + 45, y + 64);
            
            ctx.fillStyle = '#EBF6FF';
            ctx.beginPath(); ctx.arc(x + 25, y + 82, 7, 0, 2 * Math.PI); ctx.fill(); ctx.stroke();
            ctx.fillStyle = '#333333'; ctx.fillText('Institución Extranjero', x + 45, y + 86);
            
            ctx.strokeStyle = 'rgba(44, 160, 44, 0.8)'; ctx.lineWidth = 3.5;
            ctx.beginPath(); ctx.moveTo(x + 15, y + 112); ctx.lineTo(x + 35, y + 112); ctx.stroke();
            ctx.fillStyle = '#333333'; ctx.fillText('Colaboración Nacional (Mx-Mx)', x + 45, y + 116);
            
            ctx.strokeStyle = 'rgba(255, 127, 14, 0.8)';
            ctx.beginPath(); ctx.moveTo(x + 15, y + 134); ctx.lineTo(x + 35, y + 134); ctx.stroke();
            ctx.fillStyle = '#333333'; ctx.fillText('Colaboración Internacional (Mx-Ext)', x + 45, y + 138);
            
            ctx.strokeStyle = 'rgba(211, 211, 211, 0.7)';
            ctx.beginPath(); ctx.moveTo(x + 15, y + 156); ctx.lineTo(x + 35, y + 156); ctx.stroke();
            ctx.fillStyle = '#333333'; ctx.fillText('Colaboración Global (Ext-Ext)', x + 45, y + 160);
            
            var dataUrl = tempCanvas.toDataURL('image/png');
            var safeAreaName = "{dropdown_area}".replace(/[^a-zA-Z0-9]/g, "_");
            var filename = 'Red_IA_Mexico_' + "{selected_year}" + '_' + safeAreaName + '.png';
            
            var link = document.createElement('a');
            link.download = filename;
            link.href = dataUrl;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            
            var existingModal = document.getElementById('preview-modal');
            if (existingModal) existingModal.remove();
            
            var modal = document.createElement('div');
            modal.id = 'preview-modal';
            modal.style.position = 'absolute';
            modal.style.top = '0';
            modal.style.left = '0';
            modal.style.width = '100%';
            modal.style.height = '100%';
            modal.style.backgroundColor = 'rgba(255,255,255,0.97)';
            modal.style.zIndex = '10000';
            modal.style.display = 'flex';
            modal.style.flexDirection = 'column';
            modal.style.alignItems = 'center';
            modal.style.justifyContent = 'center';
            modal.style.fontFamily = 'sans-serif';
            modal.style.padding = '20px';
            modal.style.boxSizing = 'border-box';
            
            modal.innerHTML = `
                <div style="text-align: center; margin-bottom: 12px; max-width: 550px;">
                    <h3 style="margin: 0 0 5px 0; color: #111;">📸 Captura lista con Éxito</h3>
                    <p style="margin: 0; font-size: 13px; color: #555;">Si la descarga no inició automáticamente, haz <b>clic derecho</b> sobre la imagen inferior y selecciona <b>"Guardar imagen como..."</b>.</p>
                    <button id="close-modal-btn" style="margin-top: 10px; background: #ff4b4b; color: white; border: none; padding: 7px 15px; border-radius: 5px; cursor: pointer; font-weight: bold;">Volver al Mapa Interactivo</button>
                </div>
                <img src="${{dataUrl}}" style="max-width: 95%; max-height: 75%; border: 1px solid #ddd; box-shadow: 0 4px 15px rgba(0,0,0,0.15); border-radius:4px;"/>
            `;
            
            document.body.appendChild(modal);
            document.getElementById('close-modal-btn').addEventListener('click', function() {{
                modal.remove();
            }});
            
        }} catch (err) {{
            alert('Error al componer la imagen de la red: ' + err.message);
        }}
    }});
    </script>
    """
    
    html_content = html_content.replace("</body>", js_injection + "</body>")
    components.html(html_content, height=760)

def draw_volume_bars(df_periodo, institution_country_map, has_focus, focus_nodes):
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
            height=350
        )
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("Sin suficientes datos.")
