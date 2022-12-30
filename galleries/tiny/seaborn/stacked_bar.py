import pandas as pd
import seaborn as sns

df = pd.DataFrame(
    {
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Contestant": ["Alex", "Alex", "Alex", "Jordan", "Jordan", "Jordan"],
        "Number Eaten": [2, 1, 3, 1, 3, 2],
    }
)

ax = sns.histplot(data=df, x="Fruit", weights="Number Eaten", multiple="stack", hue="Contestant")
