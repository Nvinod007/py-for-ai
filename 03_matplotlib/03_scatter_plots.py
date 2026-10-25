# Scatter plots: relationship between two numbers.
# Each line has a short comment saying WHAT the function is.

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Path("data").exists(): True if that folder exists; otherwise use ../data.
DATA = Path("data") if Path("data").exists() else Path("../data")
# pd.read_csv(file): loads a CSV file into a table.
emp = pd.read_csv(DATA / "03_employees.csv")

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Basic
# plt.subplots(): makes the picture (fig) and one chart (ax).
fig, ax = plt.subplots()
# ax.scatter(x, y): draws one dot per row (age across, salary up).
ax.scatter(emp["age"], emp["salary"])
# ax.set_xlabel / set_ylabel(text): names for the x and y axis.
ax.set_xlabel("Age")
ax.set_ylabel("Salary")
# plt.show(): displays the chart.
plt.show()

# %% Size and colour by values (bubble chart)
# figsize=(w, h): chart size in inches.
fig, ax = plt.subplots(figsize=(8, 5))
points = ax.scatter(
    emp["age"],
    emp["salary"],
    s=emp["performance_score"] ** 3,       # s = dot size, bigger score = bigger bubble
    c=emp["performance_score"],            # c = dot colour taken from these numbers
    cmap="viridis",                        # cmap = colour scale (purple low, yellow high)
    alpha=0.7,                             # alpha = see-through (0 invisible, 1 solid)
    edgecolor="black",                     # edgecolor = outline colour of each dot
)
# fig.colorbar(points, ax=ax, label=...): side strip showing what the colours mean.
fig.colorbar(points, ax=ax, label="Performance")
plt.show()

# %% Colour by category
fig, ax = plt.subplots()
# groupby("department"): splits rows into one group per department (loop gives name + rows).
for dept, group in emp.groupby("department"):
    # label=dept: legend name, so each department gets its own colour.
    ax.scatter(group["age"], group["salary"], label=dept)
# ax.legend(): box explaining each colour.
ax.legend()
plt.show()

# %% Trend line
# np.polyfit(x, y, 1): best straight line through the dots; returns (slope, intercept).
slope, intercept = np.polyfit(emp["age"], emp["salary"], 1)
# np.linspace(a, b, n): n evenly spaced numbers from a to b.  .min()/.max(): smallest/biggest.
line_x = np.linspace(emp["age"].min(), emp["age"].max(), 50)
fig, ax = plt.subplots()
ax.scatter(emp["age"], emp["salary"], alpha=0.7)
# ax.plot(x, y): draws the red trend line; f"slope={slope:.0f}" puts the slope (no decimals) in the legend.
ax.plot(line_x, slope * line_x + intercept, color="red", label=f"slope={slope:.0f}")
ax.legend()
plt.show()

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Label a few points
# .nlargest(3, "salary"): the 3 rows with the highest salary.
top = emp.nlargest(3, "salary")
fig, ax = plt.subplots()
ax.scatter(emp["age"], emp["salary"], alpha=0.5)
# .iterrows(): loops over rows (gives index, row); "_" ignores the index.
for _, row in top.iterrows():
    # ax.annotate(text, (x, y)): writes text near a point. xytext=(5, 5) with
    # textcoords="offset points" moves the text 5 points right and up.
    ax.annotate(row["name"], (row["age"], row["salary"]), xytext=(5, 5), textcoords="offset points")
plt.show()

# %% Marker styles
fig, ax = plt.subplots()
# marker="D": diamond dots. s=40: dot size. color="purple": dot colour.
ax.scatter(emp["age"], emp["salary"], marker="D", s=40, color="purple", alpha=0.6)
plt.show()

# %% 2D histogram when there are too many points
# np.random.default_rng(0): random number maker; 0 = fixed seed so results repeat.
rng = np.random.default_rng(0)
# rng.normal(size=n): n bell-curve random numbers.
x = rng.normal(size=5000)
y = x + rng.normal(size=5000)
fig, ax = plt.subplots()
# ax.hist2d(x, y): splits the chart into square cells and colours each by dot count.
# bins=40: 40 cells per side. cmap="magma": colour scale (dark to bright).
h = ax.hist2d(x, y, bins=40, cmap="magma")
# h[3]: the coloured image part of the result, so the colorbar can show its scale.
fig.colorbar(h[3], ax=ax)
plt.show()

fig, ax = plt.subplots()
# ax.hexbin(x, y): like hist2d but with hexagon cells. gridsize=30: hexagons across.
ax.hexbin(x, y, gridsize=30, cmap="Blues")
plt.show()
