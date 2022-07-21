from functools import cache
import pandas as pd

distance_types = ["difflib", "cd", "ncd"]
filter_prefix = "study==@study and notation==@notation"


difflib_df = pd.read_csv("results/difflib_costs.csv", names=["study", "notation", "from_slug", "to_slug", "difflib"])
ncd_df = pd.read_csv("results/ncd_costs.csv", names=["study", "notation", "from_slug", "to_slug", "a", "b", "ab"])
ncd_df["cd"] = ncd_df["ab"] - ncd_df[["a", "b"]].min(axis=1)
ncd_df["ncd"] = (1000 * ncd_df["cd"] / ncd_df[["a", "b"]].max(axis=1)).astype(int)
distances_df = pd.merge(difflib_df, ncd_df, how="outer")


@cache
def dmat_and_order(study, notation, distance):
    df = distances_df.query(filter_prefix)
    dmat = df.pivot_table(index="from_slug", columns="to_slug", values=distance).fillna(0)
    order = list(dmat.index)
    dmat = dmat.values
    dmat_sym = (dmat + dmat.T) / 2.0
    return dmat, dmat_sym, order


@cache
def get_distance(study, notation, distance, from_slug, to_slug):
    return distances_df.query(filter_prefix + " and from_slug==@from_slug and to_slug==@to_slug")[distance].values[0]
