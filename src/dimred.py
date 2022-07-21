import json
import plotly.graph_objects as go
from functools import cache

from sklearn.manifold import TSNE
from umap import UMAP

import plotly.express as px
import numpy as np
import pandas as pd
from .distances import dmat_and_order


def get_dimred(study, notation, distance, from_slug, to_slug, method):
    fig_json, fig_df = build_dimred(study, notation, distance, method)
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
def build_dimred(study, notation, distance, method):
    dmat, dmat_sym, order = dmat_and_order(study, notation, distance)
    np.random.seed(123)
    if method == "tsne":
        dimred = TSNE(n_components=2, metric="precomputed", square_distances=True, learning_rate="auto", init="random")
    elif method == "umap":
        dimred = UMAP(n_components=2)
    embedding = dimred.fit_transform(dmat_sym)
    emb_df = pd.DataFrame(embedding, index=order, columns=["x", "y"])
    fig = px.scatter(emb_df, x="x", y="y", hover_name=order)
    fig.update_layout(height=800, dragmode="pan", plot_bgcolor="white")
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), uirevision="yes")
    fig.update_yaxes(visible=False)
    fig.update_xaxes(visible=False)
    fig.update_traces(hoverinfo="none", hovertemplate=None)

    return fig.to_json(), emb_df
