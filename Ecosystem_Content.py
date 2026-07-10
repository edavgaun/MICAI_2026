APP_TITLE = "🕸️ Mexican AI Core-Periphery Network"
APP_SUBTITLE = "Análisis estructural y longitudinal del ecosistema de IA en México (2000–2025)."
BAR_CHART_TITLE = "### 📊 Top 10 Volumen e Impacto Estructural"
EMPTY_DATA_WARNING = "No se encontraron datos para la combinación o año seleccionado."

def obtener_info_era(year):
    """Devuelve el nombre de la era basado en los hitos e inflexiones del paper."""
    if year <= 2007:
        return "Era 1: Formación y Expansión Inicial (2000–2007)"
    elif year <= 2012:
        return "Era 2: Choques Externos y Consolidación del Núcleo (2008–2012)"
    elif year <= 2022:
        return "Era 3: Crecimiento Asimétrico y Alta Transitividad (2013–2022)"
    else:
        return "Era 4: Frontera Generativa y Retos de Cohesión (2023–2025)"

# Ajuste de la sección Home al marco científico del paper
HOME_TITLE = "🇲🇽 Core-Periphery Structure of Mexican AI Research Institutions"
HOME_INTRO = """
Bienvenido a la plataforma interactiva del ecosistema de Inteligencia Artificial en México. 
Explora cómo la acumulación de lazos científicos revela una estructura de núcleo denso (IPN, ITESM, CINVESTAV, UNAM, TecNM, INAOE) 
frente a una periferia fragmentada, evaluada rigurosamente mediante modelos nulos de preservación de grado.
"""

LEGEND_HTML = """
<div style="background-color: #f8f9fa; padding: 20px; border-radius: 10px; border: 1px solid #e0e0e0; margin-bottom: 20px; font-family: sans-serif;">
    <h4 style="margin-top: 0; color: #333; border-bottom: 2px solid #2ca02c; padding-bottom: 5px;">📍 Guía de la Red</h4>
    <div style="margin-bottom: 15px;">
        <p style="font-size: 0.9rem; font-weight: bold; margin-bottom: 8px;">Instituciones (Nodos):</p>
        <div style="display: flex; align-items: center; margin-bottom: 5px;">
            <div style="width: 15px; height: 15px; background-color: #2ca02c; border-radius: 50%; margin-right: 10px; border: 1px solid #000;"></div>
            <span style="font-size: 0.85rem;">México (Núcleo o Periferia)</span>
        </div>
        <div style="display: flex; align-items: center; margin-bottom: 5px;">
            <div style="width: 15px; height: 15px; background-color: #EBF6FF; border-radius: 50%; margin-right: 10px; border: 1px solid #000;"></div>
            <span style="font-size: 0.85rem;">Extranjero</span>
        </div>
        <p style="font-size: 0.75rem; color: #666; font-style: italic;">* El tamaño del nodo representa su volumen de publicaciones en el corpus.</p>
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
