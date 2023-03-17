import pandas as pd
import altair as alt

df = pd.read_csv("data/movies.csv")

chart = (
    alt.Chart(df)
    .mark_line()
    .encode(x="year(Release Date)", y="sum(Worldwide Gross)", color="MPAA Rating")
)
