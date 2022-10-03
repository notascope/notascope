# builtins
import re
from collections import Counter

# plotly
from dash import Dash, html, dcc, Input, Output, State, callback_context
from dash_extensions import EventListener
import dash_cytoscape as cyto
from notascope_components import DashDiff

# data science
import pandas as pd
import numpy as np

from src import vis_types, ext, get_distance, distance_types, get_vis, merged_distances

import plotly.express as px

print("start", np.random.randint(1000))
tokens_df = pd.read_csv("results/tokens.tsv", names=["study", "notation", "slug", "token"], delimiter="\t")


def load_results():
    results = dict()
    for (study, notation), df in tokens_df.groupby(["study", "notation"]):
        if study not in results:
            results[study] = dict()
        results[study][notation] = dict(
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
                        html.P(id="tt_name", style=dict(textAlign="center", display="none")),
                        html.Img(id="tt_img", style={"width": "100px", "height": "100px", "object-fit": "cover", "margin": 0}),
                    ],
                    style={"width": "100px", "height": "100px", "padding": 0, "margin": 0},
                )
            ],
            style={"opacity": 0.85, "padding": 0, "margin": 0},
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
        vis2 = ""

    if distance not in distance_types:
        distance = distance_types[0]

    if distance2 not in distance_types:
        distance2 = ""

    if study not in results:
        study = "tiny"

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
    Input("crossfig", "clickData"),
    State("event_listener", "event"),
)
def update_hashpath(
    selection,
    study,
    notation,
    notation2,
    distance,
    distance2,
    vis,
    vis2,
    node_data,
    edge_data,
    fig_data,
    node_data2,
    edge_data2,
    fig_data2,
    crossfig_data,
    event,
):
    shift_down = bool((dict(shiftKey=False) if not event else event)["shiftKey"])
    ctx = callback_context
    from_slug, to_slug = selection
    if ctx.triggered:
        trig_id, trig_type = ctx.triggered[0]["prop_id"].split(".")

        if trig_type == "clickData":
            for id, data in [["figure", fig_data], ["figure2", fig_data2], ["crossfig", crossfig_data]]:
                if trig_id == id:
                    to_slug = data["points"][0]["hovertext"]
                    if from_slug == to_slug:
                        from_slug = to_slug = ""
                    elif not shift_down:
                        from_slug = to_slug

        if trig_type == "tapNodeData":
            for id, data in [["network", node_data], ["network2", node_data2]]:
                if trig_id == id:
                    to_slug = data["id"]
                    if from_slug == to_slug:
                        from_slug = to_slug = ""
                    elif not shift_down:
                        from_slug = to_slug
            edge_data = None
            edge_data2 = None
        if trig_type == "tapEdgeData":
            for id, data in [["network", edge_data], ["network2", edge_data2]]:
                if trig_id == id:
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
    study, notation, distance, vis, notation2, distance2_in, vis2_in, from_slug, to_slug = parse_hashpath(hashpath)
    distance2 = distance2_in or distance
    vis2 = vis2_in or vis
    cmp, net, fig = details_view(study, notation, distance, vis, from_slug, to_slug)
    cross_fig = {}
    cross_style = dict(display="none")
    if notation2:
        style = dict()
        style2 = dict(gridColumnStart=2, display="block")
        cmp2, net2, fig2 = details_view(study, notation2, distance2, vis2, from_slug, to_slug)
        if (notation != notation2 and distance == distance2) or (notation == notation2 and distance != distance2):
            cross_style = dict(gridColumn="1/3")
            cross_fig = cross_notation_figure(study, notation, distance, notation2, distance2, from_slug, to_slug)
    else:
        style = dict(gridRowStart=2)
        style2 = dict(display="none", gridRowStart=3)
        cross_style = dict(display="none")
        cmp2, net2, fig2, cross_fig = None, [], {}, {}

    if distance == distance2:
        if notation == notation2:
            cmp2 = None

    vis2_style = dict(width="100px")
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
                        dcc.Dropdown(id="vis2", value=vis2_in, options=vis_types, clearable=True, style=vis2_style),
                        style=dict(display="inline-block"),
                    ),
                    html.Div(
                        dcc.Dropdown(id="distance2", value=distance2_in, options=distance_types, clearable=True, style=vis2_style),
                        style=dict(display="inline-block"),
                    ),
                ],
                style=dict(margin="0 auto"),
            ),
            html.Div(
                html.Details(
                    [
                        html.Summary("Cross-Notation"),
                        dcc.Graph(id="crossfig", figure=cross_fig, style=dict(width="500px", margin="0 auto"), clear_on_unhover=True),
                    ],
                    open=True,
                ),
                style=cross_style,
            ),
            html.Div(html.Details([html.Summary(notation + " " + vis), *network_or_figure(net, fig, "")], open=True), style=style),
            html.Div(html.Details([html.Summary(notation2 + " " + vis2), *network_or_figure(net2, fig2, "2")], open=True), style=style2),
            html.Div(cmp, className="comparison"),
            html.Div(cmp2, className="comparison"),
            dcc.Store(id="selection", data=[from_slug, to_slug]),
        ],
    )


def cross_notation_figure(study, notation, distance, notation2, distance2, from_slug, to_slug):

    merged = merged_distances(study, notation, distance, notation2, distance2)

    x = distance
    y = distance2
    if notation != notation2:
        x += "_" + notation
        y += "_" + notation2

    merged = merged.groupby("from_slug").mean([x, y]).reset_index()
    merged["selected"] = (merged["from_slug"] == from_slug) | (merged["from_slug"] == to_slug)

    fig = px.scatter(merged, x=x, y=y, hover_name="from_slug", color="selected", width=500, height=500)
    fig.update_layout(showlegend=False)
    if len(fig.data) > 1:
        fig.data[1].marker.size = 10

    if distance == distance2:
        the_min = min(merged[x].min(), merged[y].min())
        the_max = max(merged[x].max(), merged[y].max())
        stretch = 0.1 * (the_max - the_min)
        fig.add_shape(
            type="line", line=dict(color="white", width=1), x0=the_min - stretch, y0=the_min - stretch, x1=the_max + stretch, y1=the_max + stretch
        )
    return fig.update_traces(hoverinfo="none", hovertemplate=None)


cross_notation_figure("movies", "vega-lite", "nmi", "plotly_express", "nmi", "bar_count", "bubble_agg")


def hide_if_none(thing):
    return dict(border="1px solid lightgrey") if thing else dict(display="none")


def network_or_figure(net, fig, suffix):
    return [
        html.Div(cytoscape("network" + suffix, net), style=hide_if_none(net)),
        html.Div(figure("figure" + suffix, fig), style=hide_if_none(fig)),
    ]


def figure(id, fig):
    return dcc.Graph(id=id, figure=fig, config=dict(scrollZoom=True), clear_on_unhover=True)


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


def header_and_image(study, notation, slug, tokens_n, tokens_nunique):
    imgext = ext(study, notation, "img")

    return [
        html.H3(slug),
        html.P(f"{tokens_n} tokens, {tokens_nunique} uniques"),
        html.Img(
            src=f"/assets/results/{study}/{notation}/img/{slug}.{imgext}",
            style=dict(verticalAlign="middle", maxHeight="200px", maxWidth="20vw"),
        ),
    ]


def diff_view(study, notation, from_slug, to_slug):
    srcext = ext(study, notation, "source")
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
    df = tokens_df.query(f"study=='{study}' and notation=='{notation}' and slug=='{slug}'")["token"]
    return df.values, len(df), df.nunique()


def details_view(study, notation, distance, vis, from_slug, to_slug):
    cmp = None
    net, fig = get_vis(study, notation, distance, vis, from_slug, to_slug)

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
    function(hoverData, hoverData2, hoverDataCross) {
        if(!hoverData && !hoverData2 && !hoverDataCross) {
            return [false, null, null, null];
        }
        pieces = window.location.hash.split("/");
        study=pieces[1];
        if(hoverData) {
            notation=pieces[2]
        }
        if(hoverData2) {
            hoverData = hoverData2;
            notation=pieces[5];
        }
        if(hoverDataCross) {
            hoverData = hoverDataCross;
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
    Input("crossfig", "hoverData"),
    prevent_initial_call=True,
)


if __name__ == "__main__":
    app.run_server(debug=True)
