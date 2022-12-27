import pandas as pd
import json
from glob import glob

tokens_df = pd.read_csv("results/tokens.tsv", names=["study", "notation", "slug", "token"], delimiter="\t")


def ext(study, notation, obj):
    return sorted(glob(f"results/{study}/{notation}/{obj}/*"), key=len)[-1].split(".")[-1]


results = dict()
for (study, notation), df in tokens_df.groupby(["study", "notation"]):
    if study not in results:
        results[study] = dict()
    results[study][notation] = dict(
        slugs=list(df["slug"].unique()),
        tokens=df["token"].nunique(),
        ext=dict(img=ext(study, notation, "img"), source=ext(study, notation, "source")),
    )

with open("results/registry.json", "w") as f:
    json.dump(results, f)
