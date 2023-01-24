from dash import dcc, html
from .tokens import load_tokens
from .utils import load_registry
from .distances import distances_df
import plotly.express as px
import plotly.graph_objects as go
from sklearn.manifold import MDS
import numpy as np
import pandas as pd
from .distances import dmat_and_order


def embedding(gallery, distance, vis):
    registry = load_registry()
    notations = list(registry[gallery].keys())

    distances = np.zeros((len(notations), len(notations)))

    for i, n1 in enumerate(notations):
        for j, n2 in enumerate(notations):
            if i < j:
                dmat1, dmat_sym1, order1 = dmat_and_order(gallery, n1, distance)
                dmat2, dmat_sym2, order2 = dmat_and_order(gallery, n2, distance)

                d = np.linalg.norm(dmat1 - dmat2)
                distances[i, j] = d
                distances[j, i] = d

    embedding = MDS(
        n_components=2, dissimilarity="precomputed", normalized_stress="auto"
    ).fit_transform(distances)

    df = pd.DataFrame(embedding, index=notations).reset_index()

    fig = px.scatter(df, x=0, y=1, text="index", height=600, width=600)
    fig.update_traces(mode="text")
    return fig


def farness(gallery, distance, vis):
    registry = load_registry()
    notations = list(registry[gallery].keys())
    df = (
        distances_df()
        .query(f"gallery=='{gallery}'")
        .groupby(["notation", "from_slug"])[distance]
        .mean()
        .reset_index()
    )
    return px.ecdf(
        df,
        x=distance,
        color="notation",
        ecdfnorm=None,
        markers=True,
        category_orders=dict(notation=notations),
    ).update_traces(line_shape="linear", marker_size=5, line_width=1)


def distance(gallery, distance, vis):
    registry = load_registry()
    notations = list(registry[gallery].keys())
    df = distances_df().query(f"gallery=='{gallery}'")
    return px.ecdf(
        df,
        x=distance,
        color="notation",
        ecdfnorm=None,
        markers=True,
        category_orders=dict(notation=notations),
    ).update_traces(line_shape="linear", marker_size=5, line_width=1)


def thumbnails(gallery, distance, vis):
    registry = load_registry()
    notations = list(registry[gallery].keys())
    df = distances_df()
    roughly_sorted_slugs = (
        df.query(f"gallery=='{gallery}'")
        .groupby("to_slug")[distance]
        .mean()
        .reset_index()
        .sort_values(by=distance)
        .to_slug
    )
    rows = []
    for slug in roughly_sorted_slugs:
        cells = []
        for notation in notations:
            cells.append(
                html.Td(
                    html.Img(
                        id=dict(type="thumbnail", notation=notation, slug=slug),
                        src=f"/assets/results/{gallery}/{notation}/img/{slug}.svg",
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
    registry = load_registry()
    notations = list(registry[gallery].keys())
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
        category_orders=dict(notation=notations),
    )
    fig.update_traces(line_shape="linear", marker_size=5, line_width=1)
    fig.update_yaxes(title_text="token frequency rank")
    fig.update_layout(scattermode="group")
    return fig


multi_vis_map = {
    "thumbnails": thumbnails,
    "embedding": embedding,
    "tokens": tokens,
    "farness": farness,
    "distance": distance,
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
