import pandas as pd
import altair as alt

df = pd.read_csv("data/movies.csv", parse_dates=["Release Date"])

chart = (
    alt.Chart(df)
    .mark_line(point=True)
    .encode(
        alt.X("Production Budget").aggregate("sum"),
        alt.Y("Worldwide Gross").aggregate("sum"),
        alt.Order("Release Date").timeUnit("year"),
    )
)
