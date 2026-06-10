import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="Mexican AI Ecosystem",
    page_icon="🇲🇽",
    layout="wide"
)

# Portada / Título principal
st.title("🇲🇽 Evolution of the Mexican AI Ecosystem")
st.markdown("---")

# Explicación del funcionamiento de la App
st.markdown("""
## 🧠 Acerca del Proyecto
Esta aplicación interactiva explora la evolución del ecosistema de investigación en **Inteligencia Artificial en México** utilizando técnicas de análisis de redes y bibliometría. 

El análisis se basa en los datos de las memorias de congresos como **MICAI**, permitiendo mapear cómo las instituciones, investigadores y colaboraciones han cambiado a lo largo del tiempo.

### 📊 ¿Cómo funciona esta aplicación?
En el menú de la izquierda encontrarás las diferentes secciones de análisis que se vayan desarrollando. Cada página te permitirá interactuar con los datos mediante filtros dinámicos (como años o áreas de investigación).

El ecosistema se analiza a través de **cuatro eras analíticas**:
* **Era 1: The Islands** (1997–2008)
* **Era 2: The Bridges** (2009–2019)
* **Era 3: Forced Virtualization** (2020–2022)
* **Era 4: Solid Networks** (2023–2026)
""")

# Cuadro informativo del autor (usando los datos de tu README)
st.sidebar.info("""
**Autor:** Edgar Avalos Gauna  
*Rice University* Investigación en sistemas de IA, ciencia de datos y redes complejas aplicadas a ecosistemas científicos.
""")

# Validamos que los datos se lean correctamente para dejar el cimiento listo
st.subheader("📁 Estado de los Datos")
try:
    df = pd.read_csv("data/data.csv")
    st.success(f"¡Datos cargados exitosamente! El dataset actual cuenta con {df.shape[0]} registros listos para ser analizados.")
except Exception as e:
    st.error(f"No se pudo encontrar el archivo de datos en 'data/data.csv'. Asegúrate de haber guardado tu archivo ahí.")
