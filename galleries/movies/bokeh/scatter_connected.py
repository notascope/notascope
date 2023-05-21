import pandas as pd
from bokeh.plotting import figure

df = pd.read_csv("data/movies.csv", parse_dates=["Release Date"])
df["Release Date"] = df["Release Date"].dt.year
df2 = (
    df.groupby("Release Date")[["Worldwide Gross", "Production Budget"]]
    .sum()
    .reset_index()
)

p = figure()
p.circle(x=df2["Production Budget"], y=df2["Worldwide Gross"])
p.line(x=df2["Production Budget"], y=df2["Worldwide Gross"])
