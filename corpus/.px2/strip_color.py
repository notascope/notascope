import plotly.express as px

df = px.data.gapminder(year=2007)

fig = px.strip(df, x="lifeExp", color="continent")