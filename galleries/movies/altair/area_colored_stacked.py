import pandas as pd
import altair as alt

df = pd.read_csv("data/movies.csv", parse_dates=["Release Date"])

chart = (
    alt.Chart(df)
    .mark_area()
    .encode(
        alt.X("Release Date").timeUnit("year"),
        alt.Y("Worldwide Gross").aggregate("sum").stack("normalize"),
        alt.Color("MPAA Rating"),
    )
)
