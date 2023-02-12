import pandas as pd
import json
from glob import glob
from pathlib import Path

tokens_df = pd.read_csv(
    "results/tokens.tsv",
    names=["gallery", "notation", "spec", "token"],
    delimiter="\t",
)


def ext(gallery, notation, obj):
    try:
        return sorted(glob(f"results/{gallery}/{notation}/{obj}/*"), key=len)[-1].split(
            "."
        )[-1]
    except IndexError:
        print(f"------ results/{gallery}/{notation}/{obj}/*")
        raise


registry = dict()
for (gallery, notation), df in tokens_df.groupby(["gallery", "notation"]):
    if gallery not in registry:
        registry[gallery] = dict()
    imgext = ext(gallery, notation, "img")
    srcext = ext(gallery, notation, "source")
    registry[gallery][notation] = dict(
        specs=list(df["spec"].unique()),
        tokens=df["token"].nunique(),
        ext=dict(img=imgext, source=srcext),
    )
    for spec in tokens_df.query(f"gallery=='{gallery}'").spec.unique():
        spec_path = Path(f"galleries/{gallery}/{notation}/{spec}.{srcext}")
        if not spec_path.exists():
            spec_path.write_text("")

with open("results/registry.json", "w") as f:
    json.dump(registry, f)
