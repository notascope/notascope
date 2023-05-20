from bokeh.plotting import figure
import pandas as pd


df = pd.read_csv("data/movies.csv", parse_dates=["Release Date"])
df["Release Date"] = df["Release Date"].dt.year
df2 = df.groupby("Release Date")["Worldwide Gross"].sum().reset_index()
p = figure()

p.vbar(x=df2["Release Date"], top=df2["Worldwide Gross"])
