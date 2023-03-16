import pandas as pd
import altair as alt

df = pd.read_csv("data/movies.csv")

chart = (
    alt.Chart(df)
    .mark_boxplot()
    .encode(alt.X("Major Genre"), alt.Y("Production Budget"))
)
