from functools import cache
import pandas as pd


@cache
def load_tokens():
    return pd.read_csv(
        "results/tokens.tsv",
        names=["gallery", "notation", "slug", "token"],
        delimiter="\t",
    )
