# Compare groups.

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

DATA = Path("data") if Path("data").exists() else Path("../data")
emp = pd.read_csv(DATA / "03_employees.csv")
sns.set_theme(style="whitegrid")

# %% Count of rows
sns.countplot(data=emp, x="department", order=emp["department"].value_counts().index)
plt.show()

sns.countplot(data=emp, x="department", hue="gender")
plt.show()

# %% Average per group (with error bars)
sns.barplot(data=emp, x="department", y="salary", errorbar="sd")
plt.show()

sns.barplot(data=emp, x="department", y="salary", hue="gender", estimator="median")
plt.show()

sns.barplot(data=emp, y="department", x="salary")        # horizontal
plt.show()

# %% Box, violin, boxen
sns.boxplot(data=emp, x="department", y="salary")
plt.show()

sns.boxplot(data=emp, x="department", y="salary", hue="remote")
plt.show()

sns.violinplot(data=emp, x="department", y="salary", inner="quartile")
plt.show()

sns.violinplot(data=emp, x="department", y="salary", hue="gender", split=True)
plt.show()

sns.boxenplot(data=emp, x="department", y="salary")
plt.show()

# %% Show every point
sns.stripplot(data=emp, x="department", y="salary", jitter=True)
plt.show()

sns.swarmplot(data=emp, x="department", y="salary", hue="gender")
plt.show()

# %% Combine box + points
sns.boxplot(data=emp, x="department", y="salary", color="lightgray")
sns.stripplot(data=emp, x="department", y="salary", color="black", size=4)
plt.show()

# %% Averages with lines
sns.pointplot(data=emp, x="department", y="salary", hue="gender")
plt.show()

# %% catplot: any of the above, split into panels
sns.catplot(data=emp, x="department", y="salary", col="gender", kind="box")
plt.show()

sns.catplot(data=emp, x="department", kind="count", hue="remote")
plt.show()
