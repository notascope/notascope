import pandas as pd
import numpy as np
from functools import cache


distance_types = ["voi", "cd", "ncd", "difflib"]


@cache
def distances_df(gallery=None, notation=None):
    if gallery is not None:
        if notation is None:
            return distances_df().query(f"gallery == '{gallery}'")
        else:
            return distances_df(gallery=gallery).query(f"notation=='{notation}'")
    df = pd.read_parquet("results/distances.pqt")
    df["voi"] = 2 * df["ab"] - df["a"] - df["b"]
    df["cd"] = df["ab"] - df[["a", "b"]].min(axis=1)
    df["ncd"] = (1000 * df["cd"] / df[["a", "b"]].max(axis=1)).astype(int)
    return df


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
def dmat_and_order(gallery, notation, distance):
    dmat = (
        distances_df(gallery=gallery, notation=notation)
        .pivot_table(index="from_spec", columns="to_spec", values=distance)
        .fillna(0)
    )
    order = list(dmat.index)
    dmat = dmat.values
    dmat_sym = (dmat + dmat.T) / 2.0
    return dmat, dmat_sym, order


@cache
def get_distance(gallery, notation, distance, from_spec, to_spec):
    return (
        distances_df(gallery=gallery, notation=notation)
        .query(f"from_spec=='{from_spec}' and to_spec=='{to_spec}'")[distance]
        .values[0]
    )


@cache
def get_mst(gallery, notation, distance):
    dmat, dmat_sym, order = dmat_and_order(gallery, notation, distance)
    from scipy.sparse.csgraph import minimum_spanning_tree
    from scipy.sparse import coo_matrix

    return coo_matrix(minimum_spanning_tree(dmat_sym))


@cache
def get_embedding(gallery, notation, distance, method, dim=2):
    np.random.seed(123)
    dmat, dmat_sym, order = dmat_and_order(gallery, notation, distance)
    if method in ["tsne", "umap"] and len(dmat) < 30:
        method = "mds"
    if method == "tsne":
        from sklearn.manifold import TSNE

        embedding = TSNE(
            n_components=dim,
            metric="precomputed",
            learning_rate="auto",
            init="random",
        ).fit_transform(dmat_sym)
    elif method == "umap":
        from umap import UMAP

        embedding = UMAP(n_components=dim).fit_transform(dmat_sym)
    elif method == "mds":
        from sklearn.manifold import MDS

        embedding = MDS(
            n_components=dim, dissimilarity="precomputed", normalized_stress="auto"
        ).fit_transform(dmat_sym)
    elif method == "kk":
        import igraph

        g = igraph.Graph.Weighted_Adjacency(
            get_mst(gallery, notation, distance).toarray().tolist()
        )
        layout = g.layout_kamada_kawai(maxiter=10000, dim=dim)
        embedding = np.array(layout.coords)
    if dim == 3:
        return pd.DataFrame(embedding, index=order, columns=["x", "y", "z"])
    return pd.DataFrame(embedding, index=order, columns=["x", "y"])
