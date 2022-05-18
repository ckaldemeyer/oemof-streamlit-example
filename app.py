import datetime
import data_handling as dh
import plotting as pt
import numpy as np
import streamlit as st
import models as md
from PIL import Image


def run_app():

    st.set_page_config(
        layout="wide",
        page_title="Streamlit meets oemof",
        initial_sidebar_state="auto",
    )

    image = Image.open(".streamlit/logo_oemof.png")
    st.sidebar.image(image, width=250, caption="Streamlit meets oemof")

    st.sidebar.text("")
    st.sidebar.text("")

    ex0 = st.sidebar.expander("Time horizon", expanded=True)
    date_start = ex0.date_input("Start", datetime.date(2021, 1, 1))
    date_end = ex0.date_input("Endd", datetime.date(2021, 1, 7))

    ex1 = st.sidebar.expander("Plant parameters", expanded=False)
    bss_capacity = ex1.slider("BSS capacity", 0, 50000, 10000, 1000)
    bss_in = ex1.slider("Capacity (in)", 0, 10000, 1000, 100)
    bss_out = ex1.slider("Capacity (out)", 0, 10000, 1000, 100)
    bss_loss_rate = ex1.slider("Loss rate", 0.0, 1.0, 0.01)
    bss_eta_in = ex1.slider("Efficiency in", 0.0, 1.0, 0.99)
    bss_eta_out = ex1.slider("Efficiency out", 0.0, 1.0, 0.99)

    ex2 = st.sidebar.expander("Grid", expanded=False)
    grid_max_power_consumption = ex2.slider(
        "Max. capacity from grid", 0, 100000, 0, 100
    )
    grid_max_power_feedin = ex2.slider(
        "Max. capacity grid feedin", 0, 100000, 10000, 100
    )

    df = dh.read_data()
    df = df.loc[date_start:date_end, :]

    result = md.run_storage(
        df,
        bss_capacity=bss_capacity,
        bss_in=bss_in,
        bss_out=bss_out,
        bss_loss_rate=bss_loss_rate,
        bss_eta_in=bss_eta_in,
        bss_eta_out=bss_eta_out,
        grid_max_power_consumption=grid_max_power_consumption,
        grid_max_power_feedin=grid_max_power_feedin,
    )

    ex2 = st.sidebar.expander("Download data", expanded=False)
    ex2.download_button(
        label="Export results to CSV",
        data=dh.convert_df(result),
        file_name="results.csv",
        mime="text/csv",
    )

    production = result.loc[:, "Wind"]
    production_mwh = production / 1000
    production = production_mwh.sum()

    bss_in = result.loc[:, "BSS (in)"].sum() / 1000
    bss_out = result.loc[:, "BSS (out)"].sum() / 1000

    feedin = result.loc[:, "Feedin"]
    feedin_mwh = feedin / 1000
    feedin = feedin_mwh.sum()

    consumption = result.loc[:, "Consumption"]
    consumption_mwh = consumption / 1000
    consumption = consumption_mwh.sum()

    pv_capacity = max(production_mwh)
    vls = production / pv_capacity

    (
        col0,
        col1,
        col2,
        col3,
        col4,
        col5,
        col6,
    ) = st.columns(7)

    with col0:
        st.metric(
            "Max. production",
            str(np.round(pv_capacity, 2)),
            "MW",
        )
    with col1:
        st.metric("Production wind", str(np.round(production, 2)), "MWh")
    with col2:
        st.metric("Full load hours", str(np.round(vls, 2)), "h")
    with col3:
        st.metric("Feedin", str(np.round(feedin, 2)), "MWh")
    with col4:
        st.metric("Consumption", str(np.round(consumption, 2)), "MWh")
    with col5:
        st.metric("BSS (in)", str(np.round(bss_in, 2)), "MWh")
    with col6:
        st.metric("BSS (ou)", str(np.round(bss_out, 2)), "MWh")

    with st.expander("Electricity price", expanded=True):
        chart = pt.line_plot(
            result,
            y="Electricity price (EUR/MWh)",
            legend=False,
        )
        st.plotly_chart(chart, use_container_width=True)

    with st.expander("BSS (power)", expanded=True):
        chart = pt.area_plot(
            result,
            y=[
                "BSS (power)",
            ],
            legend=False,
        )
        st.plotly_chart(chart, use_container_width=True)

    with st.expander("BSS (energy)", expanded=True):
        chart = pt.area_plot(
            result,
            y=[
                "BSS (energy)",
            ],
            legend=False,
        )
        st.plotly_chart(chart, use_container_width=True)

    with st.expander("Production Wind", expanded=True):
        chart = pt.line_plot(
            result,
            y=[
                "Wind",
            ],
            legend=False,
        )
        st.plotly_chart(chart, use_container_width=True)

    with st.expander("Feedin Grid", expanded=True):
        chart = pt.line_plot(
            result,
            y=[
                "Feedin",
            ],
            legend=False,
        )
        st.plotly_chart(chart, use_container_width=True)

    with st.expander("Consumption", expanded=False):
        chart = pt.line_plot(
            result,
            y=[
                "Consumption",
            ],
            legend=False,
        )
        st.plotly_chart(chart, use_container_width=True)


if __name__ == "__main__":
    run_app()
