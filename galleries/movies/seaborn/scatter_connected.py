import pandas as pd
import seaborn as sns

df = pd.read_csv("data/movies.csv", parse_dates=["Release Date"])
df2 = df.groupby(df["Release Date"].dt.year).sum(numeric_only=True)

ax = sns.relplot(
    df2,
    x="Production Budget",
    y="Worldwide Gross",
    kind="line",
    sort=False,
    estimator=None,
    marker="o",
)
