import pandas as pd

df = pd.DataFrame(
    {
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Contestant": ["Alex", "Alex", "Alex", "Jordan", "Jordan", "Jordan"],
        "Number Eaten": [2, 1, 3, 1, 3, 2],
    }
)

df2 = df.pivot_table(index="Contestant", columns="Fruit", values="Number Eaten")
ax = df2.plot()
ax.set_ylabel("Number Eaten")
