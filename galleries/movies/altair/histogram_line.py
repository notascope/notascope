import pandas as pd
import altair as alt

df = pd.read_csv("data/movies.csv")

chart = (
    alt.Chart(df).mark_line().encode(x=alt.X("Production Budget").bin(), y="count()")
)
