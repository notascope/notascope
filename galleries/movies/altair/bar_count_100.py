import pandas as pd
import altair as alt

df = pd.read_csv("data/movies.csv")

chart = (
    alt.Chart(df)
    .mark_bar()
    .encode(x="Major Genre", y=alt.Y("count()").stack("normalize"), color="MPAA Rating")
)
