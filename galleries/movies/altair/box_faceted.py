import pandas as pd
import altair as alt

df = pd.read_csv("data/movies.csv")

chart = (
    alt.Chart(df)
    .mark_boxplot()
    .encode(
        x="MPAA Rating",
        y="Production Budget",
        color="MPAA Rating",
        facet=alt.Facet("Major Genre").columns(5),
    )
)
