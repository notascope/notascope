import matplotlib.pyplot as plt
import pandas as pd

df = pd.DataFrame(
    {
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Contestant": ["Alex", "Alex", "Alex", "Jordan", "Jordan", "Jordan"],
        "Number Eaten": [2, 1, 3, 1, 3, 2],
    }
)
df2 = df.pivot_table(index="Contestant", columns="Fruit", values="Number Eaten")

fig, ax = plt.subplots()
ax.plot(df2.index, df2["Apples"], label="Apples")
ax.plot(df2.index, df2["Bananas"], label="Bananas")
ax.plot(df2.index, df2["Oranges"], label="Oranges")

ax.set_ylabel("Number Eaten")
ax.set_xlabel("Contestant")
ax.legend(title="Fruit")
