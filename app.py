import streamlit as st
from pages.Ecosystem_Setup import set_layout

# 1. Configuramos el layout antes de cualquier otra cosa
set_layout()

# 2. Definimos las páginas apuntando a sus respectivos archivos
pagina_home = st.Page("pages/Inicio.py", title="Inicio", icon="🇲🇽", default=True)
pagina_grafo = st.Page("pages/Network.py", title="Red Institucional de IA", icon="🕸️")

# 3. Arrancamos el navegador
nav = st.navigation([pagina_home, pagina_grafo])
nav.run()
