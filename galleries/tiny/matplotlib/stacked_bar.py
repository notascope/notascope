import matplotlib.pyplot as plt
import pandas as pd

df = pd.DataFrame(
    {
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Contestant": ["Alex", "Alex", "Alex", "Jordan", "Jordan", "Jordan"],
        "Number Eaten": [2, 1, 3, 1, 3, 2],
    }
)
df2 = df.pivot_table(index="Fruit", columns="Contestant", values="Number Eaten")

fig, ax = plt.subplots()
ax.bar(df2.index, df2["Alex"], label="Alex")
ax.bar(df2.index, df2["Jordan"], bottom=df2["Alex"], label="Jordan")

ax.set_ylabel("Number Eaten")
ax.set_xlabel("Fruit")
ax.legend(title="Contestant")
