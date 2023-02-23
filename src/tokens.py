from .utils import cache
import pandas as pd


@cache
def load_tokens():
    return pd.read_parquet("results/tokens.pqt")
