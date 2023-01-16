from .distances import merged_distances
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc


def diamond(gallery, notation, distance, notation2, distance2, from_slug, to_slug):

    merged = merged_distances(gallery, notation, distance, notation2, distance2)

    x = distance + "_" + notation
    y = distance2 + "_" + notation2

    merged = merged.groupby("from_slug").mean([x, y]).reset_index()
    merged["selected"] = (merged["from_slug"] == from_slug) | (
        merged["from_slug"] == to_slug
    )

    mn = 0  # min(merged[x].min(), merged[y].min())
    mx = max(merged[x].max(), merged[y].max())
    s = 0.1 * (mx - mn)
    mx += s
    # mn -= s
    md = (mn + mx) / 2
    md = round(md)
    mx = round(mx)
    mn = round(mn)

    fig = go.Figure(
        [
            go.Scattercarpet(
                mode="markers",
                a=merged[x],
                b=merged[y],
                customdata=merged["from_slug"],
                hoverinfo="none",
                hovertemplate="<extra></extra>",
            ),
            go.Carpet(
                a=[mn, md, mx, mn, md, mx, mn, md, mx],
                b=[mn, mn, mn, md, md, md, mx, mx, mx],
                x=[0, -5, -10, 5, 0, -5, 10, 5, 0],
                y=[0, 5, 10, 5, 10, 15, 10, 15, 20],
                aaxis=dict(
                    title=f"{notation} {distance} farness",
                    gridcolor="lightgrey",
                ),
                baxis=dict(
                    title=f"{notation2} {distance2} farness",
                    gridcolor="lightgrey",
                ),
            ),
        ]
    )
    if from_slug != "":
        fig.add_scattercarpet(
            mode="markers",
            a=merged.query("selected")[x],
            b=merged.query("selected")[y],
            customdata=merged.query("selected")["from_slug"],
            marker_color="red",
            marker_size=10,
            hoverinfo="none",
            hovertemplate="<extra></extra>",
        )
    fig.add_shape(line_color="lightgrey", line_width=1, x0=0, x1=0, y0=0.1, y1=19.9)
    fig.update_xaxes(visible=False, range=[-11, 11])
    fig.update_yaxes(visible=False, range=[-1, 21])
    fig.update_layout(
        plot_bgcolor="white",
        margin=dict(b=0, t=0, l=0, r=0),
        width=500,
        height=500,
        showlegend=False,
    )

    return fig


def farness_scatter(
    gallery, notation, distance, notation2, distance2, from_slug, to_slug
):

    merged = merged_distances(gallery, notation, distance, notation2, distance2)

    x = distance
    y = distance2

    merged = merged.groupby("from_slug").mean([x, y]).reset_index()
    merged["selected"] = (merged["from_slug"] == from_slug) | (
        merged["from_slug"] == to_slug
    )

    fig = px.scatter(
        merged,
        x=x,
        y=y,
        color="selected",
        hover_data=["from_slug"],
        category_orders={"selected": [False, True]},
        width=500,
        height=500,
        labels={x: x + " farness", y: y + " farness"},
    )
    fig.update_traces(hoverinfo="none", hovertemplate="<extra></extra>")
    fig.update_layout(
        showlegend=False, xaxis_rangemode="tozero", yaxis_rangemode="tozero"
    )
    if len(fig.data) > 1:
        fig.data[1].marker.size = 10
    return fig


distance_pair_vis_map = {
    "farness_scatter": farness_scatter,
}
distance_pair_vis_types = list(distance_pair_vis_map.keys())

notation_pair_vis_map = {
    "diamond": diamond,
}
notation_pair_vis_types = list(notation_pair_vis_map.keys())


def wrap_pair_vis(
    gallery, notation, distance, notation2, distance2, vis, from_slug, to_slug
):
    fig = dict(**distance_pair_vis_map, **notation_pair_vis_map)[vis](
        gallery, notation, distance, notation2, distance2, from_slug, to_slug
    )
    return dcc.Graph(
        id=dict(type="figure", suffix="pair", seq="1", notation=notation),
        figure=fig,
        style=dict(width="500px", margin="0 auto"),
        clear_on_unhover=True,
    )
