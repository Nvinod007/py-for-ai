# Seaborn = nicer statistical charts with less code. Works directly on DataFrames.
# Each line has a short comment saying WHAT the function is.
# Common arguments: data = the table, x / y = column names for the axes, hue = colour by this column.

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Path("data").exists(): True if that folder exists; otherwise use ../data.
DATA = Path("data") if Path("data").exists() else Path("../data")
# pd.read_csv(file): loads a CSV into a table.
emp = pd.read_csv(DATA / "03_employees.csv")
# sns.set_theme(style=...): sets the look for all charts; "whitegrid" = white background + grid lines.
sns.set_theme(style="whitegrid")

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Histogram
# sns.histplot(data, x): bars counting how many rows fall in each range. bins=8: 8 ranges.
sns.histplot(data=emp, x="salary", bins=8)
# plt.show(): displays the chart.
plt.show()

# kde=True: adds a smooth curve on top of the bars.
sns.histplot(data=emp, x="salary", kde=True)           # smooth curve on top
plt.show()

# hue="gender": separate colour per gender. multiple="stack": bars piled on top of each other.
sns.histplot(data=emp, x="salary", hue="gender", multiple="stack")
plt.show()

# Giving both x and y makes a grid of squares coloured by how many points are inside.
sns.histplot(data=emp, x="age", y="salary")            # 2D
plt.show()

# %% Density curve
# sns.kdeplot(data, x): smooth curve showing where values are most common. fill=True: colours under it.
sns.kdeplot(data=emp, x="salary", fill=True)
plt.show()

# hue="department": one curve per department. common_norm=False: each curve scaled on its own.
sns.kdeplot(data=emp, x="salary", hue="department", common_norm=False)
plt.show()

# %% displot: histogram/kde/ecdf, can make many panels
# sns.displot(...): distribution chart that can split into panels. kind="hist": histogram (default).
# col="gender": one panel (column) per gender.
sns.displot(data=emp, x="salary", col="gender", kind="hist")
plt.show()

# row="remote": one panel row per remote value, so you get a grid of panels.
sns.displot(data=emp, x="salary", row="remote", col="gender", bins=6)
plt.show()

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Cumulative
# sns.ecdfplot(data, x): line that climbs from 0 to 1 = share of rows at or below each value.
sns.ecdfplot(data=emp, x="salary", hue="gender")
plt.show()

# %% Small ticks for every point
# sns.rugplot(data, x): a small tick on the axis for every single row.
sns.rugplot(data=emp, x="salary")
plt.show()

# %% Joint view of two variables
# sns.jointplot(data, x, y): main chart for two columns + small histograms on the top and right edges.
# kind="scatter": dots in the main chart.
sns.jointplot(data=emp, x="age", y="salary", kind="scatter")
plt.show()

# kind="reg": dots plus a straight trend line.
sns.jointplot(data=emp, x="age", y="salary", kind="reg")
plt.show()

# kind="kde": smooth contour shapes instead of dots.
sns.jointplot(data=emp, x="age", y="salary", kind="kde")
plt.show()
