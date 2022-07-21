# builtins
import re
from collections import Counter
from glob import glob

# plotly
from dash import Dash, html, dcc, Input, Output, State, callback_context
from dash_extensions import EventListener
from notascope_components import DashDiff

# data science
import pandas as pd
import numpy as np

from src import vis_types
from src.distances import get_distance, distance_types
from src.dimred import get_dimred
from src.dendro import get_dendro
from src.network import get_network, cytoscape

default_study = "tiny"

print("start", np.random.randint(1000))  # unseeded so every launch is different

tokens_df = pd.read_csv("results/tokens.tsv", names=["study", "notation", "slug", "token"], delimiter="\t")


def ext_of_longest(study, notation, obj):
    return sorted(glob(f"results/{study}/{notation}/{obj}/*"), key=len)[-1].split(".")[-1]


def load_results():
    results = dict()
    for (study, notation), df in tokens_df.groupby(["study", "notation"]):
        if study not in results:
            results[study] = dict()
        results[study][notation] = dict(
            imgext=ext_of_longest(study, notation, "img"),
            srcext=ext_of_longest(study, notation, "source"),
            slugs=df["slug"].unique(),
            tokens=df["token"].nunique(),
        )
    return results


results = load_results()
print("ready")

app = Dash(__name__, title="NotaScope", suppress_callback_exceptions=True)


app.layout = html.Div(
    [
        html.Div(id="content"),
        dcc.Location(id="location"),
        dcc.Tooltip(
            id="tooltip",
            children=[
                html.Div(
                    [
                        html.P(id="tt_name", style=dict(textAlign="center")),
                        html.Img(id="tt_img", style={"max-width": "300px", "max-height": "200px"}),
                    ],
                    style={"width": "300px", "height": "230px", "overflow": "hidden"},
                )
            ],
        ),
        EventListener(
            id="event_listener",
            events=[
                {"event": "keydown", "props": ["shiftKey"]},
                {"event": "keyup", "props": ["shiftKey"]},
            ],
        ),
    ]
)


def parse_hashpath(hashpath):
    m = re.match("#" + "/(.*)" * 9, hashpath)
    if m:
        return sanitize_state(*m.groups())
    else:
        return sanitize_state()


def sanitize_state(study="", notation="", distance="", vis="", notation2="", distance2="", vis2="", from_slug="", to_slug=""):
    if vis not in vis_types:
        vis = vis_types[0]

    if vis2 not in vis_types:
        vis2 = vis_types[0]

    if distance not in distance_types:
        distance = distance_types[0]

    if distance2 not in distance_types:
        distance2 = distance_types[0]

    if study not in results:
        study = default_study

    study_res = results[study]
    slugs = set()
    if notation in study_res:
        for s in study_res[notation]["slugs"]:
            slugs.add(s)
    else:
        notation = list(results[study].keys())[0]

    if notation2 in study_res:
        for s in study_res[notation2]["slugs"]:
            slugs.add(s)
    else:
        notation2 = ""

    if notation2 == "":
        vis2 = ""
        distance2 = ""

    if from_slug not in slugs:
        from_slug = to_slug = ""
    elif to_slug not in slugs:
        to_slug = from_slug

    return study, notation, distance, vis, notation2, distance2, vis2, from_slug, to_slug


@app.callback(
    Output("location", "hash"),
    Output("network", "tapNodeData"),
    Output("network", "tapEdgeData"),
    Output("network2", "tapNodeData"),
    Output("network2", "tapEdgeData"),
    Input("selection", "data"),
    Input("study", "value"),
    Input("notation", "value"),
    Input("notation2", "value"),
    Input("distance", "value"),
    Input("distance2", "value"),
    Input("vis", "value"),
    Input("vis2", "value"),
    Input("network", "tapNodeData"),
    Input("network", "tapEdgeData"),
    Input("figure", "clickData"),
    Input("network2", "tapNodeData"),
    Input("network2", "tapEdgeData"),
    Input("figure2", "clickData"),
    State("event_listener", "event"),
)
def update_hashpath(
    selection, study, notation, notation2, distance, distance2, vis, vis2, node_data, edge_data, fig_data, node_data2, edge_data2, fig_data2, event
):
    shift_down = bool((dict(shiftKey=False) if not event else event)["shiftKey"])
    ctx = callback_context
    from_slug, to_slug = selection
    if ctx.triggered:
        click_notation = ctx.triggered[0]["prop_id"].split(".")[0]
        click_type = ctx.triggered[0]["prop_id"].split(".")[1]

        if click_type == "clickData":
            for id, data in [["figure", fig_data], ["figure2", fig_data2]]:
                if click_notation == id:
                    to_slug = data["points"][0]["hovertext"]
                    if from_slug == to_slug:
                        from_slug = to_slug = ""
                    elif not shift_down:
                        from_slug = to_slug
        if click_type == "tapNodeData":
            for id, data in [["network", node_data], ["network2", node_data2]]:
                if click_notation == id:
                    to_slug = data["id"]
                    if from_slug == to_slug:
                        from_slug = to_slug = ""
                    elif not shift_down:
                        from_slug = to_slug
            edge_data = None
            edge_data2 = None
        if click_type == "tapEdgeData":
            for id, data in [["network", edge_data], ["network2", edge_data2]]:
                if click_notation == id:
                    from_slug = data["source"]
                    to_slug = data["target"]
            node_data = None
            node_data2 = None
    hashpath = "#/" + "/".join(sanitize_state(study, notation, distance, vis, notation2, distance2, vis2, from_slug, to_slug))
    return hashpath, node_data, edge_data, node_data2, edge_data2


@app.callback(
    Output("content", "children"),
    Input("location", "hash"),
)
def update_content(hashpath):
    study, notation, distance, vis, notation2, distance2, vis2, from_slug, to_slug = parse_hashpath(hashpath)
    cmp, net, fig = details_view(study, notation, distance, vis, from_slug, to_slug)
    if notation2:
        style = dict()
        style2 = dict(gridColumnStart=2, display="block")
        cmp2, net2, fig2 = details_view(study, notation2, distance2, vis2, from_slug, to_slug)
    else:
        style = dict(gridRowStart=2)
        style2 = dict(display="none", gridRowStart=3)
        cmp2, net2, fig2 = None, [], {}

    vis2_style = dict(width="100px")
    if notation == notation2 and distance == distance2:
        cmp2 = None
    if not notation2:
        vis2_style["display"] = "none"

    notations = [dict(label=f"{s} ({results[study][s]['tokens']})", value=s) for s in results[study]]

    return html.Div(
        className="wrapper",
        children=[
            html.Div(
                [dcc.Dropdown(id="study", value=study, options=[s for s in results], clearable=False, style=dict(width="100px"))],
                style=dict(position="absolute", left=10, top=10),
            ),
            html.Div(
                [
                    html.Div(
                        dcc.Dropdown(id="notation", value=notation, options=notations, clearable=False, className="dropdown"),
                        style=dict(display="inline-block"),
                    ),
                    html.Div(
                        dcc.Dropdown(id="vis", value=vis, options=vis_types, clearable=False, style=dict(width="100px")),
                        style=dict(display="inline-block"),
                    ),
                    html.Div(
                        dcc.Dropdown(id="distance", value=distance, options=distance_types, clearable=False, style=dict(width="100px")),
                        style=dict(display="inline-block"),
                    ),
                ],
                style=dict(margin="0 auto"),
            ),
            html.Div(
                [
                    html.Div(
                        dcc.Dropdown(id="notation2", value=notation2, options=notations, clearable=True, className="dropdown"),
                        style=dict(display="inline-block"),
                    ),
                    html.Div(
                        dcc.Dropdown(id="vis2", value=vis2, options=vis_types, clearable=False, style=vis2_style),
                        style=dict(display="inline-block"),
                    ),
                    html.Div(
                        dcc.Dropdown(id="distance2", value=distance2, options=distance_types, clearable=False, style=vis2_style),
                        style=dict(display="inline-block"),
                    ),
                ],
                style=dict(margin="0 auto"),
            ),
            html.Div(network_or_figure(net, fig, ""), style=style),
            html.Div(network_or_figure(net2, fig2, "2"), style=style2),
            html.Div(cmp, className="comparison"),
            html.Div(cmp2, className="comparison"),
            dcc.Store(id="selection", data=[from_slug, to_slug]),
        ],
    )


def hide_if_none(thing):
    return dict() if thing else dict(display="none")


def network_or_figure(net, fig, suffix):
    return [
        html.Div(cytoscape("network" + suffix, net), style=hide_if_none(net)),
        html.Div(dcc.Graph(id="figure" + suffix, figure=fig, config=dict(scrollZoom=True), clear_on_unhover=True), style=hide_if_none(fig)),
    ]


def header_and_image(study, notation, slug, tokens_n, tokens_nunique):
    imgext = results[study][notation]["imgext"]
    return [
        html.H3(slug),
        html.P(f"{tokens_n} tokens, {tokens_nunique} uniques"),
        html.Img(
            src=f"/assets/results/{study}/{notation}/img/{slug}.{imgext}",
            style=dict(verticalAlign="middle", maxHeight="200px", maxWidth="20vw"),
        ),
    ]


def diff_view(study, notation, from_slug, to_slug):
    srcext = results[study][notation]["srcext"]
    with open(f"results/{study}/{notation}/source/{from_slug}.{srcext}", "r") as f:
        from_code = f.read()
    if from_slug == to_slug:
        to_code = from_code
    else:
        with open(f"results/{study}/{notation}/source/{to_slug}.{srcext}", "r") as f:
            to_code = f.read()
    return html.Div(
        [html.Div([DashDiff(oldCode=from_code, newCode=to_code)], style=dict(border="none"))],
        style=dict(marginTop="20px", textAlign="left", height="300px", maxWidth="48vw", overflow="scroll", border="1px solid grey"),
    )


def get_token_info(study, notation, slug):
    df = tokens_df.query("study==@study and notation==@notation and slug==@slug")["token"]
    return df.values, len(df), df.nunique()


def details_view(study, notation, distance, vis, from_slug, to_slug):
    cmp = None
    net = []
    fig = {}
    if vis == "network":
        imgext = results[study][notation]["imgext"]
        net = get_network(study, notation, distance, from_slug, to_slug, imgext)
    elif vis == "tsne":
        fig = get_dimred(study, notation, distance, from_slug, to_slug, method="tsne")
    elif vis == "umap":
        fig = get_dimred(study, notation, distance, from_slug, to_slug, method="umap")
    elif vis == "dendro":
        fig = get_dendro(study, notation, distance, from_slug, to_slug)
    else:
        raise Exception("invalid vis")

    try:
        from_tokens, from_tokens_n, from_tokens_nunique = get_token_info(study, notation, from_slug)
        if from_slug != to_slug:

            to_tokens, to_tokens_n, to_tokens_nunique = get_token_info(study, notation, to_slug)
            from_to_distance = get_distance(study, notation, distance, from_slug, to_slug)
            to_from_distance = get_distance(study, notation, distance, to_slug, from_slug)

            shared_tokens = list((Counter(from_tokens) & Counter(to_tokens)).elements())
            shared_uniques = set(from_tokens) & set(to_tokens)
            td1 = html.Td(
                header_and_image(study, notation, from_slug, from_tokens_n, from_tokens_nunique),
                style=dict(verticalAlign="top"),
            )
            td2 = html.Td(
                ["tokens", html.Br()]
                + [f"{from_tokens_n - len(shared_tokens)} ⬌ {to_tokens_n - len(shared_tokens)}"]
                + [html.Br(), html.Br(), "uniques", html.Br()]
                + [f"{from_tokens_nunique - len(shared_uniques)} ⬌ {to_tokens_nunique - len(shared_uniques)}"]
                + [html.Br(), html.Br(), "tree edit", html.Br(), f"{to_from_distance} ⬌ {from_to_distance}"]
            )
            td3 = html.Td(
                header_and_image(study, notation, to_slug, to_tokens_n, to_tokens_nunique),
                style=dict(verticalAlign="top"),
            )
            cmp = [html.Table([html.Tr([td1, td2, td3])], style=dict(width="100%", height="300px"))]
        elif from_slug != "":
            _, from_tokens_n, from_tokens_nunique = get_token_info(study, notation, from_slug)
            cmp = header_and_image(study, notation, from_slug, from_tokens_n, from_tokens_nunique)

        if from_slug != "":
            cmp += [diff_view(study, notation, from_slug, to_slug)]

    except Exception as e:
        print(repr(e))

    return (cmp, net, fig)


# if/when there is a PNG notation, just inline the imgext dict in the string
app.clientside_callback(
    """
    function(hoverData, hoverData2) {
        pieces = window.location.hash.split("/");
        study=pieces[1];
        if(!hoverData){
            if(!hoverData2){
                return [false, null, null, null];
            }
            hoverData = hoverData2;
            notation=pieces[5];
        }
        else {
            notation=pieces[2];
        }
        pt = hoverData["points"][0];
        bbox = pt["bbox"]
        slug = pt["hovertext"]
        return [true, bbox, "/assets/results/"+study+"/"+notation+"/img/"+slug+".svg", slug]
    }
    """,
    Output("tooltip", "show"),
    Output("tooltip", "bbox"),
    Output("tt_img", "src"),
    Output("tt_name", "children"),
    Input("figure", "hoverData"),
    Input("figure2", "hoverData"),
    prevent_initial_call=True,
)


if __name__ == "__main__":
    app.run_server(debug=True)
