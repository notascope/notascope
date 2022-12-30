import pandas as pd
import json
from glob import glob

tokens_df = pd.read_csv(
    "results/tokens.tsv", names=["gallery", "notation", "slug", "token"], delimiter="\t"
)


def ext(gallery, notation, obj):
    return sorted(glob(f"results/{gallery}/{notation}/{obj}/*"), key=len)[-1].split(
        "."
    )[-1]


results = dict()
for (gallery, notation), df in tokens_df.groupby(["gallery", "notation"]):
    if gallery not in results:
        results[gallery] = dict()
    results[gallery][notation] = dict(
        slugs=list(df["slug"].unique()),
        tokens=df["token"].nunique(),
        ext=dict(
            img=ext(gallery, notation, "img"), source=ext(gallery, notation, "source")
        ),
    )

with open("results/registry.json", "w") as f:
    json.dump(results, f)
