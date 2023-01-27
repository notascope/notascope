import plotly.express as px
from .tokens import load_tokens
from .distances import dmat_and_order
import pandas as pd
import numpy as np


def token_bars(gallery, notation, distance, from_slug, to_slug, vis):
    tokens_df = load_tokens()

    df = (
        tokens_df.query(f"gallery == '{gallery}' and notation== '{notation}'")
        .groupby(["token", "notation"])["slug"]
        .nunique()
        .reset_index()
    )
    df["y"] = 1
    fig = px.bar(
        df,
        x="slug",
        y="y",
        hover_name="token",
        height=600,
        hover_data=dict(y=False),
        labels=dict(slug="token frequency", y="token count"),
    )
    return fig


def token_rank(gallery, notation, distance, from_slug, to_slug, vis):

    tokens_df = load_tokens()

    df = (
        tokens_df.query(f"gallery == '{gallery}' and notation== '{notation}'")
        .groupby(["token", "notation"])["slug"]
        .nunique()
        .reset_index()
    )
    fig = px.ecdf(
        df,
        x="slug",
        hover_name="token",
        ecdfnorm=None,
        height=600,
        markers=True,
        lines=False,
        ecdfmode="complementary",
        labels=dict(slug="token frequency"),
    )
    fig.data[0].y += 1
    fig.update_yaxes(title_text="token frequency rank")
    return fig


def farness(gallery, notation, distance, from_slug, to_slug, vis):

    dmat, dmat_sym, order = dmat_and_order(gallery, notation, distance)

    df = pd.DataFrame(dict(slug=order, farness=np.median(dmat_sym, axis=1)))

    df["bin_center"] = (
        pd.cut(df["farness"], bins=50).apply(lambda x: float(x.mid)).astype(float)
    )
    df["y"] = 1
    fig = px.bar(
        df,
        x="bin_center",
        y="y",
        color="bin_center",
        hover_data=["slug"],
        labels=dict(bin_center="farness"),
        range_color=[df["bin_center"].min(), df["bin_center"].median() * 2],
        height=600,
    )
    for s in [from_slug, to_slug]:
        if s:
            fig.add_vline(df["farness"][order.index(s)], line_color="red")
    fig.update_traces(hoverinfo="none", hovertemplate="<extra></extra>")
    fig.update_xaxes(title_text="farness (binned)")
    fig.update_yaxes(title_text="count")
    return fig


def get_farness_scatter(gallery, notation, distance, from_slug, to_slug, method):

    dmat, dmat_sym, order = dmat_and_order(gallery, notation, distance)
    x = y = color = np.median(dmat_sym, axis=1)
    xlab = ylab = "farness"
    range = None
    if from_slug:
        y = dmat_sym[order.index(from_slug)]
        ylab = "distance to " + from_slug
    if to_slug != from_slug:
        x = dmat_sym[order.index(to_slug)]
        xlab = "distance to " + to_slug
        range = [0, 1.05 * max(np.max(x), np.max(y))]
    fig = px.scatter(
        x=x,
        y=y,
        hover_data=[order],
        labels=dict(x=xlab, y=ylab),
        color=color,
        height=700,
        width=700,
        range_x=range,
        range_y=range,
    )
    fig.update_coloraxes(showscale=False)
    fig.update_traces(hoverinfo="none", hovertemplate="<extra></extra>")
    return fig
