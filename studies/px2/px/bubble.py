import plotly.express as px

df = px.data.gapminder(year=2007)

fig = px.scatter(df, x="gdpPercap", y="lifeExp", size="pop", color="continent")
