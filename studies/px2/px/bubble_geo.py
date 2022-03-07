import plotly.express as px

df = px.data.gapminder(year=2007)

fig = px.scatter_geo(df, locations="iso_alpha", color="lifeExp", size="pop")
