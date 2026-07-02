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
