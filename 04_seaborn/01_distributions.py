# Seaborn = nicer statistical charts with less code. Works directly on DataFrames.

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

DATA = Path("data") if Path("data").exists() else Path("../data")
emp = pd.read_csv(DATA / "03_employees.csv")
sns.set_theme(style="whitegrid")

# %% Histogram
sns.histplot(data=emp, x="salary", bins=8)
plt.show()

sns.histplot(data=emp, x="salary", kde=True)           # smooth curve on top
plt.show()

sns.histplot(data=emp, x="salary", hue="gender", multiple="stack")
plt.show()

sns.histplot(data=emp, x="age", y="salary")            # 2D
plt.show()

# %% Density curve
sns.kdeplot(data=emp, x="salary", fill=True)
plt.show()

sns.kdeplot(data=emp, x="salary", hue="department", common_norm=False)
plt.show()

# %% Cumulative
sns.ecdfplot(data=emp, x="salary", hue="gender")
plt.show()

# %% Small ticks for every point
sns.rugplot(data=emp, x="salary")
plt.show()

# %% displot: histogram/kde/ecdf, can make many panels
sns.displot(data=emp, x="salary", col="gender", kind="hist")
plt.show()

sns.displot(data=emp, x="salary", row="remote", col="gender", bins=6)
plt.show()

# %% Joint view of two variables
sns.jointplot(data=emp, x="age", y="salary", kind="scatter")
plt.show()

sns.jointplot(data=emp, x="age", y="salary", kind="reg")
plt.show()

sns.jointplot(data=emp, x="age", y="salary", kind="kde")
plt.show()
