import streamlit as st
from pages.Ecosystem_Setup import set_layout, show_header, show_main_instructions, load_clean_data

# 1. Definimos explícitamente qué archivos se muestran y con qué etiquetas
pagina_home = st.Page("app.py", title="Inicio", icon="🇲🇽", default=True)
pagina_grafo = st.Page("pages/Network.py", title="Red Institucional de IA", icon="🕸️")

# 2. Registramos solo estas dos páginas en el navegador de la barra lateral
# Cualquier otro archivo que esté en la carpeta pages/ quedará completamente oculto
nav = st.navigation([pagina_home, pagina_grafo])

# 3. Inicializamos el layout estructural
set_layout()

# 4. Renderizamos la página que el usuario tenga seleccionada
nav.run()

# 5. Si el usuario está parado en el Inicio, mostramos tu contenido base
if nav.current_page == pagina_home:
    show_header("🇲🇽 Evolution of the Mexican AI Ecosystem")
    show_main_instructions()
    
    # Carga limpia de datos
    df = load_clean_data()
    st.sidebar.success(f"📈 Dataset listo: {df.shape[0]} registros.")
