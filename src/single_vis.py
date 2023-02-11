import dash_cytoscape as cyto
import plotly.graph_objects as go
from dash import dcc, html
from .scatter import get_scatter
from .dendro import get_dendro
from .network import get_network
from .distances import distances_df
from .distributions import token_rank, token_bars, farness, get_farness_scatter
from .utils import load_registry
from .utils import ext
from pathlib import Path


def thumbnails_for_notation(gallery, distance, notation):
    registry = load_registry()
    slugs = registry[gallery][notation]["slugs"]
    langs = dict(py="python", R="R", json="json", vl="json")
    srcext = ext(gallery, notation, "source")
    lang = langs[srcext]
    return [
        html.Table(
            [
                html.Tr(
                    [
                        html.Td(
                            [
                                html.P(s, style=dict(margin=0)),
                                html.Img(
                                    src=f"/assets/results/{gallery}/{notation}/img/{s}.png",
                                    id=dict(
                                        type="thumbnail", notation=notation, slug=s
                                    ),
                                    className="bigthumb",
                                ),
                            ],
                            style=dict(
                                verticalAlign="top", borderBottom="1px solid lightgrey"
                            ),
                        ),
                        html.Td(
                            dcc.Markdown(
                                "```"
                                + lang
                                + "\n"
                                + Path(
                                    f"results/{gallery}/{notation}/pretty/{s}.{srcext}"
                                ).read_text()
                                + "```",
                                style=dict(textAlign="left"),
                            ),
                            style=dict(
                                verticalAlign="top", borderBottom="1px solid lightgrey"
                            ),
                        ),
                    ]
                )
                for s in slugs
            ],
            style=dict(margin="0 auto"),
            className="thumbnails",
        )
    ]


def thumbnails(gallery, notation, distance, from_slug, to_slug, vis):
    df = distances_df(gallery=gallery).query(f"notation=='{notation}'")
    if from_slug:
        df = df.query(f"from_slug == '{from_slug}'")
    sorted_slugs = (
        df.groupby("to_slug")[distance]
        .median()
        .reset_index()
        .sort_values(by=distance)
        .to_slug
    )
    thumbs = []
    if from_slug:
        thumbs += [
            html.Img(
                id=dict(type="thumbnail", no_notation=notation, slug=from_slug),
                src=f"/assets/results/{gallery}/{notation}/img/{from_slug}.png",
                className="selected_thumb",
            ),
            html.Br(),
        ]

    for slug in sorted_slugs:
        thumbs.append(
            html.Img(
                id=dict(type="thumbnail", no_notation=notation, slug=slug),
                src=f"/assets/results/{gallery}/{notation}/img/{slug}.png",
                className="selected_thumb" if slug == to_slug else "regular_thumb",
            )
        )
    return html.Div(thumbs, className="thumbnails", style=dict(textAlign="center"))


vis_map = {
    "thumbnails": thumbnails,
    "mst": get_network,
    "spanner-1.5": get_network,
    "spanner-1.2": get_network,
    "spanner-1.1": get_network,
    "spanner-1": get_network,
    "tsne": get_scatter,
    "umap": get_scatter,
    "dendro": get_dendro,
    "token_rank": token_rank,
    "token_bars": token_bars,
    "farness": farness,
    "farness_scatter": get_farness_scatter,
}
single_vis_types = list(vis_map.keys())


def get_vis(gallery, notation, distance, vis, from_slug, to_slug):
    return [vis_map[vis](gallery, notation, distance, from_slug, to_slug, vis)]


def wrap_single_vis(gallery, notation, distance, vis, from_slug, to_slug, suffix):
    vis_list = []
    for i, vis_out in enumerate(
        get_vis(gallery, notation, distance, vis, from_slug, to_slug)
    ):
        if isinstance(vis_out, go.Figure):
            vis_list.append(
                figure(
                    dict(type="figure", notation=notation, suffix=suffix, seq=str(i)),
                    vis_out,
                )
            )
        elif isinstance(vis_out, html.Div):
            vis_list.append(vis_out)
        else:
            vis_list.append(
                cytoscape(dict(type="network", suffix=suffix, seq=str(i)), vis_out)
            )
    return vis_list


def figure(id, fig):
    return dcc.Graph(
        id=id, figure=fig, config=dict(scrollZoom=True), clear_on_unhover=True
    )


def cytoscape(id, elements):
    return cyto.Cytoscape(
        id=id,
        className="network",
        layout={"name": "preset", "fit": True},
        minZoom=0.05,
        maxZoom=1,
        autoRefreshLayout=False,
        elements=elements,
        style=dict(height="800px", width="initial"),
        stylesheet=[
            {
                "selector": "node",
                "style": {
                    "width": 100,
                    "height": 100,
                    "shape": "rectangle",
                    "background-fit": "cover",
                    "background-image": "data(url)",
                    "label": "data(label)",
                    "border-color": "grey",
                    "border-width": 1,
                    "text-outline-color": "white",
                    "text-outline-width": "2",
                    "text-margin-y": "20",
                },
            },
            {
                "selector": "edge",
                "style": {
                    "line-color": "lightgrey",
                    "curve-style": "bezier",
                    "target-arrow-color": "lightgrey",
                    "control-point-weight": 0.6,
                    "target-arrow-shape": "triangle-backcurve",
                    "arrow-scale": 2,
                    "label": "data(length)",
                    "font-size": "24px",
                    "text-outline-color": "white",
                    "text-outline-width": "3",
                },
            },
            {
                "selector": ".bidir",
                "style": {
                    "source-arrow-color": "lightgrey",
                    "source-arrow-shape": "triangle-backcurve",
                },
            },
            {
                "selector": ".selected",
                "style": {
                    "source-arrow-color": "red",
                    "target-arrow-color": "red",
                    "line-color": "red",
                    "border-color": "red",
                    "border-width": 5,
                },
            },
            {
                "selector": ".inserted",
                "style": {"line-style": "dashed"},
            },
            {
                "selector": ".neighbour",
                "style": {"line-color": "red"},
            },
        ],
    )
