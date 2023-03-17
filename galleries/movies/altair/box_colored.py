import pandas as pd
import altair as alt

df = pd.read_csv("data/movies.csv")

chart = (
    alt.Chart(df)
    .mark_boxplot()
    .encode(
        x="Major Genre",
        xOffset="MPAA Rating",
        y="Production Budget",
        color="MPAA Rating",
    )
)
