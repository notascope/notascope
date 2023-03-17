import pandas as pd
import altair as alt

df = pd.read_csv("data/movies.csv")

chart = (
    alt.Chart(df)
    .mark_point()
    .encode(
        x="mean(Production Budget)",
        y="mean(Worldwide Gross)",
        color="MPAA Rating",
        size="mean(IMDB Rating)",
    )
)
