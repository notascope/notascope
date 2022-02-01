import seaborn as sns

tips = sns.load_dataset("tips")
fig = sns.catplot(data=tips, x="total_bill", y="day", col="time", kind="violin")
fig
