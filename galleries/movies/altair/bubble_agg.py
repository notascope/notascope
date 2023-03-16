import pandas as pd
import altair as alt

df = pd.read_csv("data/movies.csv")

chart = (
    alt.Chart(df)
    .mark_point()
    .encode(
        alt.X("Production Budget").aggregate("mean"),
        alt.Y("Worldwide Gross").aggregate("mean"),
        alt.Color("MPAA Rating"),
        alt.Size("IMDB Rating").aggregate("mean"),
    )
)
