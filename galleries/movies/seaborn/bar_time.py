import pandas as pd
import seaborn as sns

df = pd.read_csv("data/movies.csv")
df["Release Date"] = pd.to_datetime(df["Release Date"]).dt.year

ax = sns.barplot(
    df, x="Release Date", y="Worldwide Gross", estimator="sum", errorbar=None
)
