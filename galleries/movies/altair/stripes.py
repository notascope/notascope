import pandas as pd
import altair as alt

df = pd.read_csv("data/movies.csv", parse_dates=["Release Date"])

chart = (
    alt.Chart(df)
    .mark_rect()
    .encode(
        alt.X("Release Date").timeUnit("year"),
        alt.Color("Worldwide Gross").aggregate("sum"),
    )
)
