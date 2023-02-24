import pandas as pd
import seaborn as sns

df = pd.read_csv("data/movies.csv")
df["Release Date"] = pd.to_datetime(df["Release Date"]).dt.year
df2 = df.groupby(["Release Date", "MPAA Rating"])["Worldwide Gross"].sum().reset_index()
df2["Worldwide Gross"] /= df2.groupby("Release Date")["Worldwide Gross"].transform(
    "sum"
)


ax = sns.displot(
    df2,
    x="Release Date",
    weights="Worldwide Gross",
    hue="MPAA Rating",
    multiple="stack",
    element="poly",
    bins=100,
)
