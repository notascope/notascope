from .distances import merged_distances
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc
from .tokens import load_tokens


def tokens(gallery, notation, distance, notation2, distance2, from_spec, to_spec, vis):
    tokens_df = load_tokens()

    df = (
        tokens_df.query(
            f"gallery == '{gallery}' and notation in ('{notation}', '{notation2}')"
        )
        .groupby(["token", "notation"])["spec"]
        .nunique()
        .reset_index()
    )
    fig = px.ecdf(
        df,
        x="spec",
        color="notation",
        hover_name="token",
        ecdfnorm=None,
        height=600,
        markers=True,
        lines=True,
        # ecdfmode="complementary",
        labels=dict(spec="token frequency"),
    )
    fig.update_traces(line_shape="linear", marker_size=5, line_width=1)
    fig.update_yaxes(title_text="token frequency rank")
    fig.update_layout(scattermode="group")
    return fig


def diamond(gallery, notation, distance, notation2, distance2, from_spec, to_spec, vis):
    merged = merged_distances(gallery, notation, distance, notation2, distance2)

    x = distance + "_" + notation
    y = distance2 + "_" + notation2

    merged = merged.groupby("from_spec")[[x, y]].median().reset_index()
    merged["selected"] = (merged["from_spec"] == from_spec) | (
        merged["from_spec"] == to_spec
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
                customdata=merged["from_spec"],
                hoverinfo="none",
                hovertemplate="<extra></extra>",
            ),
            go.Carpet(
                a=[mn, md, mx, mn, md, mx, mn, md, mx],
                b=[mn, mn, mn, md, md, md, mx, mx, mx],
                x=[0, -5, -10, 5, 0, -5, 10, 5, 0],
                y=[0, 5, 10, 5, 10, 15, 10, 15, 20],
                aaxis=dict(
                    title=f"{notation} {distance} remoteness", gridcolor="lightgrey"
                ),
                baxis=dict(
                    title=f"{notation2} {distance2} remoteness", gridcolor="lightgrey"
                ),
            ),
        ]
    )
    if from_spec != "":
        fig.add_scattercarpet(
            mode="markers",
            a=merged.query("selected")[x],
            b=merged.query("selected")[y],
            customdata=merged.query("selected")["from_spec"],
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


def length_scatter(
    gallery, notation, distance, notation2, distance2, from_spec, to_spec, vis
):
    return remoteness_scatter(
        gallery,
        notation,
        "from_length",
        notation2,
        "from_length",
        from_spec,
        to_spec,
        vis,
    )


def remoteness_scatter(
    gallery, notation, distance, notation2, distance2, from_spec, to_spec, vis
):
    import statsmodels.api as sm

    merged_in = merged_distances(gallery, notation, distance, notation2, distance2)

    x = str(merged_in.columns[2])
    y = str(merged_in.columns[3])

    merged = merged_in.groupby("from_spec")[[x, y]].median().reset_index()
    merged["selected"] = (merged["from_spec"] == from_spec) | (
        merged["from_spec"] == to_spec
    )
    mn = 0  # min(merged[x].min(), merged[y].min())
    mx = max(merged[x].max(), merged[y].max())
    s = 0.1 * (mx - mn)
    mx += s

    fig = px.scatter(
        merged,
        x=x,
        y=y,
        color="selected",
        hover_data=["from_spec"],
        category_orders={"selected": [False, True]},
        width=500,
        height=500,
        labels={
            x: " ".join(
                [
                    distance if distance != "from_length" else "spec length",
                    notation,
                    (" remoteness" if distance != "from_length" else ""),
                ]
            ),
            y: " ".join(
                [
                    distance2 if distance2 != "from_length" else "spec length",
                    notation2,
                    (" remoteness" if distance2 != "from_length" else ""),
                ]
            ),
        },
    )
    fig.update_traces(hoverinfo="none", hovertemplate="<extra></extra>")
    fig.update_layout(showlegend=False)
    if distance == distance2:
        fig.add_shape(type="line", x0=mn, x1=mx, y0=mn, y1=mx, line_color="white")
        fig.update_xaxes(rangemode="tozero", range=[mn, mx])
        fig.update_yaxes(rangemode="tozero", range=[mn, mx])
    else:
        fig.add_traces(
            px.line(sm.PCA(merged[[x, y]]).project(ncomp=1), x=x, y=y)
            .update_traces(
                line_color="grey", hoverinfo="skip", hovertemplate="<extra></extra>"
            )
            .data
        )
    if len(fig.data) > 1:
        fig.data[1].marker.size = 10
    return fig


def distance_scatter(
    gallery, notation, distance, notation2, distance2, from_spec, to_spec, vis
):
    import statsmodels.api as sm

    merged = (
        merged_distances(gallery, notation, distance, notation2, distance2)
        .query("from_spec < to_spec")
        .copy()
    )

    x = str(merged.columns[2])
    y = str(merged.columns[3])
    merged["selected"] = False
    if from_spec:
        merged.loc[
            (merged["from_spec"] == from_spec) | (merged["to_spec"] == from_spec),
            "selected",
        ] = from_spec
    if to_spec:
        merged.loc[
            (merged["from_spec"] == to_spec) | (merged["to_spec"] == to_spec),
            "selected",
        ] = to_spec
    if from_spec and to_spec:
        merged.loc[
            (merged["from_spec"] == min(from_spec, to_spec))
            & (merged["to_spec"] == max(from_spec, to_spec)),
            "selected",
        ] = "here"

    mn = 0  # min(merged[x].min(), merged[y].min())
    mx = max(merged[x].max(), merged[y].max())
    s = 0.1 * (mx - mn)
    mx += s

    fig = px.scatter(
        merged,
        x=x,
        y=y,
        color="selected",
        hover_data=["from_spec", "to_spec"],
        category_orders=dict(selected=[False, from_spec, to_spec, "here"]),
        color_discrete_map={
            False: "grey",
            "here": px.colors.qualitative.Plotly[1],
            from_spec: px.colors.qualitative.Plotly[0],
            to_spec: px.colors.qualitative.Plotly[2],
        },
        width=500,
        height=500,
        labels={x: x + " distances", y: y + " distances"},
    )
    fig.update_traces(hoverinfo="none", hovertemplate="<extra></extra>")
    fig.update_layout(showlegend=False)
    if len(fig.data) > 1:
        fig.update_traces(selector=0, marker_size=2)
    if len(fig.data) == 4:
        fig.update_traces(
            selector=3, marker=dict(size=10, line_color="white", line_width=2)
        )
    if distance == distance2:
        fig.add_shape(
            type="line", x0=mn, x1=mx, y0=mn, y1=mx, line_color="white", line_width=1
        )
        fig.update_xaxes(rangemode="tozero", range=[mn, mx])
        fig.update_yaxes(rangemode="tozero", range=[mn, mx])
    else:
        fig.add_traces(
            px.line(sm.PCA(merged[[x, y]]).project(ncomp=1), x=x, y=y)
            .update_traces(
                line_color="grey",
                hoverinfo="skip",
                hovertemplate="<extra></extra>",
                line_width=1,
            )
            .data
        )
    return fig


def slope(gallery, notation, distance, notation2, distance2, from_spec, to_spec, vis):
    df = merged_distances(gallery, notation, distance, notation2, distance2)
    if from_spec:
        df = df.query(f"from_spec == '{from_spec}'")
    df = df.groupby("to_spec").median(numeric_only=True).reset_index()
    if "rank" in vis:
        for col in df.columns[1:]:
            df[col] = df[col].rank(method="first")
    df["none"] = None
    df["selected"] = df["to_spec"] == to_spec
    df = (
        df.melt(id_vars=["to_spec", "selected"], var_name="pair", value_name="distance")
        .sort_values(by=["to_spec", "distance"])
        .query("pair != 'none'")
    )
    fig = px.line(
        df,
        x="distance",
        y="pair",
        line_group="to_spec",
        color="selected",
        markers=True,
        hover_data=["to_spec"],
        category_orders={"selected": [False, True]},
        labels=dict(distance="rank" if "rank" in vis else "distance"),
        width=800,
        height=500,
    )
    fig.update_traces(hoverinfo="none", hovertemplate="<extra></extra>")
    fig.update_layout(showlegend=False)
    return fig


distance_pair_vis_map = {
    "scatter": remoteness_scatter,
    "distances": distance_scatter,
    "slope": slope,
    "rank_slope": slope,
}
distance_pair_vis_types = list(distance_pair_vis_map.keys())

notation_pair_vis_map = {
    "scatter": remoteness_scatter,
    "length_scatter": length_scatter,
    "diamond": diamond,
    "slope": slope,
    "rank_slope": slope,
    "tokens": tokens,
    "distances": distance_scatter,
}
notation_pair_vis_types = list(notation_pair_vis_map.keys())


def wrap_pair_vis(
    gallery, notation, distance, notation2, distance2, vis, from_spec, to_spec
):
    if distance == distance2:
        vis_function = notation_pair_vis_map[vis]
    else:
        vis_function = distance_pair_vis_map[vis]
    fig = vis_function(
        gallery, notation, distance, notation2, distance2, from_spec, to_spec, vis
    )
    return dcc.Graph(
        id=dict(type="figure", suffix="pair", seq="1", notation=notation),
        figure=fig,
        style=dict(width=str(fig.layout.width or "800") + "px", margin="0 auto"),
        clear_on_unhover=True,
    )
