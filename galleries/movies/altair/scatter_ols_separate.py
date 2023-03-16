import pandas as pd
import altair as alt

df = pd.read_csv("data/movies.csv")

chart = (
    alt.Chart(df)
    .mark_point()
    .encode(
        alt.X("Production Budget"), alt.Y("Worldwide Gross"), alt.Color("MPAA Rating")
    )
)
chart += chart.transform_regression(
    "Production Budget", "Worldwide Gross", groupby=["MPAA Rating"]
).mark_line()
