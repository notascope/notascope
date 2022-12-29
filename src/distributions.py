import plotly.express as px
from .tokens import load_tokens
from .distances import dmat_and_order
import pandas as pd
import numpy as np


def token_bars(study, notation):
    tokens_df = load_tokens()

    df = tokens_df.query(f"study == '{study}' and notation== '{notation}'").groupby(["token", "notation"])["slug"].nunique().reset_index()
    df["y"] = 1
    fig = px.bar(df, x="slug", y="y", hover_name="token", height=600, hover_data=dict(y=False), labels=dict(slug="token frequency", y="token count"))
    return fig


def token_rank(study, notation):

    tokens_df = load_tokens()

    df = tokens_df.query(f"study == '{study}' and notation== '{notation}'").groupby(["token", "notation"])["slug"].nunique().reset_index()
    fig = px.ecdf(df, x="slug", hover_name="token", ecdfnorm=None, height=600, markers=True, lines=False, ecdfmode="complementary")
    fig.data[0].y += 1
    fig.layout.xaxis.title.text = "token frequency"
    fig.layout.yaxis.title.text = "token frequency rank"
    return fig


def farness(study, notation, distance):

    dmat, dmat_sym, order = dmat_and_order(study, notation, distance)

    df = pd.DataFrame(dict(slug=order, farness=np.mean(dmat, axis=1)))

    df["bin_centres"] = pd.cut(df["farness"], bins=50).apply(lambda x: float(x.mid)).astype(float)

    return px.bar(
        df,
        x="bin_centres",
        y=px.Constant(1),
        hover_data=["slug"],
        color="farness",
        range_color=[df["bin_centres"].min(), df["bin_centres"].median() * 2],
        height=600,
    ).update_traces(hoverinfo="none", hovertemplate="<extra></extra>")
