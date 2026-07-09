import altair as alt
import numpy as np
import networkx as nx
import streamlit as st
import streamlit.components.v1 as components
from pyvis.network import Network
import json

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
    
    # 📊 PREPARACIÓN DE DATOS PARA LA MINI GRÁFICA EN EL CANVAS
    top_10_raw = sorted(paper_count.items(), key=lambda x: x[1], reverse=True)[:10]
    bar_data_list = []
    for idx, (inst, count) in enumerate(top_10_raw):
        country = institution_country_map.get(inst, "Unknown")
        color = '#2ca02c' if country == 'Mexico' else '#EBF6FF'
        bar_data_list.append({
            "name": inst,
            "papers": int(count),
            "is_top5": idx < 5,
            "color": color
        })
    js_bar_data_json = json.dumps(bar_data_list)
    
    # 1. CONSTRUCCIÓN DE NODOS CON TAMAÑOS REALES Y BORDES DESTACADOS
    for i, node_id in enumerate(G.nodes()):
        country = institution_country_map.get(node_id, "Unknown")
        is_mexico = country == "Mexico"
        p_count = paper_count.get(node_id, 1)
        
        if p_count == 1:
            size_value = 6
        else:
            size_value = 8 + (np.log1p(p_count) * 8)
            
        label_text = ""  
        
        if node_id in pos:
            x_pos = pos[node_id][0] * 250
            y_pos = pos[node_id][1] * 250
        else:
            angulo = i * (2 * np.pi / max(num_nodos, 1))
            x_pos = np.cos(angulo) * 550
            y_pos = np.sin(angulo) * 550
            
        bg_color = "#2ca02c" if is_mexico else "#EBF6FF"
        
        if node_id in top_5_grandes:
            border_color = "#FF0000"  
            border_width = 3.5        
        else:
            border_color = "#000000"  
            border_width = 1.2
        
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
    
    with open("temp_network.html", 'r', encoding='utf-8') as f:
        html_content = f.read()

    # 4. PLANTILLA DE EXPORTACIÓN CON MINI GRÁFICA DE BARRAS EN LA ESQUINA INFERIOR DERECHA
    js_template = """
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
    document.getElementById('download-btn').addEventListener('click', function() {
        try {
            var originalCanvas = document.querySelector('.vis-network canvas') || document.querySelector('canvas');
            if (!originalCanvas) {
                alert('El lienzo del grafo aún no está listo. Intenta de nuevo en unos segundos.');
                return;
            }
            
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
            ctx.fillText('Año de corte: __SELECTED_YEAR__', 35, 80);
            ctx.fillText('Área de Investigación: __DROPDOWN_AREA__', 35, 105);
            
            // --- CUADRO DE LEYENDA / NOMENCLATURA (Esquina Inferior Izquierda) ---
            var boxWidth = 290;
            var boxHeight = 185;
            var x = 35;
            var y = tempCanvas.height - boxHeight - 35;
            
            ctx.fillStyle = '#f8f9fa';
            ctx.strokeStyle = '#e0e0e0';
            ctx.lineWidth = 1.5;
            if (ctx.roundRect) {
                ctx.beginPath(); ctx.roundRect(x, y, boxWidth, boxHeight, 10); ctx.fill(); ctx.stroke();
            } else {
                ctx.fillRect(x, y, boxWidth, boxHeight); ctx.strokeRect(x, y, boxWidth, boxHeight);
            }
            
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
            
            // --- 📊 MINI GRÁFICA DE BARRAS INTEGRADA (Esquina Inferior Derecha) ---
            var barData = __BAR_DATA__;
            if (barData && barData.length > 0) {
                var bWidth = 340;
                var bHeight = 240;
                var bx = tempCanvas.width - bWidth - 35;
                var by = tempCanvas.height - bHeight - 35;
                
                // Fondo del contenedor de barras
                ctx.fillStyle = '#f8f9fa';
                ctx.strokeStyle = '#e0e0e0';
                ctx.lineWidth = 1.5;
                if (ctx.roundRect) {
                    ctx.beginPath(); ctx.roundRect(bx, by, bWidth, bHeight, 10); ctx.fill(); ctx.stroke();
                } else {
                    ctx.fillRect(bx, by, bWidth, bHeight); ctx.strokeRect(bx, by, bWidth, bHeight);
                }
                
                // Título del gráfico interno
                ctx.fillStyle = '#222222';
                ctx.font = 'bold 14px sans-serif';
                ctx.fillText('📊 Top 10 Volumen', bx + 15, by + 25);
                
                var maxPapers = barData[0].papers;
                var maxBarWidth = 140; 
                
                ctx.font = '11px sans-serif';
                for (var i = 0; i < barData.length; i++) {
                    var item = barData[i];
                    var rowY = by + 45 + (i * 18);
                    
                    // Texto de la Institución (Truncado de forma segura si es largo)
                    ctx.fillStyle = '#333333';
                    ctx.textAlign = 'left';
                    var displayName = item.name;
                    if (displayName.length > 20) displayName = displayName.substring(0, 18) + '...';
                    ctx.fillText(displayName, bx + 15, rowY + 10);
                    
                    // Dibujo de la barra
                    var barW = (item.papers / maxPapers) * maxBarWidth;
                    if (barW < 3) barW = 3;
                    
                    ctx.fillStyle = item.color;
                    ctx.fillRect(bx + 140, rowY, barW, 12);
                    
                    // Borde condicional: Rojo grueso para Top 5, negro sutil para el resto
                    if (item.is_top5) {
                        ctx.strokeStyle = '#FF0000';
                        ctx.lineWidth = 1.8;
                    } else {
                        ctx.strokeStyle = '#000000';
                        ctx.lineWidth = 0.5;
                    }
                    ctx.strokeRect(bx + 140, rowY, barW, 12);
                    
                    // Número indicador de papers al final de la barra
                    ctx.fillStyle = '#555555';
                    ctx.fillText(item.papers, bx + 146 + barW, rowY + 10);
                }
                ctx.textAlign = 'left'; // Restaurar alineación estándar
            }
            
            // --- DISPARAR DESCARGA AUTOMÁTICA ---
            var dataUrl = tempCanvas.toDataURL('image/png');
            var safeAreaName = "__DROPDOWN_AREA__".replace(/[^a-zA-Z0-9]/g, "_");
            var filename = 'Red_IA_Mexico_' + '__SELECTED_YEAR__' + '_' + safeAreaName + '.png';
            
            var link = document.createElement('a');
            link.download = filename;
            link.href = dataUrl;
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
            
            // --- VENTANA DE RESPALDO INTERNA CONTRA BLOQUEOS ---
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
                <img src="${dataUrl}" style="max-width: 95%; max-height: 75%; border: 1px solid #ddd; box-shadow: 0 4px 15px rgba(0,0,0,0.15); border-radius:4px;"/>
            `;
            
            document.body.appendChild(modal);
            document.getElementById('close-modal-btn').addEventListener('click', function() {
                modal.remove();
            });
            
        } catch (err) {
            alert('Error al componer la imagen de la red: ' + err.message);
        }
    });
    </script>
    """
    
    # Inyección segura mediante reemplazos directos de texto controlado
    js_injection = js_template.replace("__SELECTED_YEAR__", str(selected_year)).replace("__DROPDOWN_AREA__", str(dropdown_area)).replace("__BAR_DATA__", js_bar_data_json)
    
    html_content = html_content.replace("</body>", js_injection + "</body>")
    components.html(html_content, height=760)

def draw_volume_bars(df_periodo, institution_country_map, has_focus, focus_nodes):
    """Dibuja el gráfico de volumen de la UI de Streamlit remarcando el Top 5 con borde rojo."""
    counts = df_periodo.groupby('institution_clean')['title'].nunique().reset_index()
    counts.columns = ['Institución', 'Papers']
    counts = counts.sort_values(by='Papers', ascending=False).head(10).reset_index(drop=True)
    
    counts['Color'] = counts['Institución'].apply(lambda x: '#2ca02c' if institution_country_map.get(x, 'Unknown') == 'Mexico' else '#EBF6FF')
    counts['Opacity'] = counts['Institución'].apply(lambda x: 1.0 if not has_focus or x in focus_nodes else 0.15)
    
    # 🔴 AGREGAR COLUMNAS DE BORDE CONDICIONAL PARA EL TOP 5 EN LA INTERFAZ ALTAIR
    counts['StrokeColor'] = '#000000'
    counts.loc[0:4, 'StrokeColor'] = '#FF0000'
    counts['StrokeWidth'] = 1.0
    counts.loc[0:4, 'StrokeWidth'] = 2.2

    if not counts.empty:
        chart = alt.Chart(counts).mark_bar().encode(
            x=alt.X('Papers:Q', title='Papers'),
            y=alt.Y('Institución:N', sort='-x', title=None),
            color=alt.Color('Color:N', scale=None),
            opacity=alt.Opacity('Opacity:Q', scale=None),
            stroke=alt.Color('StrokeColor:N', scale=None),
            strokeWidth=alt.Size('StrokeWidth:Q', scale=None),
            tooltip=['Institución', 'Papers']
        ).properties(
            width='container',
            height=350
        )
        st.altair_chart(chart, use_container_width=True)
    else:
        st.info("Sin suficientes datos.")
