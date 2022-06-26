import re
from dash import Dash, html, dcc, Input, Output, State, callback_context
import random
import json
import pandas as pd
import numpy as np
from sklearn.manifold import MDS
import dash_cytoscape as cyto
from collections import Counter
from dash_extensions import EventListener
from notascope_components import DashDiff
import sys

cost_type = sys.argv[1]


print("start", np.random.randint(100))
np.random.seed(1)


costs_df = pd.read_csv(
    f"results/{cost_type}_costs.csv",
    names=["study", "system", "from_slug", "to_slug", "cost"],
)
tokens_df = pd.read_csv(
    "results/tokens.tsv",
    names=["study", "system", "spec", "token"],
    delimiter="\t",
)


def precompute():
    results = dict()
    for (study, system), df in costs_df.groupby(["study", "system"]):
        square = df.pivot_table(index="from_slug", columns="to_slug", values="cost").fillna(0)
        order = list(square.index)
        mds = MDS(n_components=2, dissimilarity="precomputed")
        embedding = mds.fit_transform((square.values + square.values.T) / 2)
        emb_min = embedding.min()
        emb_max = embedding.max()
        emb_span = emb_max - emb_min
        emb_max += emb_span / 2
        emb_min -= emb_span / 2
        emb_df = pd.DataFrame(embedding, index=order, columns=["x", "y"])

        network_elements = []
        for i, row in emb_df.iterrows():
            network_elements.append(
                {
                    "data": {
                        "id": i,
                        "label": i,
                        "url": f"/assets/results/{study}/{system}/svg/{i}.svg",
                    },
                    "position": {c: row[c] * 1000 / emb_span for c in ["x", "y"]},
                    "classes": "",
                }
            )

        square = square.values
        n = len(square)
        result = np.zeros((n, n))
        for i in range(n):
            for j in range(n):
                if i == j:
                    continue
                has_k = False
                direct = square[i, j]
                for k in range(n):
                    if k == i or k == j:
                        continue
                    via_k = square[i, k] + square[k, j]
                    if (via_k - direct) / direct <= 0:
                        has_k = True
                        break
                if not has_k:
                    result[i, j] = direct
        for i in range(n):
            for j in range(n):
                if i == j:  # no self edges
                    continue
                if result[i, j] == 0:  # no zero edges
                    continue
                if result[j, i] == 0:  # no edge without other direction
                    continue
                if result[i, j] > result[j, i] or (result[i, j] == result[j, i] and i > j):  # only one bidir edge
                    network_elements.append(
                        {
                            "data": {
                                "source": order[i],
                                "target": order[j],
                                "id": order[i] + "__" + order[j],
                                "length": result[i, j],
                            },
                            "classes": (" bidir" if result[i, j] == result[j, i] else ""),
                        }
                    )

        if study not in results:
            results[study] = dict()
        results[study][system] = dict(
            slugs=df.from_slug.unique(),
            tokens=tokens_df.query("study==@study and system==@system")["token"].nunique(),
            network_elements=network_elements,
        )
    return results


results = precompute()
default_study = "tiny"


def default_system(study):
    return list(results[study].keys())[0]


app = Dash(__name__, title="NotaScope", suppress_callback_exceptions=True)


def cytoscape(id, elements):
    return cyto.Cytoscape(
        id=id,
        className="network",
        layout={"name": "preset"},
        minZoom=0.3,
        maxZoom=2,
        elements=elements,
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
                    "line-color": "grey",
                    "curve-style": "bezier",
                    "target-arrow-color": "grey",
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
                    "source-arrow-color": "grey",
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
                "style": {
                    "line-style": "dashed",
                },
            },
        ],
    )


def parse_hashpath(hashpath):
    m = re.match(r"#/(.*)/(.*)/(.*)/(.*)/(.*)", hashpath)
    study = system = system2 = from_slug = to_slug = ""
    if m:
        study = m.group(1)
        system = m.group(2)
        system2 = m.group(3)
        from_slug = m.group(4)
        to_slug = m.group(5)
    return sanitize_state(study, system, system2, from_slug, to_slug)


def sanitize_state(study, system, system2, from_slug, to_slug):
    if study not in results:
        study = default_study
    study_res = results[study]
    slugs = set()
    if system in study_res:
        for s in study_res[system]["slugs"]:
            slugs.add(s)
    else:
        system = default_system(study)

    if system2 in study_res:
        for s in study_res[system2]["slugs"]:
            slugs.add(s)
    else:
        system2 = ""

    if from_slug not in slugs:
        from_slug = to_slug = ""
    elif to_slug not in slugs:
        to_slug = from_slug

    return study, system, system2, from_slug, to_slug


app.layout = html.Div(
    [
        html.Div(id="content"),
        dcc.Location(id="location"),
        EventListener(
            id="event_listener",
            events=[
                {"event": "keydown", "props": ["shiftKey"]},
                {"event": "keyup", "props": ["shiftKey"]},
            ],
        ),
    ]
)


@app.callback(
    Output("content", "children"),
    Input("location", "hash"),
)
def make_content(hashpath):
    study, system, system2, from_slug, to_slug = parse_hashpath(hashpath)
    cmp, net = make_comparison(study, system, from_slug, to_slug)
    if system2:
        style = dict()
        style2 = dict(gridColumnStart=2, visibility="visible")
        cmp2, net2 = make_comparison(study, system2, from_slug, to_slug)
    else:
        style = dict(gridRowStart=2)
        style2 = dict(visibility="hidden", gridRowStart=3)
        cmp2, net2 = None, []

    systems = [dict(label=f"{s} ({results[study][s]['tokens']})", value=s) for s in results[study]]

    return html.Div(
        className="wrapper",
        children=[
            html.Div(
                [
                    dcc.Dropdown(
                        id="study",
                        value=study,
                        options=[s for s in results],
                        clearable=False,
                        className="dropdown",
                    ),
                ],
                style=dict(position="absolute", left=10, top=10),
            ),
            html.Div(
                [
                    dcc.Dropdown(
                        id="system",
                        value=system,
                        options=systems,
                        clearable=False,
                        className="dropdown",
                    ),
                ]
            ),
            html.Div(
                [
                    dcc.Dropdown(
                        id="system2",
                        value=system2,
                        options=systems,
                        clearable=True,
                        className="dropdown",
                    ),
                ]
            ),
            html.Div([cytoscape("network", net)], style=style),
            html.Div([cytoscape("network2", net2)], style=style2),
            html.Div(cmp, className="comparison"),
            html.Div(cmp2, className="comparison"),
            dcc.Store(id="selection", data=[from_slug, to_slug]),
        ],
    )


@app.callback(
    Output("location", "hash"),
    Output("network", "tapNodeData"),
    Output("network", "tapEdgeData"),
    Output("network2", "tapNodeData"),
    Output("network2", "tapEdgeData"),
    Input("selection", "data"),
    Input("study", "value"),
    Input("system", "value"),
    Input("system2", "value"),
    Input("network", "tapNodeData"),
    Input("network", "tapEdgeData"),
    Input("network2", "tapNodeData"),
    Input("network2", "tapEdgeData"),
    State("event_listener", "event"),
)
def update_hashpath(selection, study, system, system2, node_data, edge_data, node_data2, edge_data2, event):
    shift_down = bool((dict(shiftKey=False) if not event else event)["shiftKey"])
    ctx = callback_context
    from_slug, to_slug = selection
    if ctx.triggered:
        click_system = ctx.triggered[0]["prop_id"].split(".")[0]
        click_type = ctx.triggered[0]["prop_id"].split(".")[1]

        if click_type == "tapNodeData":
            if click_system == "network":
                to_slug = node_data["id"]
                if not shift_down:
                    from_slug = to_slug
            if click_system == "network2":
                to_slug = node_data2["id"]
                if not shift_down:
                    from_slug = to_slug
            edge_data = None
            edge_data2 = None
        if click_type == "tapEdgeData":
            if click_system == "network":
                from_slug = edge_data["source"]
                to_slug = edge_data["target"]
            if click_system == "network2":
                from_slug = edge_data2["source"]
                to_slug = edge_data2["target"]
            node_data = None
            node_data2 = None
    study, system, system2, from_slug, to_slug = sanitize_state(study, system, system2, from_slug, to_slug)
    hashpath = f"#/{study}/{system}/{system2 or ''}/{from_slug}/{to_slug}"
    return hashpath, node_data, edge_data, node_data2, edge_data2


def iframe(study, system, url):
    return html.Iframe(
        src=f"/assets/results/{study}/{system}/{url}?{random.random()}",
        style=dict(width="100%", height="300px"),
    )


def single(study, system, slug, tokens_n, tokens_nunique):
    return [
        html.H3(slug),
        html.P(f"{tokens_n} tokens, {tokens_nunique} uniques"),
        html.Img(
            src=f"/assets/results/{study}/{system}/svg/{slug}.svg",
            style=dict(verticalAlign="middle", maxHeight="250px", maxWidth="20vw"),
        ),
    ]


def code(study, system, from_slug, to_slug):
    with open(f"results/{study}/{system}/source/{from_slug}.txt", "r") as f:
        from_code = f.read()
    with open(f"results/{study}/{system}/source/{to_slug}.txt", "r") as f:
        to_code = f.read()
    return html.Div(
        [html.Div([DashDiff(oldCode=from_code, newCode=to_code)], style=dict(border="none"))],
        style=dict(textAlign="left", height="300px", overflow="scroll", border="1px solid grey"),
    )


def make_comparison(study, system, from_slug, to_slug):
    cmp = None
    system_results = results[study][system]
    net = json.loads(json.dumps(system_results["network_elements"]))
    try:
        filter_prefix = "study==@study and system==@system"
        from_tokens_df = tokens_df.query(filter_prefix + " and spec==@from_slug")
        from_tokens_n = len(from_tokens_df)
        from_tokens_nunique = from_tokens_df["token"].nunique()
        if from_slug != to_slug:
            to_tokens_df = tokens_df.query(filter_prefix + " and spec==@to_slug")
            to_tokens_n = len(to_tokens_df)
            to_tokens_nunique = to_tokens_df["token"].nunique()
            cost = costs_df.query(filter_prefix + " and from_slug==@from_slug and to_slug==@to_slug")["cost"].values[0]
            rev_cost = costs_df.query(filter_prefix + " and from_slug==@to_slug and to_slug==@from_slug")["cost"].values[0]

            shared_tokens = list((Counter(from_tokens_df["token"].values) & Counter(to_tokens_df["token"].values)).elements())
            shared_uniques = set(from_tokens_df["token"]) & set(to_tokens_df["token"])

            any_elem_found = False
            for source, dest in [[from_slug, to_slug], [to_slug, from_slug]]:
                edge_id = source + "__" + dest
                elem_found = False
                for elem in net:
                    if elem["data"]["id"] == edge_id:
                        elem["classes"] += " selected"
                        elem_found = True
                        any_elem_found = True

                if (not elem_found and cost != rev_cost) or (dest == from_slug and not any_elem_found and cost == rev_cost):
                    net.append(
                        {
                            "data": {
                                "source": source,
                                "target": dest,
                                "id": edge_id,
                                "length": cost if source == from_slug else rev_cost,
                            },
                            "classes": "selected inserted" + (" bidir" if cost == rev_cost else ""),
                        }
                    )

            cmp = [
                html.Table(
                    [
                        html.Tr(
                            [
                                html.Td(
                                    single(study, system, from_slug, from_tokens_n, from_tokens_nunique),
                                    style=dict(verticalAlign="top"),
                                ),
                                html.Td(
                                    [
                                        html.P(
                                            [
                                                "tokens",
                                                html.Br(),
                                                f"{from_tokens_n - len(shared_tokens)} ⬌ {to_tokens_n - len(shared_tokens)}",
                                            ]
                                        ),
                                        html.P(
                                            [
                                                "uniques",
                                                html.Br(),
                                                f"{from_tokens_nunique - len(shared_uniques)} ⬌ {to_tokens_nunique - len(shared_uniques)}",
                                            ]
                                        ),
                                        html.P(["tree edit", html.Br(), f"{rev_cost} ⬌ {cost}"]),
                                    ]
                                ),
                                html.Td(
                                    single(study, system, to_slug, to_tokens_n, to_tokens_nunique),
                                    style=dict(verticalAlign="top"),
                                ),
                            ]
                        )
                    ],
                    style=dict(width="100%"),
                ),
                code(study, system, from_slug, to_slug),
            ]
        elif from_slug != "":
            cmp = single(study, system, from_slug, from_tokens_n, from_tokens_nunique)
            cmp += [code(study, system, from_slug, from_slug)]

            for elem in net:
                if elem["data"]["id"] == from_slug:
                    elem["classes"] += " selected"

    except Exception as e:
        print(repr(e))

    return (cmp, net)


if __name__ == "__main__":
    app.run_server(debug=True)
