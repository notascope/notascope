import pandas as pd
import altair as alt

df = pd.read_csv("data/movies.csv", parse_dates=["Release Date"])

chart = alt.Chart(df).mark_arc().encode(alt.Theta("count()"), alt.Color("MPAA Rating"))
