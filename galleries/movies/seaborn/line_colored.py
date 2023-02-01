import pandas as pd
import seaborn as sns

df = pd.read_csv("data/movies.csv")
df["Release Date"] = pd.to_datetime(df["Release Date"]).dt.year

ax = sns.lineplot(
    df,
    x="Release Date",
    y="Worldwide Gross",
    hue="MPAA Rating",
    estimator="sum",
    errorbar=None,
)
