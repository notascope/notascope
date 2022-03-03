import seaborn as sns

tips = sns.load_dataset("tips")
fig = sns.catplot(data=tips, x="total_bill", y="time", col="day", kind="box")
fig
