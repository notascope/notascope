import pandas as pd
import json
from glob import glob
from pathlib import Path

tokens_df = pd.read_csv(
    "results/tokens.tsv",
    names=["gallery", "notation", "slug", "token"],
    delimiter="\t",
)


def ext(gallery, notation, obj):
    return sorted(glob(f"results/{gallery}/{notation}/{obj}/*"), key=len)[-1].split(
        "."
    )[-1]


registry = dict()
for (gallery, notation), df in tokens_df.groupby(["gallery", "notation"]):
    if gallery not in registry:
        registry[gallery] = dict()
    imgext = ext(gallery, notation, "img")
    srcext = ext(gallery, notation, "source")
    registry[gallery][notation] = dict(
        slugs=list(df["slug"].unique()),
        tokens=df["token"].nunique(),
        ext=dict(img=imgext, source=srcext),
    )
    for slug in tokens_df.query(f"gallery=='{gallery}'").slug.unique():
        slug_path = Path(f"galleries/{gallery}/{notation}/{slug}.{srcext}")
        if not slug_path.exists():
            slug_path.write_text("")

with open("results/registry.json", "w") as f:
    json.dump(registry, f)
