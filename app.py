import streamlit as st
from pages.Ecosystem_Setup import set_layout

# 1. Configure the screen layout globally
set_layout()

# 2. Define the pages with clean English titles
pagina_home = st.Page("pages/Inicio.py", title="Home Overview", icon="🇲🇽", default=True)
pagina_grafo = st.Page("pages/Network.py", title="Institutional AI Network", icon="🕸️")

# 3. Create the navigation instance
nav = st.navigation([pagina_home, pagina_grafo])

# 4. Inject the Title into the sidebar container BEFORE running the pages render
with st.sidebar:
    st.markdown("## 🧭 Navigation Panel")
    st.markdown("---")

# 5. Run the navigation system
nav.run()
