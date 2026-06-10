import pandas as pd
import streamlit as st

DATA_PATH = "data/metadata_extraida.csv"

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)

    df.sort_values(by="image_file", inplace=True)
    df.reset_index(drop=True, inplace=True)

    return df
