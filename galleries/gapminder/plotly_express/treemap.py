import plotly.express as px

df = px.data.gapminder(year=2007)

fig = px.treemap(df, path=["continent", "country"], values="pop", color="lifeExp")
