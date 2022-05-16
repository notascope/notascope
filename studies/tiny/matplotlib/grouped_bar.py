import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.DataFrame(
    {
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Contestant": ["Alex", "Alex", "Alex", "Jordan", "Jordan", "Jordan"],
        "Number Eaten": [2, 1, 3, 1, 3, 2],
    }
)
df2 = df.pivot_table(index="Fruit", columns="Contestant", values="Number Eaten")

x = np.arange(3)
width = 0.3

fig, ax = plt.subplots()
ax.bar(x - width / 2, df2["Alex"], width, label="Alex")
ax.bar(x + width / 2, df2["Jordan"], width, label="Jordan")

ax.set_ylabel("Number Eaten")
ax.set_xlabel("Fruit")
ax.legend(title="Contestant")
ax.set_xticks(x, df2.index)
