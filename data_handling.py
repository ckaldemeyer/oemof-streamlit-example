import pandas as pd
import streamlit as st
from io import StringIO


@st.cache()
def read_data(file="data.csv", columns=None, rename=True):

    df = pd.read_csv(file, sep=";", decimal=",", index_col=0, parse_dates=True)

    if columns is None:
        columns = {
            "electricity_price_eur_mwh": "Electricity price (EUR/MWh)",
            "feedin_wind_kw": "Wind production (kWh)",
        }

    df = df.loc[:, list(columns.keys())]

    if rename:
        df = df.rename(columns=columns)

    return df


@st.cache
def convert_df(df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return df.to_csv(sep=";", decimal=",").encode("utf-8")
