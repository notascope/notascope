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


def _source_table(gallery, notation_spec_generator):
    return [
        html.Table(
            [
                html.Tr(
                    [
                        html.Td(
                            [
                                html.P(notation, style=dict(margin=0)),
                                html.Img(
                                    src=img_path(gallery, notation, spec),
                                    id=dict(
                                        type="thumbnail", notation=notation, spec=spec
                                    ),
                                    className="bigthumb",
                                ),
                            ],
                            style=dict(
                                verticalAlign="top", borderBottom="1px solid lightgrey"
                            ),
                        ),
                        html.Td(
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
                        ),
                    ]
                )
                for notation, spec in notation_spec_generator
            ],
            style=dict(margin="0 auto"),
            className="thumbnails",
        )
    ]


def thumbnails_for_spec(gallery, distance, from_spec):
    return _source_table(gallery, zip(gallery_notations(gallery), cycle([from_spec])))


def thumbnails_for_notation(gallery, distance, notation):
    return _source_table(gallery, zip(cycle([notation]), gallery_specs(gallery)))
