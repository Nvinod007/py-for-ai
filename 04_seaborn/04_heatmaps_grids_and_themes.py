# Correlation heatmaps, pair plots, grids, themes and colours.

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

DATA = Path("data") if Path("data").exists() else Path("../data")
emp = pd.read_csv(DATA / "03_employees.csv")
monthly = pd.read_csv(DATA / "04_monthly_sales.csv", parse_dates=["month"], index_col="month")

# %% Correlation heatmap (the most used one)
corr = emp[["age", "salary", "performance_score"]].corr()
sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1, fmt=".2f")
plt.show()

sns.heatmap(monthly.corr(), annot=True, cmap="Blues", linewidths=0.5)
plt.show()

# %% Hide half of a symmetric heatmap
mask = np.triu(np.ones_like(monthly.corr(), dtype=bool))
sns.heatmap(monthly.corr(), mask=mask, annot=True, cmap="mako")
plt.show()

# %% Heatmap of a pivot table
pivot = emp.pivot_table(values="salary", index="department", columns="gender", aggfunc="mean")
sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGnBu")
plt.show()

# %% Grouped heatmap (rows and columns are clustered)
sns.clustermap(monthly.corr(), annot=True, cmap="vlag")
plt.show()

# %% Pair plot: every numeric column against every other
sns.pairplot(emp[["age", "salary", "performance_score", "department"]], hue="department")
plt.show()

sns.pairplot(emp[["age", "salary", "performance_score"]], kind="reg", diag_kind="kde")
plt.show()

# %% Custom grids
grid = sns.FacetGrid(emp, col="department", col_wrap=3, height=3)
grid.map(sns.histplot, "salary")
plt.show()

pair = sns.PairGrid(emp[["age", "salary", "performance_score"]])
pair.map_upper(sns.scatterplot)
pair.map_lower(sns.kdeplot)
pair.map_diag(sns.histplot)
plt.show()

# %% Themes
for style in ["darkgrid", "whitegrid", "dark", "white", "ticks"]:
    sns.set_theme(style=style)
    sns.lineplot(x=[1, 2, 3], y=[1, 4, 9])
    plt.title(style)
    plt.show()

# %% Context (sizes for papers, talks, posters)
sns.set_theme(context="talk", style="whitegrid")
sns.barplot(data=emp, x="department", y="salary")
plt.show()
sns.set_theme()

# %% Colours
print(sns.color_palette("deep").as_hex())
sns.palplot(sns.color_palette("viridis", 6))
plt.show()
sns.barplot(data=emp, x="department", y="salary", hue="department", palette="Set2", legend=False)
plt.show()
sns.barplot(data=emp, x="department", y="salary", hue="department", palette="rocket", legend=False)
sns.despine()                      # remove top and right lines
plt.show()

# %% Built-in practice datasets (needs internet the first time)
# tips = sns.load_dataset("tips")
# iris = sns.load_dataset("iris")
# titanic = sns.load_dataset("titanic")
print("Use sns.load_dataset('tips') to get example data")
