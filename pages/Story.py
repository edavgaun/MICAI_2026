import streamlit as st

from pages.Ecosystem_Setup import (
    show_header,
    load_clean_data
)

show_header("📖 Story of Mexican AI")

df = load_clean_data()

st.markdown("""
# The Evolution of the Mexican AI Ecosystem

For nearly three decades, researchers, universities,
and research centers have collaborated to build the
Mexican Artificial Intelligence ecosystem.

This story explores how that network evolved from
isolated research groups into a nationally connected
and internationally visible community.
""")

st.markdown("---")

st.header("Chapter 1 — The Islands (1997–2008)")

st.write("""
During the early years, AI research in Mexico was
concentrated in a relatively small number of institutions.

Collaboration existed, but many groups operated
independently, creating isolated clusters of expertise.
""")

st.info("""
Key question:

How did a fragmented ecosystem become a connected community?
""")
