import streamlit as st
from pages.Ecosystem_Setup import set_layout

set_layout()

pagina_home = st.Page("pages/Inicio.py", title="Home Overview", icon="🇲🇽", default=True)
pagina_grafo = st.Page("pages/Network.py", title="Institutional AI Network", icon="🕸️")

def draw_custom_sidebar(pages):
    st.sidebar.markdown("## 🗺️ Navigation Panel")
    st.sidebar.markdown("---")

    for page in pages:
        st.sidebar.page_link(page, label=page.title, icon=page.icon)

nav = st.navigation(
    [pagina_home, pagina_grafo],
    position="hidden"
)

draw_custom_sidebar(
    [pagina_home, pagina_grafo]
)

nav.run()
