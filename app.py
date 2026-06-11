import streamlit as st
from pages.Ecosystem_Setup import set_layout

# 1. Configure the screen layout globally
set_layout()

# 2. Define the pages
pagina_home = st.Page("pages/Inicio.py", title="Home Overview", icon="🇲🇽", default=True)
pagina_grafo = st.Page("pages/Network.py", title="Institutional AI Network", icon="🕸️")

# 3. Create a custom sidebar layout function
def draw_custom_sidebar(pages):
    """Forces our custom title to stay at the absolute top of the navigation links."""
    st.sidebar.markdown("## 🧭 Navigation Panel")
    st.sidebar.markdown("---")
    
    # This renders the standard list of page links natively right below our header
    for page in pages:
        st.sidebar.page_link(page, label=page.title, icon=page.icon)

# 4. Initialize navigation using our custom sidebar function
nav = st.navigation([pagina_home, pagina_grafo], position="hidden")

# 5. Manually render our custom layout and run the page content
draw_custom_sidebar([pagina_home, pagina_grafo])
nav.run()
