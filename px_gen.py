def make_spec(fn, x, y, color):
    spec = f"""import plotly.express as px

df = px.data.tips()

fig = px.{fn}(df, x="{x}", y="{y}", color="{color}")
fig
"""
    with open(f"studies/autogen/px/{fn}_{x}_{y}_{color}.py", "w") as f:
        f.write(spec)


for fn in ["scatter", "bar", "line"]:
    for x in ["tip", "time"]:
        for y in ["tip", "time"]:
            for color in ["tip", "time"]:
                make_spec(fn, x, y, color)
