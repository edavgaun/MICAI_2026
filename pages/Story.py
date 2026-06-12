import streamlit as st

from pages.Ecosystem_Setup import (
    show_header,
    load_clean_data,
)

show_header("📖 Story of Mexican AI")

df = load_clean_data()

# =====================================================
# STORY STATES
# =====================================================

STORY = [
    {
        "title": "🌱 Birth of the Ecosystem",
        "years": (1997, 2000),
        "text": """
        The Mexican AI ecosystem was still in its infancy.
        A small number of institutions dominated the landscape,
        and collaboration was limited.
        """
    },
    {
        "title": "🏝️ The Islands",
        "years": (1997, 2008),
        "text": """
        Research groups operated mostly as isolated islands.
        Connections existed, but communities remained fragmented.
        """
    },
    {
        "title": "🌉 The Bridges",
        "years": (2009, 2019),
        "text": """
        New institutional bridges emerged.
        Previously disconnected communities began collaborating.
        """
    },
    {
        "title": "🌎 International Expansion",
        "years": (2014, 2019),
        "text": """
        International collaboration accelerated and the ecosystem
        became increasingly connected to the global AI community.
        """
    },
    {
        "title": "💻 Forced Virtualization",
        "years": (2020, 2022),
        "text": """
        The pandemic transformed academic collaboration patterns
        and accelerated virtual interaction.
        """
    },
    {
        "title": "🕸️ Solid Networks",
        "years": (2023, 2026),
        "text": """
        The ecosystem reached its highest level of connectivity,
        diversity and institutional participation.
        """
    }
]

# =====================================================
# STORY CONTROLLER
# =====================================================

step = st.select_slider(
    "",
    options=range(len(STORY)),
    format_func=lambda x: STORY[x]["title"]
)

story = STORY[step]

year_min, year_max = story["years"]

df_story = df[
    (df["year"] >= year_min) &
    (df["year"] <= year_max)
]

# =====================================================
# HERO SECTION
# =====================================================

st.markdown(f"# {story['title']}")

st.markdown(story["text"])

st.markdown("---")

# =====================================================
# KPIs
# =====================================================

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Institutions",
    df_story["institution_clean"].nunique()
)

c2.metric(
    "Authors",
    df_story["author"].nunique()
)

c3.metric(
    "Countries",
    df_story["country"].nunique()
)

c4.metric(
    "Papers",
    df_story["title"].nunique()
)

st.markdown("---")

# =====================================================
# PLACEHOLDER FOR NETWORK
# =====================================================

network_placeholder = st.container()

with network_placeholder:

    st.info(
        f"Network visualization for {year_min}-{year_max} will appear here."
    )

# =====================================================
# DID YOU KNOW
# =====================================================

st.markdown("### 🔍 Did You Know?")

st.success(
    "Dynamic insights will appear here based on the selected story stage."
)
