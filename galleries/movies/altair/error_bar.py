import pandas as pd
import altair as alt

df = pd.read_csv("data/movies.csv")

chart = (
    alt.Chart(df)
    .mark_point()
    .encode(alt.X("Production Budget").aggregate("mean"), alt.Y("Major Genre"))
)

chart += chart.mark_errorbar(extent="stderr")
