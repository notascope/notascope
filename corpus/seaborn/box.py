import seaborn as sns

tips = sns.load_dataset("tips")
fig = sns.boxplot(data=tips, x="total_bill")
fig