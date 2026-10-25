# pandas can draw charts directly (it uses matplotlib behind the scenes).
# Each line has a short comment saying WHAT the function is.

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# Path("data").exists(): True if that folder exists; otherwise use ../data.
DATA = Path("data") if Path("data").exists() else Path("../data")
# pd.read_csv(file): loads a CSV into a table.
emp = pd.read_csv(DATA / "03_employees.csv")
# parse_dates=[col]: reads that column as dates. index_col="month": uses it as the row labels (x axis).
m = pd.read_csv(DATA / "04_monthly_sales.csv", parse_dates=["month"], index_col="month")

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Line
# table.plot(): draws one line per column. figsize=(w, h): size in inches. title: text on top.
m[["electronics", "clothing", "furniture"]].plot(figsize=(8, 4), title="Sales")
# plt.show(): displays the chart.
plt.show()

# %% Bar
# groupby("department")["salary"].mean(): average salary per department.
# kind="bar": vertical bars. color="teal": bar colour.
emp.groupby("department")["salary"].mean().plot(kind="bar", color="teal")
# plt.ylabel(text): name beside the y axis.
plt.ylabel("Average salary")
plt.show()

# .plot.barh(): sideways bars (same as kind="barh").
emp.groupby("department")["salary"].mean().plot.barh()
plt.show()

# %% Stacked and grouped bars
# pd.crosstab(a, b): counts rows for each pair. stacked=True: piles the bars on top of each other.
pd.crosstab(emp["department"], emp["gender"]).plot(kind="bar", stacked=True)
plt.show()
# pivot_table(values, index, columns): average salary per department (rows) and gender (columns).
# Without stacked=True the bars sit side by side (grouped).
emp.pivot_table(values="salary", index="department", columns="gender").plot(kind="bar")
plt.show()

# %% Histogram, density, box
# kind="hist": bars counting values per range. bins=8: 8 ranges. edgecolor: bar outline.
emp["salary"].plot(kind="hist", bins=8, edgecolor="black")
plt.show()
# kind="density": smooth curve showing where values are most common.
emp["salary"].plot(kind="density")
plt.show()
# kind="box": box plot (middle 50%, median, outliers). subplots=True: one chart per column.
# layout=(1, 2): 1 row, 2 columns.
emp[["age", "salary"]].plot(kind="box", subplots=True, layout=(1, 2))
plt.show()
# emp.boxplot(column, by): one box of that column per group.
emp.boxplot(column="salary", by="department")
plt.show()

# %% Scatter, area, pie, hexbin
# kind="scatter": one dot per row (x, y). c=column: dot colour from that column. colormap: colour scale.
emp.plot(kind="scatter", x="age", y="salary", c="performance_score", colormap="viridis")
plt.show()
# kind="area": coloured areas over time. stacked=True: piled up. alpha=0.7: slightly see-through.
m[["electronics", "clothing", "furniture"]].plot(kind="area", stacked=True, alpha=0.7)
plt.show()
# .value_counts(): how many rows per department. kind="pie": round chart.
# autopct="%1.0f%%": shows percent on each slice. ylabel="": removes the side label.
emp["department"].value_counts().plot(kind="pie", autopct="%1.0f%%", ylabel="")
plt.show()
# kind="hexbin": hexagon cells coloured by how many dots fall in them. gridsize=8: hexagons across.
emp.plot(kind="hexbin", x="age", y="salary", gridsize=8)
plt.show()

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Subplots from columns
# subplots=True: each column gets its own chart. sharex=True: they share the same x axis.
m[["electronics", "clothing", "furniture"]].plot(subplots=True, figsize=(8, 6), sharex=True)
plt.show()

# %% Two axes
# label: legend name. legend=True: shows the legend box. Returns the chart (ax).
ax = m["electronics"].plot(label="electronics", legend=True)
# secondary_y=True: draws on a second y axis on the right. ax=ax: same chart as before.
m["visitors"].plot(secondary_y=True, ax=ax, color="red", legend=True)
plt.show()

# %% Histogram for every numeric column
# table.hist(): one histogram per column. layout=(1, 3): 1 row, 3 columns.
emp[["age", "salary", "performance_score"]].hist(bins=8, figsize=(9, 3), layout=(1, 3))
plt.show()

# %% Scatter matrix
# pd.plotting.scatter_matrix(table): grid of scatter plots, every column against every other.
# diagonal="hist": shows a histogram of each column on the diagonal.
pd.plotting.scatter_matrix(emp[["age", "salary", "performance_score"]], figsize=(7, 7), diagonal="hist")
plt.show()

# %% Use matplotlib on top of pandas plot
# .plot() returns the chart (ax), so you can keep styling it with matplotlib methods.
ax = emp.groupby("department")["salary"].mean().plot(kind="bar")
# ax.set_title(text): title above the chart.
ax.set_title("Mixing both")
# ax.axhline(y): horizontal line at y (here the overall average salary). linestyle="--": dashed.
ax.axhline(emp["salary"].mean(), color="red", linestyle="--")
# plt.tight_layout(): moves things so labels do not overlap.
plt.tight_layout()
plt.show()
