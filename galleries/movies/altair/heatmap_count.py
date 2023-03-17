import pandas as pd
import altair as alt

df = pd.read_csv("data/movies.csv")

chart = (
    alt.Chart(df).mark_rect().encode(x="Major Genre", y="MPAA Rating", color="count()")
)
