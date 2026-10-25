# Correlation heatmaps, pair plots, grids, themes and colours.
# Each line has a short comment saying WHAT the function is.

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

# Path("data").exists(): True if that folder exists; otherwise use ../data.
DATA = Path("data") if Path("data").exists() else Path("../data")
# pd.read_csv(file): loads a CSV into a table.
emp = pd.read_csv(DATA / "03_employees.csv")
# parse_dates=[col]: reads that column as dates. index_col="month": uses it as the row labels.
monthly = pd.read_csv(DATA / "04_monthly_sales.csv", parse_dates=["month"], index_col="month")

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Correlation heatmap (the most used one)
# .corr(): table of how strongly each pair of columns moves together (-1 to 1).
corr = emp[["age", "salary", "performance_score"]].corr()
# sns.heatmap(table): coloured squares for each number. annot=True: writes the number in each square.
# cmap="coolwarm": blue = low, red = high. vmin / vmax: values for the lowest / highest colour.
# fmt=".2f": show 2 decimals.
sns.heatmap(corr, annot=True, cmap="coolwarm", vmin=-1, vmax=1, fmt=".2f")
# plt.show(): displays the chart.
plt.show()

# linewidths=0.5: thin gap lines between squares.
sns.heatmap(monthly.corr(), annot=True, cmap="Blues", linewidths=0.5)
plt.show()

# %% Hide half of a symmetric heatmap
# np.ones_like(t, dtype=bool): same-shape table full of True. np.triu(...): keeps the upper triangle.
mask = np.triu(np.ones_like(monthly.corr(), dtype=bool))
# mask=mask: squares where mask is True are hidden. cmap="mako": dark blue-green colour scale.
sns.heatmap(monthly.corr(), mask=mask, annot=True, cmap="mako")
plt.show()

# %% Heatmap of a pivot table
# pivot_table: grid with rows = department, columns = gender, cells = average salary (aggfunc="mean").
pivot = emp.pivot_table(values="salary", index="department", columns="gender", aggfunc="mean")
# fmt=".0f": no decimals. cmap="YlGnBu": yellow-green-blue scale.
sns.heatmap(pivot, annot=True, fmt=".0f", cmap="YlGnBu")
plt.show()

# %% Themes
# Loop over 5 built-in looks: darkgrid, whitegrid, dark, white, ticks.
for style in ["darkgrid", "whitegrid", "dark", "white", "ticks"]:
    # sns.set_theme(style=...): applies that look to the charts that follow.
    sns.set_theme(style=style)
    # sns.lineplot(x, y): simple line through the points.
    sns.lineplot(x=[1, 2, 3], y=[1, 4, 9])
    # plt.title(text): title above the chart.
    plt.title(style)
    plt.show()

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Grouped heatmap (rows and columns are clustered)
# sns.clustermap(table): heatmap where similar rows/columns are placed together (with tree lines).
# cmap="vlag": blue-white-red scale.
sns.clustermap(monthly.corr(), annot=True, cmap="vlag")
plt.show()

# %% Pair plot: every numeric column against every other
# sns.pairplot(table): grid of scatter plots for every pair of number columns (histograms on the diagonal).
# hue="department": colour by department.
sns.pairplot(emp[["age", "salary", "performance_score", "department"]], hue="department")
plt.show()

# kind="reg": adds a trend line in each scatter. diag_kind="kde": smooth curves on the diagonal.
sns.pairplot(emp[["age", "salary", "performance_score"]], kind="reg", diag_kind="kde")
plt.show()

# %% Custom grids
# sns.FacetGrid(data, col=...): empty set of panels, one per department.
# col_wrap=3: 3 panels per row. height=3: panel height.
grid = sns.FacetGrid(emp, col="department", col_wrap=3, height=3)
# grid.map(chart_function, column): draws that chart in every panel (here a histogram of salary).
grid.map(sns.histplot, "salary")
plt.show()

# sns.PairGrid(table): empty grid of every column vs every column, you choose what goes where.
pair = sns.PairGrid(emp[["age", "salary", "performance_score"]])
# map_upper / map_lower / map_diag: chart type for the upper triangle / lower triangle / diagonal.
pair.map_upper(sns.scatterplot)       # dots
pair.map_lower(sns.kdeplot)           # smooth density contours
pair.map_diag(sns.histplot)           # histograms
plt.show()

# %% Context (sizes for papers, talks, posters)
# context="talk": bigger text and lines, good for slides. ("paper" is smaller, "poster" is bigger.)
sns.set_theme(context="talk", style="whitegrid")
# sns.barplot: bar = average salary per department.
sns.barplot(data=emp, x="department", y="salary")
plt.show()
# sns.set_theme() with no arguments: resets to the seaborn default look.
sns.set_theme()

# %% Colours
# sns.color_palette("deep"): a set of matching colours. .as_hex(): shows them as hex codes like #4c72b0.
print(sns.color_palette("deep").as_hex())
# sns.palplot(palette): draws the colours as a row of squares. ("viridis", 6) = 6 colours.
sns.palplot(sns.color_palette("viridis", 6))
plt.show()
# palette="Set2": colour set to use. hue="department": colour by department.
# legend=False: hides the legend (the x axis already names each bar).
sns.barplot(data=emp, x="department", y="salary", hue="department", palette="Set2", legend=False)
plt.show()
sns.barplot(data=emp, x="department", y="salary", hue="department", palette="rocket", legend=False)
# sns.despine(): removes the top and right border lines.
sns.despine()                      # remove top and right lines
plt.show()

# %% Built-in practice datasets (needs internet the first time)
# sns.load_dataset(name): downloads a ready-made example table (tips, iris, titanic).
# tips = sns.load_dataset("tips")
# iris = sns.load_dataset("iris")
# titanic = sns.load_dataset("titanic")
print("Use sns.load_dataset('tips') to get example data")
