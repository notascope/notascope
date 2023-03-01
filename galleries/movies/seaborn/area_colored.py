import pandas as pd
import seaborn as sns

df = pd.read_csv("data/movies.csv", parse_dates=["Release Date"])

ax = sns.displot(
    df,
    x="Release Date",
    weights="Worldwide Gross",
    hue="MPAA Rating",
    multiple="stack",
    element="poly",
    binwidth=365,
)
