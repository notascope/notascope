import pandas as pd
import altair as alt

df = pd.read_csv("data/movies.csv")

chart = (
    alt.Chart(df)
    .mark_area()
    .encode(
        x="year(Release Date)",
        y=alt.Y("sum(Worldwide Gross)").stack("normalize"),
        color="MPAA Rating",
    )
)
