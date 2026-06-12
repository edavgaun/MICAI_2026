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

Scroll down to explore its transformation.
""")

st.markdown("---")

# ==========================================================
# CHAPTER 1
# ==========================================================

st.header("🏝️ Chapter 1 — The Islands (1997–2008)")

col1, col2 = st.columns([2,1])

with col1:
    st.write("""
    During the early years, AI research in Mexico was
    concentrated in a small number of institutions.

    Collaboration existed, but many groups remained
    disconnected from each other.

    The ecosystem resembled a collection of islands
    rather than a unified network.
    """)

with col2:
    st.metric("Institutions", "TBD")
    st.metric("Countries", "TBD")
    st.metric("Collaborations", "TBD")

st.markdown("---")

# ==========================================================
# CHAPTER 2
# ==========================================================

st.header("🌉 Chapter 2 — The Bridges (2009–2019)")

col1, col2 = st.columns([2,1])

with col1:
    st.write("""
    As the ecosystem matured, several institutions
    emerged as connectors between previously isolated
    communities.

    National and international collaborations increased,
    creating a denser research landscape.
    """)

with col2:
    st.metric("Institutions", "TBD")
    st.metric("Countries", "TBD")
    st.metric("Collaborations", "TBD")

st.markdown("---")

# ==========================================================
# CHAPTER 3
# ==========================================================

st.header("💻 Chapter 3 — Forced Virtualization (2020–2022)")

col1, col2 = st.columns([2,1])

with col1:
    st.write("""
    The COVID-19 pandemic disrupted traditional
    collaboration patterns but accelerated virtual
    interaction among researchers.

    The ecosystem adapted rapidly.
    """)

with col2:
    st.metric("Institutions", "TBD")
    st.metric("Countries", "TBD")
    st.metric("Collaborations", "TBD")

st.markdown("---")

# ==========================================================
# CHAPTER 4
# ==========================================================

st.header("🕸️ Chapter 4 — Solid Networks (2023–2026)")

col1, col2 = st.columns([2,1])

with col1:
    st.write("""
    By the most recent period, the Mexican AI ecosystem
    had evolved into a highly connected network with
    strong national and international participation.
    """)

with col2:
    st.metric("Institutions", "TBD")
    st.metric("Countries", "TBD")
    st.metric("Collaborations", "TBD")

st.markdown("---")

st.success("""
You have reached the present day.

Continue your exploration using the Institutional AI Network page.
""")
