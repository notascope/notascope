import plotly.express as px
from .tokens import load_tokens
from .distances import dmat_and_order, distances_df
import numpy as np


def token_bars(gallery, notation, distance, from_spec, to_spec, vis):
    tokens_df = load_tokens()

    df = (
        tokens_df.query(f"gallery == '{gallery}' and notation== '{notation}'")
        .groupby(["token", "notation"])["spec"]
        .nunique()
        .reset_index()
    )
    df["y"] = 1
    fig = px.bar(
        df,
        x="spec",
        y="y",
        hover_name="token",
        height=600,
        hover_data=dict(y=False),
        labels=dict(spec="token frequency", y="token count"),
    )
    return fig


def token_rank(gallery, notation, distance, from_spec, to_spec, vis):

    tokens_df = load_tokens()

    df = (
        tokens_df.query(f"gallery == '{gallery}' and notation== '{notation}'")
        .groupby(["token", "notation"])["spec"]
        .nunique()
        .reset_index()
    )
    fig = px.ecdf(
        df,
        x="spec",
        hover_name="token",
        ecdfnorm=None,
        height=600,
        markers=True,
        lines=False,
        ecdfmode="complementary",
        labels=dict(spec="token frequency"),
    )
    fig.data[0].y += 1
    fig.update_yaxes(title_text="token frequency rank")
    return fig


def remoteness(gallery, notation, distance, from_spec, to_spec, vis):
    df = (
        distances_df(gallery=gallery, notation=notation)
        .groupby(["from_spec"])[distance]
        .median()
        .reset_index()
    )
    selected_ids = [from_spec, to_spec]  # noqa

    fig = (
        px.violin(
            df,
            x=distance,
            height=600,
            points="all",
            hover_data=["from_spec"],
            labels={distance: f"Specification Remoteness ({distance})"},
            title="Specification Remoteness Distribution",
        )
        .update_traces(
            hoveron="points",
            pointpos=0,
            scalemode="count",
            hoverinfo="none",
            hovertemplate="",
            spanmode="hard",
            line_width=0,
            meanline_visible=True,
            meanline_width=2,
            selectedpoints=df.query("from_spec in @selected_ids").index,
            selected_marker_color="red",
        )
        .update_layout(violingroupgap=0, violingap=0.05)
    )
    fig.update_yaxes(title="")
    fig.update_xaxes(rangemode="tozero")
    return fig


def get_remoteness_scatter(gallery, notation, distance, from_spec, to_spec, method):

    dmat, dmat_sym, order = dmat_and_order(gallery, notation, distance)
    x = y = color = np.median(dmat_sym, axis=1)
    xlab = ylab = "remoteness"
    range = None
    if from_spec:
        y = dmat_sym[order.index(from_spec)]
        ylab = "distance to " + from_spec
    if to_spec != from_spec:
        x = dmat_sym[order.index(to_spec)]
        xlab = "distance to " + to_spec
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
    fig.update_yaxes(rangemode="tozero")
    fig.update_xaxes(rangemode="tozero")
    return fig
