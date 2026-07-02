APP_TITLE = "🕸️ Collaboration Network Discovery"
APP_SUBTITLE = "Explora la evolución del ecosistema de IA en México año por año."
BAR_CHART_TITLE = "### 📊 Top 10 Volumen"
EMPTY_DATA_WARNING = "No se encontraron datos para la combinación seleccionada."

def obtener_info_era(year):
    """Devuelve el nombre de la era basado en el año seleccionado."""
    if year <= 2008:
        return "Era 1: The Islands (1997–2008)"
    elif year <= 2019:
        return "Era 2: The Bridges (2009–2019)"
    elif year <= 2022:
        return "Era 3: Forced Virtualization (2020–2022)"
    else:
        return "Era 4: Solid Networks (2023–2026)"

# El texto de Home se mantiene igual
HOME_TITLE = "🇲🇽 Mexico's AI Ecosystem Timeline"
HOME_INTRO = """
Bienvenido al mapa interactivo de investigación y colaboración de Inteligencia Artificial en México.
Utiliza la línea de tiempo para ver cómo la red crece y se conecta año con año.
"""


# ... (mantiene lo anterior)

LEGEND_HTML = """
<div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; border: 1px solid #e0e0e0; margin-bottom: 20px; font-family: sans-serif;">
    <h4 style="margin-top: 0; color: #333; border-bottom: 2px solid #2ca02c; padding-bottom: 5px;">📍 Guía de la Red</h4>
    <div style="margin-bottom: 15px;">
        <p style="font-size: 0.9rem; font-weight: bold; margin-bottom: 8px;">Instituciones (Nodos):</p>
        <div style="display: flex; align-items: center; margin-bottom: 5px;">
            <div style="width: 15px; height: 15px; background-color: #2ca02c; border-radius: 50%; margin-right: 10px; border: 1px solid #000;"></div>
            <span style="font-size: 0.85rem;">México</span>
        </div>
        <div style="display: flex; align-items: center; margin-bottom: 5px;">
            <div style="width: 15px; height: 15px; background-color: #EBF6FF; border-radius: 50%; margin-right: 10px; border: 1px solid #000;"></div>
            <span style="font-size: 0.85rem;">Extranjero</span>
        </div>
        <p style="font-size: 0.75rem; color: #666; font-style: italic;">* El tamaño representa el volumen de papers.</p>
    </div>
    <div>
        <p style="font-size: 0.9rem; font-weight: bold; margin-bottom: 8px;">Colaboraciones (Aristas):</p>
        <div style="display: flex; align-items: center; margin-bottom: 5px;">
            <div style="width: 25px; height: 3px; background-color: rgba(44, 160, 44, 0.6); margin-right: 10px;"></div>
            <span style="font-size: 0.85rem;">Nacional (Mx-Mx)</span>
        </div>
        <div style="display: flex; align-items: center; margin-bottom: 5px;">
            <div style="width: 25px; height: 3px; background-color: rgba(255, 127, 14, 0.6); margin-right: 10px;"></div>
            <span style="font-size: 0.85rem;">Internacional (Mx-Ext)</span>
        </div>
        <div style="display: flex; align-items: center; margin-bottom: 5px;">
            <div style="width: 25px; height: 3px; background-color: rgba(211, 211, 211, 0.4); margin-right: 10px;"></div>
            <span style="font-size: 0.85rem;">Global (Ext-Ext)</span>
        </div>
    </div>
</div>
"""
