import seaborn as sns

tips = sns.load_dataset("tips")
ax = sns.boxplot(data=tips, x="total_bill", y="time")
