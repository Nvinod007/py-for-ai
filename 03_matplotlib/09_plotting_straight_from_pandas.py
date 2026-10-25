# pandas can draw charts directly (it uses matplotlib behind the scenes).

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

DATA = Path("data") if Path("data").exists() else Path("../data")
emp = pd.read_csv(DATA / "03_employees.csv")
m = pd.read_csv(DATA / "04_monthly_sales.csv", parse_dates=["month"], index_col="month")

# %% Line
m[["electronics", "clothing", "furniture"]].plot(figsize=(8, 4), title="Sales")
plt.show()

# %% Bar
emp.groupby("department")["salary"].mean().plot(kind="bar", color="teal")
plt.ylabel("Average salary")
plt.show()

emp.groupby("department")["salary"].mean().plot.barh()
plt.show()

# %% Stacked and grouped bars
pd.crosstab(emp["department"], emp["gender"]).plot(kind="bar", stacked=True)
plt.show()
emp.pivot_table(values="salary", index="department", columns="gender").plot(kind="bar")
plt.show()

# %% Histogram, density, box
emp["salary"].plot(kind="hist", bins=8, edgecolor="black")
plt.show()
emp["salary"].plot(kind="density")
plt.show()
emp[["age", "salary"]].plot(kind="box", subplots=True, layout=(1, 2))
plt.show()
emp.boxplot(column="salary", by="department")
plt.show()

# %% Scatter, area, pie, hexbin
emp.plot(kind="scatter", x="age", y="salary", c="performance_score", colormap="viridis")
plt.show()
m[["electronics", "clothing", "furniture"]].plot(kind="area", stacked=True, alpha=0.7)
plt.show()
emp["department"].value_counts().plot(kind="pie", autopct="%1.0f%%", ylabel="")
plt.show()
emp.plot(kind="hexbin", x="age", y="salary", gridsize=8)
plt.show()

# %% Subplots from columns
m[["electronics", "clothing", "furniture"]].plot(subplots=True, figsize=(8, 6), sharex=True)
plt.show()

# %% Two axes
ax = m["electronics"].plot(label="electronics", legend=True)
m["visitors"].plot(secondary_y=True, ax=ax, color="red", legend=True)
plt.show()

# %% Histogram for every numeric column
emp[["age", "salary", "performance_score"]].hist(bins=8, figsize=(9, 3), layout=(1, 3))
plt.show()

# %% Scatter matrix
pd.plotting.scatter_matrix(emp[["age", "salary", "performance_score"]], figsize=(7, 7), diagonal="hist")
plt.show()

# %% Use matplotlib on top of pandas plot
ax = emp.groupby("department")["salary"].mean().plot(kind="bar")
ax.set_title("Mixing both")
ax.axhline(emp["salary"].mean(), color="red", linestyle="--")
plt.tight_layout()
plt.show()
