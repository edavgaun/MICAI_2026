import pandas as pd
import os

DATA_PATH = "data/metadata_extraida.csv"

def load_data():
    df = pd.read_csv(DATA_PATH)
    df.sort_values(by="image_file", inplace=True)
    df.reset_index(drop=True, inplace=True)
    return df
