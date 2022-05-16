import seaborn as sns

tips = sns.load_dataset("tips")
ax = sns.catplot(data=tips, x="total_bill", y="time", col="day", kind="box")
