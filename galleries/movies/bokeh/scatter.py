from bokeh.plotting import figure
import pandas as pd


df = pd.read_csv("data/movies.csv")

p = figure()
p.circle(x=df["Production Budget"], y=df["Worldwide Gross"])
