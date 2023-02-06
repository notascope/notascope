import seaborn.objects as so
import pandas as pd

df = pd.DataFrame(
    {
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Contestant": ["Alex", "Alex", "Alex", "Jordan", "Jordan", "Jordan"],
        "Number Eaten": [2, 1, 3, 1, 3, 2],
    }
)

p = so.Plot(df, x="Fruit", y="Number Eaten", color="Contestant").add(
    so.Bar(), so.Dodge()
)
