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

    result = []

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
    result.append(fig)
    return result


def stats(gallery, distance, vis):
    registry = load_registry()
    notations = list(registry[gallery].keys())
    result = []

    # Farness
    df = (
        distances_df(gallery=gallery)
        .groupby(["notation", "from_slug"])[distance]
        .median()
        .reset_index()
    )

    result.append(
        px.violin(
            df,
            x=distance,
            y="notation",
            color="notation",
            height=600,
            points="all",
            category_orders=dict(notation=notations),
            hover_data=["from_slug"],
        )
        .update_traces(
            hoveron="points",
            pointpos=0,
            scalemode="count",
            hoverinfo="none",
            hovertemplate="",
        )
        .update_layout(violingroupgap=0, violingap=0.05)
    )

    df = (
        distances_df(gallery=gallery)
        .groupby(["from_slug", "notation"])["from_length"]
        .min()
        .reset_index()
    )
    fig = (
        px.violin(
            df,
            x="from_length",
            y="notation",
            color="notation",
            hover_data=["from_slug"],
            height=600,
            points="all",
            category_orders=dict(notation=notations),
        )
        .update_traces(
            hoveron="points",
            pointpos=0,
            scalemode="count",
            hoverinfo="none",
            hovertemplate="",
        )
        .update_layout(violingroupgap=0, violingap=0.05)
    )
    # fig.update_layout(scattermode="group")
    result.append(fig)

    tokens_df = load_tokens()
    df = (
        tokens_df.query(f"gallery == '{gallery}'")
        .groupby(["token", "notation"])["slug"]
        .nunique()
        .reset_index()
        .groupby(["notation", "slug"])
        .count()
        .reset_index()
        .sort_values(by="slug", ascending=False)
    )
    fig = px.bar(
        df,
        x="notation",
        y="token",
        color="notation",
        text="slug",
        height=600,
        category_orders=dict(notation=notations),
    )
    fig.update_traces(
        textposition="inside",
        textangle=0,
        insidetextanchor="middle",
        texttemplate="%{y} tokens<br> used %{text} times",
    )
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode="hide")
    result.append(fig)

    return result


def thumbnails(gallery, distance, vis):
    registry = load_registry()
    notations = list(registry[gallery].keys())
    df = (
        distances_df(gallery=gallery)
        .groupby(["notation", "to_slug"])[distance]
        .median()
        .reset_index()
    )

    df["rank_in_notation"] = df.groupby("notation")[distance].rank()

    slugs_by_mean_farness_rank = (
        df.groupby("to_slug")["rank_in_notation"]
        .mean()
        .reset_index()
        .sort_values(by="rank_in_notation")
        .to_slug
    )
    rows = []
    for slug in slugs_by_mean_farness_rank:
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
            html.Tr(
                [html.Th(slug, style=dict(textAlign="right"))]
                + cells
                + [html.Th(slug, style=dict(opacity=0))]
            )
        )
    return [
        html.Table(
            [html.Tr([html.Th()] + [html.Th(n) for n in notations])] + rows,
            style=dict(margin="0 auto"),
            className="thumbnails",
        )
    ]


multi_vis_map = {
    "thumbnails": thumbnails,
    "embedding": embedding,
    "stats": stats,
}
multi_vis_types = list(multi_vis_map)


def wrap_multi_vis(gallery, distance, vis):
    vis_list = []

    registry = load_registry()
    first_notation = list(registry[gallery].keys())[0]
    for i, vis_out in enumerate(multi_vis_map[vis](gallery, distance, vis)):
        if isinstance(vis_out, go.Figure):
            vis_list.append(
                dcc.Graph(
                    id=dict(
                        type="figure",
                        suffix="multi",
                        notation=first_notation,
                        seq=str(i),
                    ),
                    figure=vis_out,
                    style=dict(
                        width=str(vis_out.layout.width or "800") + "px", margin="0 auto"
                    ),
                    clear_on_unhover=True,
                )
            )
        else:
            vis_list.append(vis_out)
    return vis_list
