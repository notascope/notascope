import pandas as pd
import seaborn as sns

df = pd.read_csv("data/movies.csv", parse_dates=["Release Date"])
df["Release Date"] = df["Release Date"].dt.year

ax = sns.relplot(
    df,
    kind="line",
    x="Release Date",
    y="Worldwide Gross",
    hue="MPAA Rating",
    estimator="sum",
    errorbar=None,
)
