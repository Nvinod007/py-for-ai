# Many charts in one picture.
# Each line has a short comment saying WHAT the function is.

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np
import pandas as pd

# Path("data").exists(): True if that folder exists; otherwise use ../data.
DATA = Path("data") if Path("data").exists() else Path("../data")
# pd.read_csv(file): loads a CSV into a table. parse_dates=[col]: reads that column as dates.
m = pd.read_csv(DATA / "04_monthly_sales.csv", parse_dates=["month"])
emp = pd.read_csv(DATA / "03_employees.csv")

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Side by side
# plt.subplots(rows, cols, figsize=(w, h)): one picture with a grid of charts; here 1 row, 2 charts.
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
# ax.plot(x, y): draws a line on that chart.
ax1.plot(m["month"], m["electronics"])
# ax.set_title(text): title above that chart.
ax1.set_title("Electronics")
ax2.plot(m["month"], m["clothing"], color="orange")
ax2.set_title("Clothing")
# fig.suptitle(text): one big title for the whole picture.
fig.suptitle("Sales")
# fig.tight_layout(): moves charts so labels and titles do not overlap.
fig.tight_layout()
# plt.show(): displays the picture.
plt.show()

# %% Grid of charts
# 2 rows x 2 columns; axes is a table of charts, pick one with axes[row, col].
fig, axes = plt.subplots(2, 2, figsize=(10, 7))
axes[0, 0].plot(m["month"], m["electronics"])             # top-left: line
# .dt.month: month number (1-12) from a date column. ax.bar(x, h): vertical bars.
axes[0, 1].bar(m["month"].dt.month, m["clothing"])        # top-right: bars
# ax.hist(values, bins=n): counts values into n ranges.
axes[1, 0].hist(emp["salary"], bins=8)                    # bottom-left: histogram
# ax.scatter(x, y): one dot per row.
axes[1, 1].scatter(emp["age"], emp["salary"])             # bottom-right: dots
# axes.flat: lets you loop over every chart one by one.
for ax in axes.flat:
    # ax.grid(alpha=0.3): faint grid lines (alpha = see-through).
    ax.grid(alpha=0.3)
fig.tight_layout()
plt.show()

# %% Share an axis
# sharex=True: all charts use the same x axis. 3 rows x 1 column.
fig, axes = plt.subplots(3, 1, sharex=True, figsize=(8, 7))
# zip(a, b): walks through two lists together (chart + column name).
for ax, column in zip(axes, ["electronics", "clothing", "furniture"]):
    ax.plot(m["month"], m[column])
    # ax.set_ylabel(text): name beside the y axis.
    ax.set_ylabel(column)
fig.tight_layout()
plt.show()

# sharey=True: all charts use the same y scale, so bars are easy to compare. 1 row x 3 columns.
fig, axes = plt.subplots(1, 3, sharey=True, figsize=(12, 3))
for ax, column in zip(axes, ["electronics", "clothing", "furniture"]):
    ax.bar(m["month"].dt.month, m[column])
    ax.set_title(column)
plt.show()

# %% Two y-axes on one chart
fig, ax1 = plt.subplots(figsize=(8, 4))
# width=20: bar width (in days, because x is dates). alpha=0.5: see-through. label: legend name.
ax1.bar(m["month"], m["electronics"], width=20, alpha=0.5, label="sales")
ax1.set_ylabel("Sales")
# ax.twinx(): a second chart on top that shares x but has its own y axis on the right.
ax2 = ax1.twinx()
# marker="o": a circle on each point.
ax2.plot(m["month"], m["visitors"], color="red", marker="o")
ax2.set_ylabel("Visitors")
plt.show()

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Uneven layout with GridSpec
# plt.figure(figsize=(w, h)): an empty picture to place charts in yourself.
fig = plt.figure(figsize=(9, 6))
# GridSpec(rows, cols, figure=fig): an invisible 2 x 3 grid of cells to place charts in.
gs = GridSpec(2, 3, figure=fig)
# fig.add_subplot(cells): adds a chart covering the chosen cells. gs[0, :] = row 0, all columns.
big = fig.add_subplot(gs[0, :])           # top row, all columns
big.plot(m["month"], m["electronics"])
left = fig.add_subplot(gs[1, 0])
left.hist(emp["age"])
right = fig.add_subplot(gs[1, 1:])        # bottom row, last two columns
right.scatter(emp["age"], emp["salary"])
fig.tight_layout()
plt.show()

# %% Mosaic: draw the layout as text
# plt.subplot_mosaic(layout): each name in the list is a chart; repeated names merge into one wide chart.
# Returns a dict: axd["top"] is the chart named "top".
fig, axd = plt.subplot_mosaic([["top", "top"], ["left", "right"]], figsize=(8, 6))
axd["top"].plot(m["month"], m["visitors"])
axd["left"].bar(["a", "b"], [3, 4])
# ax.pie(sizes): round chart cut into slices.
axd["right"].pie([1, 2, 3])
plt.show()

# %% Chart inside a chart
fig, ax = plt.subplots()
ax.plot(m["month"], m["electronics"])
# ax.inset_axes((x, y, w, h)): small chart placed inside this one (numbers are fractions 0-1).
inset = ax.inset_axes((0.1, 0.55, 0.35, 0.35))
inset.hist(m["electronics"], bins=5)
plt.show()

# %% Spacing control
fig, axes = plt.subplots(2, 2)
# fig.subplots_adjust(hspace, wspace): gap between rows (h) and columns (w).
fig.subplots_adjust(hspace=0.5, wspace=0.3)
plt.show()

# layout="constrained": matplotlib sets the spacing for you.
fig, axes = plt.subplots(2, 2, layout="constrained")     # automatic spacing
plt.show()

# %% Many small charts quickly
fig, axes = plt.subplots(1, 5, figsize=(14, 2), sharey=True)
# emp.groupby("department"): splits rows per department; each loop gives (name, rows).
for ax, (dept, group) in zip(axes, emp.groupby("department")):
    ax.hist(group["salary"], bins=4)
    ax.set_title(dept)
plt.show()
