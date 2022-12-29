# builtins
from functools import cache
from collections import defaultdict, Counter
from datetime import datetime
from operator import itemgetter
from urllib.parse import urlencode, parse_qsl

# plotly
from dash import Dash, html, dcc, Input, Output, State, callback_context, ALL
from dash_extensions import EventListener
import dash_cytoscape as cyto
from notascope_components import DashDiff

from src import vis_types, ext, get_distance, distance_types, get_vis, merged_distances, load_tokens, load_registry

import plotly.graph_objects as go
import plotly.express as px
from dash_dangerously_set_inner_html import DangerouslySetInnerHTML
import spectra
import math

print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
registry = load_registry()
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
    return sanitize_state(parse_qsl(hashpath.lstrip("#")))


def make_hashpath(values):
    return "#" + urlencode(sanitize_state(values))


def sanitize_state(hashpath_values):
    state = defaultdict(str, hashpath_values)

    if state["vis"] not in vis_types:
        state["vis"] = vis_types[0]

    if state["vis2"] not in vis_types:
        state["vis2"] = ""

    if state["distance"] not in distance_types:
        state["distance"] = distance_types[0]

    if state["distance2"] not in distance_types:
        state["distance2"] = ""

    if state["study"] not in registry:
        state["study"] = "tiny"

    study_res = registry[state["study"]]
    slugs = set()
    if state["notation"] in study_res:
        for s in study_res[state["notation"]]["slugs"]:
            slugs.add(s)
    else:
        state["notation"] = list(registry[state["study"]].keys())[0]

    if state["notation2"] in study_res:
        for s in study_res[state["notation2"]]["slugs"]:
            slugs.add(s)
    else:
        state["notation2"] = ""

    if state["notation2"] == "":
        state["vis2"] = ""
        state["distance2"] = ""

    if state["from_slug"] not in slugs:
        state["from_slug"] = state["to_slug"] = ""
    elif state["to_slug"] not in slugs:
        state["to_slug"] = state["from_slug"]

    return state


@app.callback(
    Output("location", "hash"),
    Output(dict(type="network", suffix=ALL, seq=ALL), "tapNodeData"),
    Output(dict(type="network", suffix=ALL, seq=ALL), "tapEdgeData"),
    Input("selection", "data"),
    Input(dict(type="dropdown", id=ALL), "value"),
    Input(dict(type="network", suffix=ALL, seq=ALL), "tapNodeData"),
    Input(dict(type="network", suffix=ALL, seq=ALL), "tapEdgeData"),
    Input(dict(type="figure", suffix=ALL, seq=ALL), "clickData"),
    State("event_listener", "event"),
)
def update_hashpath(selection, dropdowns, node_data, edge_data, _, event):
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
            if "customdata" in data["points"][0]:
                to_slug = data["points"][0]["customdata"]
                if len(to_slug) == 1:
                    to_slug = to_slug[0]
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

    hashpath_values = {"from_slug": from_slug, "to_slug": to_slug}
    for input in callback_context.inputs_list[1]:
        try:
            hashpath_values[input["id"]["id"]] = input["value"]
        except Exception as e:
            print(repr(e))
    hashpath = make_hashpath(hashpath_values)
    return hashpath, node_data, edge_data


@app.callback(
    Output("content", "children"),
    Input("location", "hash"),
)
def update_content(hashpath):
    study, notation, distance, vis, notation2, distance2_in, vis2_in, from_slug, to_slug = itemgetter(
        "study", "notation", "distance", "vis", "notation2", "distance2", "vis2", "from_slug", "to_slug"
    )(parse_hashpath(hashpath))
    distance2 = distance2_in or distance
    vis2 = vis2_in or vis

    notations = [s for s in registry[study]]

    blocks = [
        html.Div(
            [
                html.Div(
                    [
                        html.Span("gallery"),
                        dcc.Dropdown(
                            id=dict(id="study", type="dropdown"),
                            value=study,
                            options=[s for s in registry],
                            clearable=False,
                            style=dict(width="100px"),
                        ),
                    ],
                    style=dict(display="inline-block"),
                ),
                html.Div(
                    [
                        html.Span("notation"),
                        dcc.Dropdown(
                            id=dict(id="notation", type="dropdown"), value=notation, options=notations, clearable=False, style=dict(width="150px")
                        ),
                    ],
                    style=dict(display="inline-block"),
                ),
                html.Div(
                    [
                        html.Span("visualization"),
                        dcc.Dropdown(id=dict(id="vis", type="dropdown"), value=vis, options=vis_types, clearable=False, style=dict(width="150px")),
                    ],
                    style=dict(display="inline-block"),
                ),
                html.Div(
                    [
                        html.Span("distance"),
                        dcc.Dropdown(
                            id=dict(id="distance", type="dropdown"),
                            value=distance,
                            options=distance_types,
                            clearable=False,
                            style=dict(width="100px"),
                        ),
                    ],
                    style=dict(display="inline-block"),
                ),
            ],
            style=dict(margin="0 auto"),
        ),
        html.Div(
            [
                html.Div(
                    [
                        html.Span("notation"),
                        dcc.Dropdown(
                            id=dict(id="notation2", type="dropdown"),
                            value=notation2,
                            options=notations,
                            clearable=True,
                            style=dict(width="150px"),
                            placeholder="Compare...",
                        ),
                    ],
                    style=dict(display="inline-block"),
                ),
                html.Div(
                    [
                        html.Span("visualization"),
                        dcc.Dropdown(
                            id=dict(id="vis2", type="dropdown"),
                            value=vis2_in,
                            options=vis_types,
                            clearable=True,
                            style=dict(width="150px"),
                            placeholder=vis2,
                        ),
                    ],
                    style=dict(display="inline-block" if notation2 else "none"),
                ),
                html.Div(
                    [
                        html.Span("distance"),
                        dcc.Dropdown(
                            id=dict(id="distance2", type="dropdown"),
                            value=distance2_in,
                            options=distance_types,
                            clearable=True,
                            style=dict(width="100px"),
                            placeholder=distance2,
                        ),
                    ],
                    style=dict(display="inline-block" if notation2 else "none"),
                ),
            ],
            style=dict(margin="0 auto"),
        ),
        dcc.Store(id="selection", data=[from_slug, to_slug]),
    ]

    if notation2 and ((notation != notation2 and distance == distance2) or (notation == notation2 and distance != distance2)):
        blocks.append(
            html.Div(
                html.Details(
                    [
                        html.Summary("cross-notation"),
                        dcc.Graph(
                            id=dict(type="figure", suffix="cross", seq="1"),
                            figure=cross_notation_figure(study, notation, distance, notation2, distance2, from_slug, to_slug),
                            style=dict(width="500px", margin="0 auto"),
                            clear_on_unhover=True,
                        ),
                    ],
                    open=True,
                    style=dict(width="800px", margin="0 auto"),
                ),
                style=dict(gridColumn="1/3"),
            )
        )

    blocks.append(
        html.Div(
            html.Details(
                [html.Summary(notation + " " + vis)] + wrap_vis(study, notation, distance, vis, from_slug, to_slug, "1"),
                open=True,
            )
        ),
    )

    if notation2:
        blocks.append(
            html.Div(
                html.Details(
                    [html.Summary(notation2 + " " + vis2)] + wrap_vis(study, notation2, distance2, vis2, from_slug, to_slug, "2"),
                    open=True,
                )
            )
        )

    blocks.append(details_view(study, notation, distance, from_slug, to_slug))

    if notation2 and (distance != distance2 or notation != notation2):
        blocks.append(details_view(study, notation2, distance2, from_slug, to_slug))

    return html.Div(className="wrapper", children=blocks)


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
                    customdata=merged["from_slug"],
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
                customdata=merged.query("selected")["from_slug"],
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


def wrap_vis(study, notation, distance, vis, from_slug, to_slug, suffix):
    vis_list = []
    for i, vis in enumerate(get_vis(study, notation, distance, vis, from_slug, to_slug)):
        if isinstance(vis, go.Figure):
            vis_list.append(figure(dict(type="figure", suffix=suffix, seq=str(i)), vis))
        else:
            vis_list.append(cytoscape(dict(type="network", suffix=suffix, seq=str(i)), vis))
    return vis_list


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
        style=dict(marginTop="20px", textAlign="left", height="300px", maxWidth="48vw", border="1px solid grey"),
    )


@cache
def build_trie(study, notation):
    tokens_df = load_tokens()
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
    return DangerouslySetInnerHTML("<pre align='left' style='width: 45vw'>" + out_text + "</pre>")


def get_token_info(study, notation, slug):
    tokens_df = load_tokens()
    df = tokens_df.query(f"study=='{study}' and notation=='{notation}' and slug=='{slug}'")["token"]
    return df.values, len(df), df.nunique()


def details_view(study, notation, distance, from_slug, to_slug):
    cmp = None
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
            cmp = header_and_image(study, notation, from_slug, from_tokens_n, from_tokens_nunique)
            cmp += [single_view(study, notation, from_slug)]

    except Exception as e:
        print(repr(e))

    return html.Div(cmp, className="comparison")


# if/when there is a PNG notation, just inline the imgext dict in the string or in the ID dict
app.clientside_callback(
    """
    function(ignore) {
        trig = window.dash_clientside.callback_context.triggered
        pt = trig.length > 0 && trig[0].value &&  trig[0].value["points"][0]
        if(!pt || !pt["customdata"]){
            return [false, null, null, null];
        }
        qs = new URLSearchParams(window.location.hash.replace(/^#/, ""));
        study=qs.get('study');
        notation=qs.get('notation')
        if(trig[0].prop_id.includes('2')) {
            notation=qs.get('notation2') // pack this into the id?
        }
        slug = pt["customdata"]
        if(slug.length == 1) {
            slug = slug[0]
        }
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
    Input(dict(type="figure", suffix=ALL, seq=ALL), "hoverData"),
)


if __name__ == "__main__":
    app.run_server(debug=True)
