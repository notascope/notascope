from dash import dcc, html
from .utils import (
    gallery_specs,
    pretty_source,
    vscode_link,
    md_lang,
    img_path,
    gallery_notations,
    debug_mode,
)
from itertools import cycle


def code_cell(gallery, notation, spec):
    return html.Td(
        [
            dcc.Markdown(
                "```"
                + md_lang(gallery, notation)
                + "\n"
                + pretty_source(gallery, notation, spec)
                + "```"
            ),
            html.A(
                "✎",
                href=vscode_link(gallery, notation, spec),
                className="editlink",
            )
            if debug_mode()
            else "",
        ],
        style=dict(
            verticalAlign="top",
            position="relative",
            textAlign="left",
            borderBottom="1px solid lightgrey",
        ),
    )


def thumbnail_cell(gallery, notation, spec, mode):
    return html.Td(
        [
            html.P(
                notation if mode == "n" else spec,
                id=dict(
                    type="thumbnail",
                    notation=notation if mode == "n" else "clear",
                    spec="clear" if mode == "n" else spec,
                    vis="",
                ),
                style=dict(margin=0, cursor="pointer"),
            ),
            html.Img(
                src=img_path(gallery, notation, spec),
                id=dict(
                    type="thumbnail",
                    notation=notation,
                    spec=spec,
                    vis="thumbnails",
                ),
                className="bigthumb",
            ),
        ],
        style=dict(verticalAlign="top", borderBottom="1px solid lightgrey"),
    )


def _source_table(gallery, notation_spec_generator, mode):
    return [
        html.Table(
            [
                html.Tr(
                    [
                        thumbnail_cell(gallery, n, spec, mode),
                        code_cell(gallery, n, spec),
                        code_cell(gallery, n2, spec) if n2 else None,
                        thumbnail_cell(gallery, n2, spec, mode) if n2 else None,
                    ]
                )
                for n, n2, spec in notation_spec_generator
            ],
            style=dict(margin="0 auto"),
            className="thumbnails",
        )
    ]


def thumbnails_for_spec(gallery, distance, from_spec):
    return _source_table(
        gallery, zip(gallery_notations(gallery), cycle([None]), cycle([from_spec])), "n"
    )


def thumbnails_for_notation(gallery, distance, notation, notation2=None):
    return _source_table(
        gallery, zip(cycle([notation]), cycle([notation2]), gallery_specs(gallery)), "s"
    )
