import pandas as pd
from bokeh.plotting import figure

df = pd.read_csv("data/movies.csv", parse_dates=["Release Date"])
df["Release Date"] = df["Release Date"].dt.year
df2 = df.groupby("Release Date")["Worldwide Gross"].sum().reset_index()

p = figure()

p.line(df2["Release Date"], df2["Worldwide Gross"])
