import pandas as pd
import numpy as np
from .utils import cache

distance_types = ["cd", "ncd", "levenshtein", "difflib", "voi"]


@cache
def distances_df(gallery=None, notation=None):
    if gallery is not None:
        if notation is None:
            return distances_df().query(f"gallery == '{gallery}'")
        else:
            return distances_df().query(
                f"gallery == '{gallery}' and notation=='{notation}'"
            )
    return pd.read_parquet("results/distances.pqt")


@cache
def merged_distances(gallery, notation, distance, notation2, distance2):
    return pd.merge(
        distances_df(gallery=gallery, notation=notation)[
            ["from_spec", "to_spec", distance]
        ],
        distances_df(gallery=gallery, notation=notation2)[
            ["from_spec", "to_spec", distance2]
        ],
        on=["from_spec", "to_spec"],
        suffixes=["_" + notation, "_" + notation2],
    )


@cache
def dmat_and_order(
    gallery: str, notation: str, distance: str
) -> tuple[np.ndarray, list[str]]:
    dmat = (
        distances_df(gallery=gallery, notation=notation)
        .pivot_table(index="from_spec", columns="to_spec", values=distance)
        .fillna(0)
    )
    return dmat.values, dmat.index.tolist()


@cache
def get_distance(gallery, notation, distance, from_spec, to_spec):
    return (
        distances_df(gallery=gallery, notation=notation)
        .query(f"from_spec=='{from_spec}' and to_spec=='{to_spec}'")[distance]
        .values[0]
    )


@cache
def get_distance_rank(gallery, notation, distance, from_spec, to_spec):
    df = (
        distances_df(gallery=gallery, notation=notation)
        .query(f"from_spec=='{from_spec}'")
        .copy()
    )
    df["rank"] = df[distance].rank(method="min").astype(int)
    return df.query(f"to_spec=='{to_spec}'")["rank"].values[0]


@cache
def get_mst(gallery, notation, distance):
    dmat, order = dmat_and_order(gallery, notation, distance)
    from scipy.sparse.csgraph import minimum_spanning_tree
    from scipy.sparse import coo_matrix

    return coo_matrix(minimum_spanning_tree(dmat))


@cache
def get_embedding(gallery, notation, distance, method, dim=2):
    np.random.seed(123)
    dmat, order = dmat_and_order(gallery, notation, distance)
    if method in ["tsne", "umap"] and len(dmat) < 30:
        method = "mds"
    if method == "tsne":
        from sklearn.manifold import TSNE

        embedding = TSNE(
            n_components=dim, metric="precomputed", learning_rate="auto", init="random"
        ).fit_transform(dmat)
    elif method == "umap":
        from umap import UMAP

        embedding = UMAP(n_components=dim).fit_transform(dmat)
    elif method == "mds":
        from sklearn.manifold import MDS

        embedding = MDS(
            n_components=dim, dissimilarity="precomputed", normalized_stress="auto"
        ).fit_transform(dmat)
    elif method == "kk":
        import igraph

        g = igraph.Graph.Weighted_Adjacency(
            get_mst(gallery, notation, distance).toarray().tolist()
        )
        layout = g.layout_kamada_kawai(maxiter=10000, dim=dim)
        embedding = np.array(layout.coords)
    else:
        embedding = None
    if dim == 3:
        return pd.DataFrame(embedding, index=order, columns=["x", "y", "z"])
    return pd.DataFrame(embedding, index=order, columns=["x", "y"])
