from typing import Optional, Any

import plotly.graph_objects as go
from plotly.subplots import make_subplots
import ipywidgets as widgets

layout = widgets.Layout(width="auto", height="40px")


def table_with_filter(df: Any, title: Optional[str] = None):
    df = df.reset_index().round(3)
    fig = go.Figure(go.Table(header={"values": df.columns}, cells={"values": df.T.values}), layout=dict(title=title))
    fig.update_layout(
        updatemenus=[
            {
                "buttons": [
                    {
                        "label": c,
                        "method": "update",
                        "args": [
                            {"cells": {"values": df.T.values if c == "All" else df.loc[df["Type"].eq(c)].T.values}}
                        ],
                    }
                    for c in ["All"] + df["Type"].unique().tolist()
                ]
            }
        ],
        margin=dict(l=10, r=10, b=10, t=50),
    )
    fig.show()


def tables_show(dfs: list, titles: Optional[list] = None):
    if len(dfs) == 1:
        df = dfs[0].reset_index().round(3)
        fig = go.Figure(
            go.Table(header={"values": df.columns}, cells={"values": df.T.values}), layout=dict(title=titles[0])
        )
    else:
        fig = make_subplots(
            rows=1,
            cols=2,
            specs=[[{"type": "table"}, {"type": "table"}]],
            subplot_titles=titles,
        )

        for col, df in enumerate(dfs, start=1):
            df = df.reset_index().round(3)
            fig.add_trace(
                go.Table(header={"values": df.columns}, cells={"values": df.T.values}),
                row=1,
                col=col,
            )
    fig.update_layout(margin=dict(l=10, r=10, b=10, t=50))
    fig.show()


def range_slider(title: str):
    return widgets.IntRangeSlider(
        value=[-25, 10],
        min=-100,
        max=100,
        step=5,
        description=title,
        continuous_update=False,
        disabled=False,
        layout=layout,
        style={"description_width": "200px"},
    )
