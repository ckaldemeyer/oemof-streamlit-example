import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


def line_plot(
    df,
    x="dt_start_utc",
    y=None,
    labels=None,
    line_colors=None,
    paper_bgcolor="rgba(0, 0, 0, 0)",
    plot_bgcolor="rgba(0, 0, 0, 0)",
    legend=True,
):

    if labels is None:
        labels = {
            "dt_start_utc": "Datum",
            "value": "kWh",
            "variable": "Variable",
        }

    if line_colors is None:
        line_colors = [
            "#1c547c",
            "#AFAFAF",
        ]

    chart = px.line(
        df,
        y=y,
        labels=labels,
        template="plotly_dark",
        color_discrete_sequence=line_colors,
    )
    chart.update_layout(
        showlegend=legend,
        paper_bgcolor=paper_bgcolor,
        plot_bgcolor=plot_bgcolor,
    )

    return chart


def scatter_plot(
    df,
    x=None,
    y=None,
    labels=None,
    line_colors=None,
    paper_bgcolor="rgba(0, 0, 0, 0)",
    plot_bgcolor="rgba(0, 0, 0, 0)",
    legend=True,
):
    if labels is None:
        labels = {
            "dt_start_utc": "Datum",
            "value": "kWh",
            "variable": "Variable",
        }

    if line_colors is None:
        line_colors = [
            "#1c547c",
            "#AFAFAF",
        ]

    chart = px.scatter(
        df,
        x=x,
        y=y,
        labels=labels,
        template="plotly_dark",
        color_discrete_sequence=line_colors,
    )
    chart.update_layout(
        showlegend=legend,
        paper_bgcolor=paper_bgcolor,
        plot_bgcolor=plot_bgcolor,
    )

    return chart


def area_plot(
    df,
    x=None,
    y=None,
    labels=None,
    line_colors=None,
    paper_bgcolor="rgba(0, 0, 0, 0)",
    plot_bgcolor="rgba(0, 0, 0, 0)",
    template="plotly_dark",
    legend=True,
):
    if labels is None:
        labels = {
            "dt_start_utc": "Datum",
            "value": "kWh",
            "variable": "Variable",
        }

    if line_colors is None:
        line_colors = [
            "#1c547c",
            "#AFAFAF",
        ]

    chart = px.area(
        df,
        x=x,
        y=y,
        labels=labels,
        template=template,
        color_discrete_sequence=line_colors,
    )
    chart.update_layout(
        showlegend=legend,
        paper_bgcolor=paper_bgcolor,
        plot_bgcolor=plot_bgcolor,
    )

    return chart
