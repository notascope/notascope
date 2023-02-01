import pandas as pd
import seaborn as sns

df = pd.read_csv("data/movies.csv", parse_dates=["Release Date"])
ax = sns.histplot(df, x="Release Date")
