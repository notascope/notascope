from dash import dcc, html
from .tokens import load_tokens
from .utils import load_registry
import plotly.express as px
import plotly.graph_objects as go


def thumbnails(gallery, distance, vis):
    registry = load_registry()
    notations = list(registry[gallery].keys())
    rows = []
    for slug in registry[gallery][notations[0]]["slugs"]:
        cells = []
        for notation in notations:
            cells.append(
                html.Td(
                    html.Img(
                        id=dict(type="thumbnail", notation=notation, slug=slug),
                        src=f"/assets/results/{gallery}/{notation}/img/{slug}.svg",
                        className="zoomable",
                    )
                )
            )
        rows.append(
            html.Tr([html.Th(slug)] + cells + [html.Th(slug, style=dict(opacity=0))])
        )
    return html.Table(
        [html.Tr([html.Th()] + [html.Th(n) for n in notations])] + rows,
        style=dict(margin="0 auto"),
        className="thumbnails",
    )


def tokens(gallery, distance, vis):
    tokens_df = load_tokens()

    gallery = "movies"

    df = (
        tokens_df.query(f"gallery == '{gallery}'")
        .groupby(["token", "notation"])["slug"]
        .nunique()
        .reset_index()
    )
    fig = px.ecdf(
        df,
        x="slug",
        color="notation",
        hover_name="token",
        ecdfnorm=None,
        height=600,
        markers=True,
        lines=True,
        # ecdfmode="complementary",
        labels=dict(slug="token frequency"),
    )
    fig.update_traces(line_shape="linear", marker_size=5, line_width=1)
    fig.update_yaxes(title_text="token frequency rank")
    fig.update_layout(scattermode="group")
    return fig


multi_vis_map = {
    "thumbnails": thumbnails,
    "tokens": tokens,
}
multi_vis_types = list(multi_vis_map)


def wrap_multi_vis(gallery, distance, vis):
    out = multi_vis_map[vis](gallery, distance, vis)
    if isinstance(out, go.Figure):
        return dcc.Graph(
            id=dict(type="figure", suffix="multi", seq="1"),
            figure=out,
            style=dict(width=str(out.layout.width or "800") + "px", margin="0 auto"),
            clear_on_unhover=True,
        )
    else:
        return out
