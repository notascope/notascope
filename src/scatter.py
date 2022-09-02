import json
import plotly.graph_objects as go
from functools import cache
import plotly.express as px
import numpy as np
from .distances import dmat_and_order, get_embedding


def get_scatter(study, notation, distance, from_slug, to_slug, method):
    fig_json, fig_df = build_scatter(study, notation, distance, method)
    fig = go.Figure(json.loads(fig_json))

    dmat, dmat_sym, order = dmat_and_order(study, notation, distance)
    if from_slug:
        from_row = fig_df.loc[from_slug]
        to_row = fig_df.loc[to_slug]
        fig.add_scatter(x=[from_row.x, to_row.x], y=[from_row.y, to_row.y], hoverinfo="skip", showlegend=False)
        if from_slug == to_slug:
            fig.data[0].marker = dict(color=dmat_sym[order.index(from_slug)], cmax=np.median(dmat_sym), colorscale="Viridis")
    else:
        fig.data[0].marker = dict(color=np.median(dmat_sym, axis=0))

    return fig


@cache
def build_scatter(study, notation, distance, method):
    emb_df = get_embedding(study, notation, distance, method)
    fig = px.scatter(emb_df, x="x", y="y", hover_name=emb_df.index)
    fig.update_layout(height=800, dragmode="pan", plot_bgcolor="white")
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), uirevision="yes")
    fig.update_yaxes(visible=False)
    fig.update_xaxes(visible=False)
    fig.update_traces(hoverinfo="none", hovertemplate=None)

    return fig.to_json(), emb_df


def get_scatter3d(study, notation, distance, from_slug, to_slug, method):
    fig_json, fig_df = build_scatter3d(study, notation, distance, method)
    fig = go.Figure(json.loads(fig_json))

    dmat, dmat_sym, order = dmat_and_order(study, notation, distance)
    if from_slug:
        from_row = fig_df.loc[from_slug]
        to_row = fig_df.loc[to_slug]
        fig.add_scatter3d(x=[from_row.x, to_row.x], y=[from_row.y, to_row.y], z=[from_row.z, to_row.z], hoverinfo="skip", showlegend=False)
        if from_slug == to_slug:
            fig.data[0].marker = dict(color=dmat_sym[order.index(from_slug)], cmax=np.median(dmat_sym), colorscale="Viridis")
    else:
        fig.data[0].marker = dict(color=np.median(dmat_sym, axis=0))

    fig.update_traces(marker_size=4, line_width=2)
    return fig


@cache
def build_scatter3d(study, notation, distance, method):
    emb_df = get_embedding(study, notation, distance, method, dim=3)
    fig = px.scatter_3d(emb_df, x="x", y="y", z="z", hover_name=emb_df.index)
    fig.update_layout(height=800, dragmode="pan", plot_bgcolor="white")
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), uirevision="yes")
    fig.update_yaxes(visible=False)
    fig.update_xaxes(visible=False)
    fig.update_traces(hoverinfo="none", hovertemplate=None)

    return fig.to_json(), emb_df