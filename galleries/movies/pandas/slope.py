import pandas as pd

df = pd.read_csv("data/movies.csv")
ax = (
    df.pivot_table(
        index="Major Genre",
        columns="MPAA Rating",
        values="Production Budget",
        aggfunc="mean",
    )
    .fillna(0)
    .plot.line()
)
