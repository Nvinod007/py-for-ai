# Bar charts: compare categories.
# Each line has a short comment saying WHAT the function is.

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Path("data").exists(): True if that folder exists; otherwise use ../data.
DATA = Path("data") if Path("data").exists() else Path("../data")
# pd.read_csv(file): loads a CSV file into a table.
emp = pd.read_csv(DATA / "03_employees.csv")
# groupby("department")["salary"].mean(): average salary per department.
# sort_values(ascending=False): biggest first.
avg = emp.groupby("department")["salary"].mean().sort_values(ascending=False)

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Vertical bars
# plt.subplots(): makes the picture (fig) and one chart (ax).
fig, ax = plt.subplots()
# ax.bar(names, heights): draws vertical bars; color sets the bar colour.
ax.bar(avg.index, avg.values, color="tab:blue")
# ax.set_title(text): title above the chart.
ax.set_title("Average salary by department")
# ax.set_ylabel(text): name beside the y axis.
ax.set_ylabel("Salary")
# plt.show(): displays the chart.
plt.show()

# %% Horizontal bars (better for long names)
fig, ax = plt.subplots()
# ax.barh(names, widths): draws sideways bars (names on the left).
ax.barh(avg.index, avg.values, color="tab:orange")
# ax.invert_yaxis(): flips the y axis so the first item is at the top.
ax.invert_yaxis()                     # biggest on top
plt.show()

# %% Value labels on bars
fig, ax = plt.subplots()
bars = ax.bar(avg.index, avg.values)
# ax.bar_label(bars): writes each bar's value on it. fmt="%.0f": no decimals. padding: gap in points.
ax.bar_label(bars, fmt="%.0f", padding=3)
# ax.set_ylim(low, high): visible y range; 1.15x the max leaves room for the labels.
ax.set_ylim(0, avg.max() * 1.15)
plt.show()

# %% Different colours per bar
# List of colours: red for the biggest bar, light grey for the rest.
colors = ["tab:red" if v == avg.max() else "lightgray" for v in avg.values]
fig, ax = plt.subplots()
# color=list: one colour per bar. edgecolor: outline colour of each bar.
ax.bar(avg.index, avg.values, color=colors, edgecolor="black")
plt.show()

# %% Grouped bars
# pivot_table: builds a grid; rows = department, columns = gender, cells = average salary.
table = emp.pivot_table(values="salary", index="department", columns="gender", aggfunc="mean")
# np.arange(n): numbers 0..n-1, used as bar positions.
x = np.arange(len(table))
width = 0.35                          # width of each bar
fig, ax = plt.subplots()
# ax.bar(x, h, width): shifting x left/right puts the F and M bars side by side.
ax.bar(x - width / 2, table["F"], width, label="F")
ax.bar(x + width / 2, table["M"], width, label="M")
# ax.set_xticks(positions, names): puts department names under each group.
ax.set_xticks(x, table.index)
# ax.legend(): box that explains which colour is F and which is M.
ax.legend()
plt.show()

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Stacked bars
# pd.crosstab(a, b): counts how many rows for each pair (department x gender).
counts = pd.crosstab(emp["department"], emp["gender"])
fig, ax = plt.subplots()
ax.bar(counts.index, counts["F"], label="F")
# bottom=...: starts the M bars on top of the F bars (stacking).
ax.bar(counts.index, counts["M"], bottom=counts["F"], label="M")
ax.legend()
plt.show()

# %% Error bars
# .agg(["mean", "std"]): gets average and spread (standard deviation) per department.
spread = emp.groupby("department")["salary"].agg(["mean", "std"])
fig, ax = plt.subplots()
# yerr: draws a whisker (+/-) on each bar. capsize: width of whisker caps.
# alpha=0.7: slightly see-through bars.
ax.bar(spread.index, spread["mean"], yerr=spread["std"], capsize=5, alpha=0.7)
plt.show()

# %% Count bars (like value_counts)
# .value_counts(): how many times each department appears.
counts = emp["department"].value_counts()
fig, ax = plt.subplots()
ax.bar(counts.index, counts.values)
# ax.tick_params(axis="x", rotation=30): tilts the x labels by 30 degrees.
ax.tick_params(axis="x", rotation=30)
plt.show()

# %% Lollipop and step variations
fig, ax = plt.subplots()
# ax.stem(names, values): thin stick with a dot on top (lollipop) instead of a thick bar.
ax.stem(avg.index, avg.values)
plt.show()
