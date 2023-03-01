import pandas as pd
import plotly.express as px

df = pd.read_csv("data/movies.csv", parse_dates=["Release Date"])
df2 = (
    df.groupby([df["Release Date"].dt.year, "MPAA Rating"])["Worldwide Gross"]
    .sum()
    .reset_index()
)
fig = px.area(
    df2, x="Release Date", y="Worldwide Gross", color="MPAA Rating", groupnorm="percent"
)
fig
