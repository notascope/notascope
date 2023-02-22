from dash import html
from notascope_components import DashDiff
from dash_dangerously_set_inner_html import DangerouslySetInnerHTML
import spectra
import math
from functools import cache
from collections import Counter
from .utils import img_path, pretty_source
from .distances import get_distance, distances_df
from .tokens import load_tokens


def header_and_image(gallery, notation, distance, spec):

    remotenesses = (
        distances_df(gallery=gallery, notation=notation)
        .groupby(["from_spec"])[distance]
        .median()
        .reset_index()
    )
    remotenesses["rank"] = remotenesses[distance].rank()
    spec_stats = remotenesses.query(f"from_spec == '{spec}'").iloc[0]
    return [
        html.H3(spec),
        html.P(
            f"remoteness: {spec_stats[distance]} ({int(spec_stats['rank'])}/{len(remotenesses)})"
        ),
        html.Img(
            src=img_path(gallery, notation, spec),
            style=dict(verticalAlign="middle", maxHeight="200px", maxWidth="20vw"),
            className="zoomable",
        ),
    ]


def diff_view(gallery, notation, from_spec, to_spec):
    from_code = pretty_source(gallery, notation, from_spec)
    if from_spec == to_spec:
        to_code = from_code
    else:
        to_code = pretty_source(gallery, notation, to_spec)
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
            maxWidth="48vw",
            border="1px solid grey",
        ),
    )


@cache
def build_trie(gallery, notation):
    tokens_df = load_tokens()
    filtered = (
        tokens_df.query(f"gallery=='{gallery}' and notation=='{notation}'")
        .groupby("token")["spec"]
        .nunique()
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
    trie, max_count = build_trie(gallery, notation)
    text = pretty_source(gallery, notation, spec)

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
                out_text += f" title='{buffer}: {pointer['count']}/{max_count}'"
            out_text += ">" + buffer + "</span>"

            pointer = trie
            buffer = ""
            if c in pointer:
                buffer += c
                pointer = pointer[c]
            else:
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
                header_and_image(gallery, notation, distance, from_spec),
                style=dict(verticalAlign="top"),
            )
            td2 = html.Td(
                [
                    "distance",
                    html.Br(),
                    f"(2/40) {to_from_distance} ⬌ {from_to_distance} (5/40)",
                ]
                + [html.Br(), html.Br()]
                + [
                    "tokens",
                    html.Br(),
                    f"({from_tokens_n}) {from_tokens_n - len(shared_tokens)} ⬌ {to_tokens_n - len(shared_tokens)} ({to_tokens_n})",
                ]
                + [html.Br(), html.Br()]
                + [
                    "uniques",
                    html.Br(),
                    f"({from_tokens_nunique}) {from_tokens_nunique - len(shared_uniques)} ⬌ {to_tokens_nunique - len(shared_uniques)} ({to_tokens_nunique})",
                ]
            )
            td3 = html.Td(
                header_and_image(gallery, notation, distance, to_spec),
                style=dict(verticalAlign="top"),
            )
            cmp = [
                html.Table(
                    [html.Tr([td1, td2, td3])], style=dict(width="100%", height="300px")
                )
            ]
            cmp += [diff_view(gallery, notation, from_spec, to_spec)]
        elif from_spec != "":
            cmp = header_and_image(gallery, notation, distance, from_spec)
            cmp += [single_view(gallery, notation, from_spec)]

    except Exception as e:
        print(repr(e))

    return html.Div(cmp, className="comparison")
