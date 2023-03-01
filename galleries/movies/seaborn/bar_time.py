import pandas as pd
import seaborn as sns

df = pd.read_csv("data/movies.csv", parse_dates=["Release Date"])
ax = sns.displot(df, x="Release Date", weights="Worldwide Gross", binwidth=365)
