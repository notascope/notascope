import json
import plotly.graph_objects as go
from functools import cache
import plotly.express as px
import numpy as np
from .distances import dmat_and_order, get_embedding


def get_scatter(gallery, notation, distance, from_spec, to_spec, method):
    fig_json, fig_df = build_scatter(gallery, notation, distance, method)
    fig = go.Figure(json.loads(fig_json))

    dmat, dmat_sym, order = dmat_and_order(gallery, notation, distance)
    if from_spec:
        from_row = fig_df.loc[from_spec]
        to_row = fig_df.loc[to_spec]
        fig.add_scatter(
            x=[from_row.x, to_row.x],
            y=[from_row.y, to_row.y],
            hoverinfo="skip",
            showlegend=False,
        )
        if from_spec == to_spec:
            fig.data[0].marker = dict(
                color=dmat_sym[order.index(from_spec)],
                cmax=np.median(dmat_sym),
                colorscale="Viridis",
            )
    else:
        fig.data[0].marker = dict(color=np.median(dmat_sym, axis=0))

    return fig


@cache
def build_scatter(gallery, notation, distance, method):
    emb_df = get_embedding(gallery, notation, distance, method)
    fig = px.scatter(emb_df, x="x", y="y", hover_data=dict(spec=emb_df.index))
    fig.update_layout(height=800, dragmode="pan", plot_bgcolor="white")
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), uirevision="yes")
    fig.update_yaxes(visible=False)
    fig.update_xaxes(visible=False)
    fig.update_traces(hoverinfo="none", hovertemplate=None)

    return fig.to_json(), emb_df
