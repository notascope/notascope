import pandas as pd
import seaborn as sns

df = pd.read_csv("data/movies.csv")
df2 = df.groupby(["Major Genre", "MPAA Rating"]).size().reset_index()
df2[0] /= df2.groupby("Major Genre")[0].transform("sum")

ax = sns.histplot(
    df2,
    x="Major Genre",
    weights=0,
    hue="MPAA Rating",
    multiple="stack",
)
