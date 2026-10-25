# Compare groups.
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
# sns.set_theme(style="whitegrid"): white background with grid lines for all charts.
sns.set_theme(style="whitegrid")

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Count of rows
# sns.countplot(data, x): one bar per category showing how many rows it has.
# order=...: bar order; value_counts().index = biggest department first.
sns.countplot(data=emp, x="department", order=emp["department"].value_counts().index)
# plt.show(): displays the chart.
plt.show()

# hue="gender": splits each bar into side-by-side bars per gender.
sns.countplot(data=emp, x="department", hue="gender")
plt.show()

# %% Average per group (with error bars)
# sns.barplot(data, x, y): bar = average of y for each x group, with a whisker for spread.
# errorbar="sd": whisker shows standard deviation (how spread out the values are).
sns.barplot(data=emp, x="department", y="salary", errorbar="sd")
plt.show()

# estimator="median": bar height is the middle value instead of the average.
sns.barplot(data=emp, x="department", y="salary", hue="gender", estimator="median")
plt.show()

# Swapping x and y makes the bars sideways.
sns.barplot(data=emp, y="department", x="salary")        # horizontal
plt.show()

# %% Box, violin, boxen
# sns.boxplot(data, x, y): box = middle 50% of values, line = median, dots = outliers.
sns.boxplot(data=emp, x="department", y="salary")
plt.show()

# hue="remote": two boxes per department (remote or not).
sns.boxplot(data=emp, x="department", y="salary", hue="remote")
plt.show()

# sns.violinplot: mirrored smooth shape per group (wide = many values). inner="quartile": lines at 25/50/75%.
sns.violinplot(data=emp, x="department", y="salary", inner="quartile")
plt.show()

# split=True: with 2 hue values, each violin is cut in half (one side per gender).
sns.violinplot(data=emp, x="department", y="salary", hue="gender", split=True)
plt.show()

# sns.boxenplot: like a box plot but with more boxes for the tails; good for big data.
sns.boxenplot(data=emp, x="department", y="salary")
plt.show()

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Show every point
# sns.stripplot: one dot per row in a column per group. jitter=True: spreads dots sideways so they don't overlap.
sns.stripplot(data=emp, x="department", y="salary", jitter=True)
plt.show()

# sns.swarmplot: like stripplot but dots are placed so none overlap.
sns.swarmplot(data=emp, x="department", y="salary", hue="gender")
plt.show()

# %% Combine box + points
# color="lightgray": one fixed colour for all boxes.
sns.boxplot(data=emp, x="department", y="salary", color="lightgray")
# size=4: dot size. Drawn on top of the same chart, so you see boxes and dots together.
sns.stripplot(data=emp, x="department", y="salary", color="black", size=4)
plt.show()

# %% Averages with lines
# sns.pointplot: a dot for each group's average (with whiskers), joined by lines per hue.
sns.pointplot(data=emp, x="department", y="salary", hue="gender")
plt.show()

# %% catplot: any of the above, split into panels
# sns.catplot(...): category chart that can split into panels. kind="box": box plots.
# col="gender": one panel per gender.
sns.catplot(data=emp, x="department", y="salary", col="gender", kind="box")
plt.show()

# kind="count": count bars (no y needed).
sns.catplot(data=emp, x="department", kind="count", hue="remote")
plt.show()
