import altair as alt
from plotly.data import tips

chart = (
    alt.Chart(tips(), width=400, height=30)
    .mark_circle(size=8)
    .encode(
        x=alt.X("total_bill"),
        color=alt.Color("time", legend=None),
        row=alt.Row(
            "time",
            header=alt.Header(
                labelAngle=0,
                titleOrient="left",
                labelOrient="left",
                labelAlign="left",
                labelPadding=3,
            ),
        ),
        y=alt.Y(
            "jitter:Q",
            title=None,
            axis=alt.Axis(values=[0], ticks=True, grid=False, labels=False),
            scale=alt.Scale(),
        ),
    )
    .transform_calculate(
        # Generate Gaussian jitter with a Box-Muller transform
        jitter="sqrt(-2*log(random()))*cos(2*PI*random())"
    )
    .configure_facet(spacing=0)
    .configure_view(stroke=None)
)

chart
