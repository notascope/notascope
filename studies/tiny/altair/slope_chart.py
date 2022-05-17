import pandas as pd
import altair as alt

df = pd.DataFrame(
    {
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Contestant": ["Alex", "Alex", "Alex", "Jordan", "Jordan", "Jordan"],
        "Number Eaten": [2, 1, 3, 1, 3, 2],
    }
)

chart = alt.Chart(df).mark_line().encode(x="Contestant", y="Number Eaten", color="Fruit")
chart.properties(width=400, height=400)
