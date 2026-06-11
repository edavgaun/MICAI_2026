import streamlit as st
from pages.Ecosystem_Setup import set_layout

# 1. Configure the screen layout globally before rendering anything else
set_layout()

# 2. Define the pages pointing to their respective files with clean English titles
pagina_home = st.Page("pages/Inicio.py", title="Home Overview", icon="🇲🇽", default=True)
pagina_grafo = st.Page("pages/Network.py", title="Institutional AI Network", icon="🕸️")

# 3. Boot and run the navigation sidebar suite
nav = st.navigation([pagina_home, pagina_grafo])
nav.run()
