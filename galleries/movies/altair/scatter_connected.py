import pandas as pd
import altair as alt

df = pd.read_csv("data/movies.csv")

chart = (
    alt.Chart(df)
    .mark_line(point=True)
    .encode(
        x="sum(Production Budget)", y="sum(Worldwide Gross)", order="year(Release Date)"
    )
)
