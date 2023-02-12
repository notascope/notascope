from dash import html
from notascope_components import DashDiff
from dash_dangerously_set_inner_html import DangerouslySetInnerHTML
import spectra
import math
from functools import cache
from collections import Counter
from .utils import ext
from .distances import get_distance
from .tokens import load_tokens


def header_and_image(gallery, notation, spec, tokens_n, tokens_nunique):
    imgext = ext(gallery, notation, "img")

    return [
        html.H3(spec),
        html.P(f"{tokens_n} tokens, {tokens_nunique} uniques"),
        html.Img(
            src=f"/assets/results/{gallery}/{notation}/img/{spec}.{imgext}",
            style=dict(verticalAlign="middle", maxHeight="200px", maxWidth="20vw"),
            className="zoomable",
        ),
    ]


def diff_view(gallery, notation, from_spec, to_spec):
    srcext = ext(gallery, notation, "source")
    with open(f"results/{gallery}/{notation}/pretty/{from_spec}.{srcext}", "r") as f:
        from_code = f.read()
    if from_spec == to_spec:
        to_code = from_code
    else:
        with open(f"results/{gallery}/{notation}/pretty/{to_spec}.{srcext}", "r") as f:
            to_code = f.read()
    return html.Div(
        [
            html.Div(
                [DashDiff(oldCode=from_code, newCode=to_code)],
                style=dict(border="none"),
            )
        ],
        style=dict(
            marginTop="20px",
            textAlign="left",
            height="300px",
            maxWidth="48vw",
            border="1px solid grey",
        ),
    )


@cache
def build_trie(gallery, notation):
    tokens_df = load_tokens()
    filtered = (
        tokens_df.query(f"gallery=='{gallery}' and notation=='{notation}'")
        .groupby("token")
        .nunique("spec")
    )
    max_count = filtered["spec"].max()
    trie = dict()
    for token, count in filtered["spec"].items():
        pointer = trie
        for c in token:
            if c not in pointer:
                pointer[c] = dict()
            pointer = pointer[c]
        pointer["count"] = count
    return trie, max_count


def single_view(gallery, notation, spec):
    srcext = ext(gallery, notation, "source")
    trie, max_count = build_trie(gallery, notation)
    with open(f"results/{gallery}/{notation}/pretty/{spec}.{srcext}", "r") as f:
        text = f.read()

    scale = spectra.scale([spectra.html("#2FF"), spectra.html("#FFF")]).domain(
        [math.log(1), math.log(max_count - 1)]
    )

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
    return html.Div(
        DangerouslySetInnerHTML(
            "<pre align='left' style='width: 45vw'>" + out_text + "</pre>"
        ),
        className="singleWrapper",
    )


def get_token_info(gallery, notation, spec):
    tokens_df = load_tokens()
    df = tokens_df.query(
        f"gallery=='{gallery}' and notation=='{notation}' and spec=='{spec}'"
    )["token"]
    return df.values, len(df), df.nunique()


def details_view(gallery, notation, distance, from_spec, to_spec):
    cmp = None
    try:
        from_tokens, from_tokens_n, from_tokens_nunique = get_token_info(
            gallery, notation, from_spec
        )
        if from_spec != to_spec:

            to_tokens, to_tokens_n, to_tokens_nunique = get_token_info(
                gallery, notation, to_spec
            )
            from_to_distance = get_distance(
                gallery, notation, distance, from_spec, to_spec
            )
            to_from_distance = get_distance(
                gallery, notation, distance, to_spec, from_spec
            )

            shared_tokens = list((Counter(from_tokens) & Counter(to_tokens)).elements())
            shared_uniques = set(from_tokens) & set(to_tokens)
            td1 = html.Td(
                header_and_image(
                    gallery, notation, from_spec, from_tokens_n, from_tokens_nunique
                ),
                style=dict(verticalAlign="top"),
            )
            td2 = html.Td(
                ["tokens", html.Br()]
                + [
                    f"{from_tokens_n - len(shared_tokens)} ⬌ {to_tokens_n - len(shared_tokens)}"
                ]
                + [html.Br(), html.Br(), "uniques", html.Br()]
                + [
                    f"{from_tokens_nunique - len(shared_uniques)} ⬌ {to_tokens_nunique - len(shared_uniques)}"
                ]
                + [
                    html.Br(),
                    html.Br(),
                    "tree edit",
                    html.Br(),
                    f"{to_from_distance} ⬌ {from_to_distance}",
                ]
            )
            td3 = html.Td(
                header_and_image(
                    gallery, notation, to_spec, to_tokens_n, to_tokens_nunique
                ),
                style=dict(verticalAlign="top"),
            )
            cmp = [
                html.Table(
                    [html.Tr([td1, td2, td3])], style=dict(width="100%", height="300px")
                )
            ]
            cmp += [diff_view(gallery, notation, from_spec, to_spec)]
        elif from_spec != "":
            cmp = header_and_image(
                gallery, notation, from_spec, from_tokens_n, from_tokens_nunique
            )
            cmp += [single_view(gallery, notation, from_spec)]

    except Exception as e:
        print(repr(e))

    return html.Div(cmp, className="comparison")
