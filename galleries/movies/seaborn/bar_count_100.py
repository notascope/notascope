import pandas as pd
import seaborn as sns

df = pd.read_csv("data/movies.csv")
df2 = (
    df.groupby(["Major Genre", "MPAA Rating"])["Production Budget"]
    .count()
    .reset_index()
)
df2["Production Budget"] /= df2.groupby("Major Genre")["Production Budget"].transform(
    "sum"
)


ax = sns.histplot(
    df2,
    x="Major Genre",
    weights="Production Budget",
    hue="MPAA Rating",
    multiple="stack",
)
