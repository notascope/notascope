from .distances import merged_distances
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc
from .tokens import load_tokens


def tokens(gallery, notation, distance, notation2, distance2, from_slug, to_slug, vis):
    tokens_df = load_tokens()

    gallery = "movies"

    df = (
        tokens_df.query(
            f"gallery == '{gallery}' and notation in ('{notation}', '{notation2}')"
        )
        .groupby(["token", "notation"])["slug"]
        .nunique()
        .reset_index()
    )
    fig = px.ecdf(
        df,
        x="slug",
        color="notation",
        hover_name="token",
        ecdfnorm=None,
        height=600,
        markers=True,
        lines=True,
        # ecdfmode="complementary",
        labels=dict(slug="token frequency"),
    )
    fig.update_traces(line_shape="linear", marker_size=5, line_width=1)
    fig.update_yaxes(title_text="token frequency rank")
    fig.update_layout(scattermode="group")
    return fig


def diamond(gallery, notation, distance, notation2, distance2, from_slug, to_slug, vis):

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
    gallery, notation, distance, notation2, distance2, from_slug, to_slug, vis
):

    merged = merged_distances(gallery, notation, distance, notation2, distance2)

    x = merged.columns[2]
    y = merged.columns[3]

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


def slope(gallery, notation, distance, notation2, distance2, from_slug, to_slug, vis):
    df = merged_distances(gallery, notation, distance, notation2, distance2)
    if from_slug:
        df = df.query(f"from_slug == '{from_slug}'")
    df = df.groupby("to_slug").mean(numeric_only=True).reset_index()
    if "rank" in vis:
        for col in df.columns[1:]:
            df[col] = df[col].rank(method="first")
    df["none"] = None
    df["selected"] = df["to_slug"] == to_slug
    df = df.melt(
        id_vars=["to_slug", "selected"], var_name="pair", value_name="distance"
    ).sort_values(by=["to_slug", "distance"])
    df["pair"] = df["pair"].apply(lambda x: None if x == "none" else x)
    fig = px.line(
        df,
        x="distance",
        y="pair",
        color="selected",
        markers=True,
        hover_data=["to_slug"],
        category_orders={"selected": [False, True]},
        labels=dict(distance="rank" if "rank" in vis else "distance"),
        width=800,
        height=500,
    )
    fig.update_traces(hoverinfo="none", hovertemplate="<extra></extra>")
    fig.update_layout(showlegend=False)
    return fig


distance_pair_vis_map = {
    "farness_scatter": farness_scatter,
    "slope": slope,
    "rank_slope": slope,
}
distance_pair_vis_types = list(distance_pair_vis_map.keys())

notation_pair_vis_map = {
    "diamond": diamond,
    "slope": slope,
    "rank_slope": slope,
    "tokens": tokens,
    "farness_scatter": farness_scatter,
}
notation_pair_vis_types = list(notation_pair_vis_map.keys())


def wrap_pair_vis(
    gallery, notation, distance, notation2, distance2, vis, from_slug, to_slug
):
    if distance == distance2:
        vis_function = notation_pair_vis_map[vis]
    else:
        vis_function = distance_pair_vis_map[vis]
    fig = vis_function(
        gallery, notation, distance, notation2, distance2, from_slug, to_slug, vis
    )
    return dcc.Graph(
        id=dict(type="figure", suffix="pair", seq="1", notation=notation),
        figure=fig,
        style=dict(width=str(fig.layout.width or "800") + "px", margin="0 auto"),
        clear_on_unhover=True,
    )
