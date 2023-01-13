import dash_cytoscape as cyto
import plotly.graph_objects as go
from dash import dcc
from .scatter import get_scatter
from .dendro import get_dendro
from .network import get_network
from .distributions import token_rank, token_bars, farness, get_farness_scatter

vis_map = {
    "mst": get_network,
    "spanner-1": get_network,
    "spanner-1.1": get_network,
    "spanner-1.2": get_network,
    "spanner-1.5": get_network,
    "tsne": get_scatter,
    "umap": get_scatter,
    "dendro": get_dendro,
    "token_rank": token_rank,
    "token_bars": token_bars,
    "farness": farness,
    "farness_scatter": get_farness_scatter,
}
vis_types = list(vis_map.keys())


def get_vis(gallery, notation, distance, vis, from_slug, to_slug):
    return [vis_map[vis](gallery, notation, distance, from_slug, to_slug, vis)]


def wrap_vis(gallery, notation, distance, vis, from_slug, to_slug, suffix):
    vis_list = []
    for i, vis in enumerate(
        get_vis(gallery, notation, distance, vis, from_slug, to_slug)
    ):
        if isinstance(vis, go.Figure):
            vis_list.append(
                figure(
                    dict(type="figure", notation=notation, suffix=suffix, seq=str(i)),
                    vis,
                )
            )
        else:
            vis_list.append(
                cytoscape(dict(type="network", suffix=suffix, seq=str(i)), vis)
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
