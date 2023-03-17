import pandas as pd
import altair as alt

df = pd.read_csv("data/movies.csv")

chart = (
    alt.Chart(df)
    .mark_point()
    .encode(
        x="Production Budget",
        y="Worldwide Gross",
        color="MPAA Rating",
        shape="Major Genre",
    )
)
