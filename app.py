# builtins
from functools import cache
import re
from collections import Counter
from datetime import datetime

# plotly
from dash import Dash, html, dcc, Input, Output, State, callback_context, ALL
from dash_extensions import EventListener
import dash_cytoscape as cyto
from notascope_components import DashDiff

# data science
import pandas as pd

from src import vis_types, ext, get_distance, distance_types, get_vis, merged_distances

import plotly.graph_objects as go
import plotly.express as px
from dash_dangerously_set_inner_html import DangerouslySetInnerHTML
import spectra
import math

print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
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
    Output(dict(type="network", suffix=ALL), "tapNodeData"),
    Output(dict(type="network", suffix=ALL), "tapEdgeData"),
    Input("selection", "data"),
    Input("study", "value"),
    Input("notation", "value"),
    Input("notation2", "value"),
    Input("distance", "value"),
    Input("distance2", "value"),
    Input("vis", "value"),
    Input("vis2", "value"),
    Input(dict(type="network", suffix=ALL), "tapNodeData"),
    Input(dict(type="network", suffix=ALL), "tapEdgeData"),
    Input(dict(type="figure", suffix=ALL), "clickData"),
    State("event_listener", "event"),
)
def update_hashpath(selection, study, notation, notation2, distance, distance2, vis, vis2, node_data, edge_data, _, event):
    shift_down = bool((dict(shiftKey=False) if not event else event)["shiftKey"])
    from_slug, to_slug = selection
    if callback_context.triggered:
        trig_prop = callback_context.triggered[0]["prop_id"]
        data = callback_context.triggered[0]["value"]

        if trig_prop.endswith("tapEdgeData"):
            from_slug = data["source"]
            to_slug = data["target"]
            node_data = [None] * len(node_data)

        if trig_prop.endswith("clickData"):
            to_slug = data["points"][0]["hovertext"]
            if from_slug == to_slug:
                from_slug = to_slug = ""
            elif not shift_down:
                from_slug = to_slug

        if trig_prop.endswith("tapNodeData"):
            to_slug = data["id"]
            edge_data = [None] * len(edge_data)
            if from_slug == to_slug:
                from_slug = to_slug = ""
            elif not shift_down:
                from_slug = to_slug

    hashpath = "#/" + "/".join(sanitize_state(study, notation, distance, vis, notation2, distance2, vis2, from_slug, to_slug))
    return hashpath, node_data, edge_data


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
    if notation2:
        style = dict()
        style2 = dict(gridColumnStart=2, display="block")
        cmp2, net2, fig2 = details_view(study, notation2, distance2, vis2, from_slug, to_slug)
        if (notation != notation2 and distance == distance2) or (notation == notation2 and distance != distance2):
            cross_fig = cross_notation_figure(study, notation, distance, notation2, distance2, from_slug, to_slug)
    else:
        style = dict(gridRowStart=2)
        style2 = dict(display="none", gridRowStart=3)
        cmp2, net2, fig2 = None, [], {}

    notations = [dict(label=f"{s} ({results[study][s]['tokens']})", value=s) for s in results[study]]

    return html.Div(
        className="wrapper",
        children=[
            html.Div(
                [
                    dcc.Dropdown(id="study", value=study, options=[s for s in results], clearable=False, style=dict(width="100px")),
                    html.A("table", href=f"/assets/results/{study}/summary.html", target="_blank"),
                ],
                style=dict(position="absolute", left=10, top=10),
            ),
            html.Div(
                [
                    html.Div(
                        dcc.Dropdown(id="notation", value=notation, options=notations, clearable=False, className="dropdown"),
                        style=dict(display="inline-block"),
                    ),
                    html.Div(
                        dcc.Dropdown(id="vis", value=vis, options=vis_types, clearable=False, style=dict(width="150px")),
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
                        dcc.Dropdown(
                            id="notation2", value=notation2, options=notations, clearable=True, className="dropdown", placeholder="Compare..."
                        ),
                        style=dict(display="inline-block"),
                    ),
                    html.Div(
                        dcc.Dropdown(
                            id="vis2",
                            value=vis2_in,
                            options=vis_types,
                            clearable=True,
                            style=dict(width="150px", **({} if notation2 else {"display": "none"})),
                            placeholder=vis2,
                        ),
                        style=dict(display="inline-block"),
                    ),
                    html.Div(
                        dcc.Dropdown(
                            id="distance2",
                            value=distance2_in,
                            options=distance_types,
                            clearable=True,
                            style=dict(width="100px", **({} if notation2 else {"display": "none"})),
                            placeholder=distance2,
                        ),
                        style=dict(display="inline-block"),
                    ),
                ],
                style=dict(margin="0 auto"),
            ),
            html.Div(
                html.Details(
                    [
                        html.Summary("cross-notation"),
                        dcc.Graph(
                            id=dict(type="figure", suffix="cross"),
                            figure=cross_fig,
                            style=dict(width="500px", margin="0 auto"),
                            clear_on_unhover=True,
                        ),
                    ],
                    open=True,
                ),
                style=dict(gridColumn="1/3"),
            )
            if cross_fig
            else None,
            html.Div(html.Details([html.Summary(notation + " " + vis), network_or_figure(net, fig, "1")], open=True), style=style),
            html.Div(
                html.Details([html.Summary(notation2 + " " + vis2, style=dict(textAlign="right")), network_or_figure(net2, fig2, "2")], open=True),
                style=style2,
            ),
            html.Div(cmp, className="comparison"),
            html.Div(cmp2, className="comparison") if distance != distance2 or notation != notation2 else None,
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

    if distance != distance2:
        fig = px.scatter(
            merged, x=x, y=y, hover_name="from_slug", color="selected", hover_data={x: False, y: False, "selected": False}, width=500, height=500
        )
        fig.update_layout(showlegend=False)
        if len(fig.data) > 1:
            fig.data[1].marker.size = 10
    else:
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
                    hovertext=merged["from_slug"],
                    hoverinfo="none",
                    hovertemplate="<extra></extra>",
                ),
                go.Carpet(
                    a=[mn, md, mx, mn, md, mx, mn, md, mx],
                    b=[mn, mn, mn, md, md, md, mx, mx, mx],
                    x=[0, -5, -10, 5, 0, -5, 10, 5, 0],
                    y=[0, 5, 10, 5, 10, 15, 10, 15, 20],
                    aaxis=dict(title=f"{notation} {distance} eccentricity", gridcolor="lightgrey"),
                    baxis=dict(title=f"{notation2} {distance2} eccentricity", gridcolor="lightgrey"),
                ),
            ]
        )
        if from_slug != "":
            fig.add_scattercarpet(
                mode="markers",
                a=merged.query("selected")[x],
                b=merged.query("selected")[y],
                hovertext=merged.query("selected")["from_slug"],
                marker_color="red",
                marker_size=10,
                hoverinfo="none",
                hovertemplate="<extra></extra>",
            )
        fig.add_shape(line_color="lightgrey", line_width=1, x0=0, x1=0, y0=0.1, y1=19.9)
        fig.update_xaxes(visible=False, range=[-11, 11])
        fig.update_yaxes(visible=False, range=[-1, 21])
        fig.update_layout(plot_bgcolor="white", margin=dict(b=0, t=0, l=0, r=0), width=500, height=500, showlegend=False)

    return fig


def network_or_figure(net, fig, suffix):
    if net:
        return html.Div(cytoscape(dict(type="network", suffix=suffix), net))
    if fig:
        return html.Div(figure(dict(type="figure", suffix=suffix), fig))


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
    with open(f"results/{study}/{notation}/pretty/{from_slug}.{srcext}", "r") as f:
        from_code = f.read()
    if from_slug == to_slug:
        to_code = from_code
    else:
        with open(f"results/{study}/{notation}/pretty/{to_slug}.{srcext}", "r") as f:
            to_code = f.read()
    return html.Div(
        [html.Div([DashDiff(oldCode=from_code, newCode=to_code)], style=dict(border="none"))],
        style=dict(marginTop="20px", textAlign="left", height="300px", maxWidth="48vw", overflow="scroll", border="1px solid grey"),
    )


@cache
def build_trie(study, notation):
    filtered = tokens_df.query(f"study=='{study}' and notation=='{notation}'").groupby("token").nunique("slug")
    max_count = filtered["slug"].max()
    trie = dict()
    for token, count in filtered["slug"].items():
        pointer = trie
        for c in token:
            if c not in pointer:
                pointer[c] = dict()
            pointer = pointer[c]
        pointer["count"] = count
    return trie, max_count


def single_view(study, notation, slug):
    srcext = ext(study, notation, "source")
    trie, max_count = build_trie(study, notation)
    with open(f"results/{study}/{notation}/pretty/{slug}.{srcext}", "r") as f:
        text = f.read()

    scale = spectra.scale([spectra.html("#2FF"), spectra.html("#FFF")]).domain([math.log(1), math.log(max_count - 1)])

    out_text = ""

    pointer = trie
    buffer = ""
    for c in text:
        if c not in pointer:
            out_text += "<span"
            if "count" in pointer and pointer["count"] < max_count:
                color = scale(math.log(pointer["count"])).hexcode
                out_text += f" style='background: {color}'"
                out_text += f" title='{pointer['count']}/{max_count}'"
            out_text += ">" + buffer + "</span>"

            buffer = ""
            pointer = trie
            out_text += c
        else:
            buffer += c
            pointer = pointer[c]
    return DangerouslySetInnerHTML("<pre align='left' style='overflow-x: scroll; width: 45vw'>" + out_text + "</pre>")


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
            cmp += [diff_view(study, notation, from_slug, to_slug)]
        elif from_slug != "":
            _, from_tokens_n, from_tokens_nunique = get_token_info(study, notation, from_slug)
            cmp = header_and_image(study, notation, from_slug, from_tokens_n, from_tokens_nunique)
            cmp += [single_view(study, notation, from_slug)]

    except Exception as e:
        print(repr(e))

    return (cmp, net, fig)


# if/when there is a PNG notation, just inline the imgext dict in the string or in the ID dict
app.clientside_callback(
    """
    function(ignore) {
        trig = window.dash_clientside.callback_context.triggered
        pt = trig.length > 0 && trig[0].value &&  trig[0].value["points"][0]
        if(!pt){
            return [false, null, null, null];
        }
        pieces = window.location.hash.split("/");
        study=pieces[1];
        notation=pieces[2]
        if(trig[0].prop_id.includes('2')) {
            notation=pieces[5]
        }
        slug = pt["hovertext"]
        return [true,
                pt["bbox"],
                "/assets/results/"+study+"/"+notation+"/img/"+slug+".svg",
                slug]
    }
    """,
    Output("tooltip", "show"),
    Output("tooltip", "bbox"),
    Output("tt_img", "src"),
    Output("tt_name", "children"),
    Input(dict(type="figure", suffix=ALL), "hoverData"),
)


if __name__ == "__main__":
    app.run_server(debug=True)
