import pandas as pd
import altair as alt

df = pd.read_csv("data/movies.csv")

chart = (
    alt.Chart(df)
    .mark_boxplot()
    .encode(
        alt.X("MPAA Rating"),
        alt.Y("Production Budget"),
        alt.Color("MPAA Rating"),
        alt.Facet("Major Genre").columns(5),
    )
)
