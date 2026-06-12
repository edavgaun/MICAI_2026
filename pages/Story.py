import streamlit as st

from pages.Ecosystem_Setup import (
    show_header,
    load_clean_data
)

# =====================================================
# PAGE SETUP
# =====================================================

show_header("📖 Story of Mexican AI")

df = load_clean_data()

# =====================================================
# CUSTOM CSS
# =====================================================

st.markdown("""
<style>

div[role="radiogroup"] {
    justify-content: center;
    gap: 0.5rem;
    margin-bottom: 1rem;
}

div[role="radiogroup"] label {
    border: 1px solid rgba(128,128,128,0.3);
    border-radius: 10px;
    padding: 0.5rem 1rem;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# STORY STATES
# =====================================================

STORY = [
    {
        "title": "🌱 Birth",
        "years": (1997, 2000),
        "text": """
The Mexican AI ecosystem was still in its infancy.
A small number of institutions dominated the landscape,
and collaboration was limited.
"""
    },

    {
        "title": "🏝️ Islands",
        "years": (1997, 2008),
        "text": """
Research groups operated mostly as isolated islands.
Connections existed, but communities remained fragmented.
"""
    },

    {
        "title": "🌉 Bridges",
        "years": (2009, 2019),
        "text": """
New institutional bridges emerged.
Previously disconnected communities began collaborating.
"""
    },

    {
        "title": "🌎 Expansion",
        "years": (2014, 2019),
        "text": """
International collaboration accelerated and the ecosystem
became increasingly connected to the global AI community.
"""
    },

    {
        "title": "💻 Virtualization",
        "years": (2020, 2022),
        "text": """
The pandemic transformed academic collaboration patterns
and accelerated virtual interaction.
"""
    },

    {
        "title": "🕸️ Networks",
        "years": (2023, 2026),
        "text": """
The ecosystem reached its highest level of connectivity,
diversity and institutional participation.
"""
    }
]

# =====================================================
# NARRATIVE CONTROLLER
# =====================================================

story_titles = [s["title"] for s in STORY]

selected_title = st.radio(
    "",
    story_titles,
    horizontal=True,
    label_visibility="collapsed"
)

story = next(
    item for item in STORY
    if item["title"] == selected_title
)

year_min, year_max = story["years"]

df_story = df[
    (df["year"] >= year_min) &
    (df["year"] <= year_max)
]

# =====================================================
# HERO SECTION
# =====================================================

hero = st.container(border=True)

with hero:

    st.markdown(f"# {story['title']}")

    st.markdown(story["text"])

# =====================================================
# KPI SECTION
# =====================================================

st.markdown("### Ecosystem Snapshot")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Institutions",
        df_story["institution_clean"].nunique()
    )

with c2:
    st.metric(
        "Authors",
        df_story["author"].nunique()
    )

with c3:
    st.metric(
        "Countries",
        df_story["country"].nunique()
    )

with c4:
    st.metric(
        "Papers",
        df_story["title"].nunique()
    )

# =====================================================
# NETWORK PLACEHOLDER
# =====================================================

st.markdown("---")
st.markdown("## Network Evolution")

st.info(
    f"Network visualization for {year_min}-{year_max} will appear here."
)

# =====================================================
# INSIGHT PLACEHOLDER
# =====================================================

st.markdown("---")
st.markdown("## Did You Know?")

st.success(
    "Narrative insights for the selected stage will appear here."
)
