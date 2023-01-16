from sklearn.manifold import TSNE, MDS
from umap import UMAP
import pandas as pd
import numpy as np
from scipy.sparse.csgraph import minimum_spanning_tree
from scipy.sparse import coo_matrix
from functools import cache
import igraph


np.random.seed(123)
distance_types = ["nmi", "cd", "ncd", "difflib"]


@cache
def distances_df():
    difflib_df = pd.read_csv(
        "results/difflib_costs.csv",
        names=["gallery", "notation", "from_slug", "to_slug", "difflib"],
    )
    ncd_df = pd.read_csv(
        "results/ncd_costs.csv",
        names=["gallery", "notation", "from_slug", "to_slug", "a", "b", "ab"],
    )
    ncd_df["nmi"] = 2 * ncd_df["ab"] - ncd_df["a"] - ncd_df["b"]
    ncd_df["cd"] = ncd_df["ab"] - ncd_df[["a", "b"]].min(axis=1)
    ncd_df["ncd"] = (1000 * ncd_df["cd"] / ncd_df[["a", "b"]].max(axis=1)).astype(int)
    return pd.merge(difflib_df, ncd_df, how="outer")


@cache
def merged_distances(gallery, notation, distance, notation2, distance2):
    df = distances_df()
    return pd.merge(
        df.query(f"gallery=='{gallery}' and notation=='{notation}'")[
            ["from_slug", "to_slug", distance]
        ],
        df.query(f"gallery=='{gallery}' and notation=='{notation2}'")[
            ["from_slug", "to_slug", distance2]
        ],
        on=["from_slug", "to_slug"],
        suffixes=["_" + notation, "_" + notation2],
    )


@cache
def dmat_and_order(gallery, notation, distance):
    df = distances_df().query(f"gallery=='{gallery}' and notation=='{notation}'")
    dmat = df.pivot_table(index="from_slug", columns="to_slug", values=distance).fillna(
        0
    )
    order = list(dmat.index)
    dmat = dmat.values
    dmat_sym = (dmat + dmat.T) / 2.0
    return dmat, dmat_sym, order


@cache
def get_distance(gallery, notation, distance, from_slug, to_slug):
    return (
        distances_df()
        .query(
            f"gallery=='{gallery}' and notation=='{notation}' and from_slug=='{from_slug}' and to_slug=='{to_slug}'"
        )[distance]
        .values[0]
    )


@cache
def get_mst(gallery, notation, distance):
    dmat, dmat_sym, order = dmat_and_order(gallery, notation, distance)
    return coo_matrix(minimum_spanning_tree(dmat_sym))


@cache
def get_embedding(gallery, notation, distance, method, dim=2):
    dmat, dmat_sym, order = dmat_and_order(gallery, notation, distance)
    if method == "tsne":
        embedding = TSNE(
            n_components=dim,
            metric="precomputed",
            learning_rate="auto",
            init="random",
        ).fit_transform(dmat_sym)
    elif method == "umap":
        embedding = UMAP(n_components=dim).fit_transform(dmat_sym)
    elif method == "mds":
        embedding = MDS(n_components=dim, dissimilarity="precomputed").fit_transform(
            dmat_sym
        )
    elif method == "kk":
        g = igraph.Graph.Weighted_Adjacency(
            get_mst(gallery, notation, distance).toarray().tolist()
        )
        layout = g.layout_kamada_kawai(maxiter=10000, dim=dim)
        embedding = np.array(layout.coords)
    if dim == 3:
        return pd.DataFrame(embedding, index=order, columns=["x", "y", "z"])
    return pd.DataFrame(embedding, index=order, columns=["x", "y"])
