# Show how values are spread out.
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

# %% Histogram
# plt.subplots(): makes the picture (fig) and one chart (ax).
fig, ax = plt.subplots()
# ax.hist(values, bins=n): counts values into n ranges and draws a bar for each (bell-ish shape).
# color: bar fill. edgecolor: bar outline.
ax.hist(emp["salary"], bins=8, color="skyblue", edgecolor="black")
# ax.set_xlabel / set_ylabel(text): names for the x and y axis.
ax.set_xlabel("Salary")
ax.set_ylabel("People")
# plt.show(): displays the chart.
plt.show()

# %% Histogram options
fig, ax = plt.subplots()
# bins=[...]: your own range edges. density=True: bar areas add up to 1 (shows share, not count).
# alpha=0.7: slightly see-through.
ax.hist(emp["salary"], bins=[40000, 60000, 80000, 100000, 140000], density=True, alpha=0.7)
# ax.axvline(x): draws a vertical line at x. linestyle="--": dashed. .mean(): average.
ax.axvline(emp["salary"].mean(), color="red", linestyle="--", label="mean")
# .median(): middle value.
ax.axvline(emp["salary"].median(), color="green", linestyle="--", label="median")
# ax.legend(): box naming each line/bar colour.
ax.legend()
plt.show()

# %% Compare two groups
fig, ax = plt.subplots()
# emp[emp["gender"] == "F"]: keeps only the rows where gender is F.
# alpha=0.6 lets the two histograms show through each other. label: legend name.
ax.hist(emp[emp["gender"] == "F"]["salary"], bins=8, alpha=0.6, label="F")
ax.hist(emp[emp["gender"] == "M"]["salary"], bins=8, alpha=0.6, label="M")
ax.legend()
plt.show()

# %% Box plot
fig, ax = plt.subplots()
# ax.boxplot(values): box = middle 50%, line = median, whiskers = normal range, dots = outliers.
ax.boxplot(emp["salary"])
plt.show()

# %% Box plot per group
# .groupby("department"): splits rows per department; g["salary"].values = that group's salaries.
groups = [g["salary"].values for _, g in emp.groupby("department")]
labels = [name for name, _ in emp.groupby("department")]   # department names
fig, ax = plt.subplots()
# ax.boxplot(list of arrays): one box per group.
# tick_labels: names under each box. patch_artist=True: boxes can be filled with colour.
# showmeans=True: also marks the average with a small triangle.
ax.boxplot(groups, tick_labels=labels, patch_artist=True, showmeans=True)
ax.set_ylabel("Salary")
plt.show()

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Cumulative
fig, ax = plt.subplots()
# cumulative=True: each bin includes everything before it (line only goes up).
# histtype="step": draws just an outline instead of filled bars.
ax.hist(emp["salary"], bins=10, cumulative=True, histtype="step")
plt.show()

# %% Horizontal box plot
fig, ax = plt.subplots()
# orientation="horizontal": boxes lie sideways.
ax.boxplot(groups, tick_labels=labels, orientation="horizontal")
plt.show()

# %% Violin plot
fig, ax = plt.subplots()
# ax.violinplot(list of arrays): a mirrored smooth shape per group (wide = many values there).
# showmedians=True: draws a line at each median.
ax.violinplot(groups, showmedians=True)
# ax.set_xticks(positions, names): puts department names under each violin (positions start at 1).
ax.set_xticks(range(1, len(labels) + 1), labels)
plt.show()

# %% Normal data for a bell curve
# np.random.default_rng(1): random number maker; 1 = fixed seed so results repeat.
rng = np.random.default_rng(1)
# rng.normal(mean, spread, n): n bell-curve random numbers (mean 100, spread 15).
data = rng.normal(100, 15, 2000)
fig, ax = plt.subplots()
# bins=40: 40 bars. density=True: scales bars so they match the curve drawn below.
ax.hist(data, bins=40, density=True, alpha=0.6)
# np.linspace(a, b, n): n evenly spaced numbers from a to b.
xs = np.linspace(40, 160, 200)
# ax.plot(x, y): draws a red line; np.exp / np.sqrt / np.pi build the bell-curve formula.
ax.plot(xs, np.exp(-((xs - 100) ** 2) / (2 * 15**2)) / (15 * np.sqrt(2 * np.pi)), color="red")
plt.show()

# %% Histogram counts without drawing
# np.histogram(values, bins=5): returns the count per bin and the bin edges (no picture).
counts, edges = np.histogram(emp["salary"], bins=5)
print(counts, edges)
