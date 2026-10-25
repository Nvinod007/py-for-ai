# Practice: one dashboard from the employee data.
# Try building each chart yourself first, then compare.
# Each line has a short comment saying WHAT the function is.

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

# Path("data").exists(): True if that folder exists; otherwise use ../data.
DATA = Path("data") if Path("data").exists() else Path("../data")
# pd.read_csv(file): loads a CSV into a table. parse_dates=[col]: reads that column as dates.
emp = pd.read_csv(DATA / "03_employees.csv", parse_dates=["join_date"])

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Dashboard
# plt.subplots(2, 3, figsize=(w, h)): one big picture with 2 rows x 3 charts. axes[row, col] picks one.
fig, axes = plt.subplots(2, 3, figsize=(15, 8))
# fig.suptitle(text): one big title for the whole picture. fontweight="bold": thick text.
fig.suptitle("Company overview", fontsize=16, fontweight="bold")

# 1. headcount per department
# .value_counts(): how many times each department appears.
counts = emp["department"].value_counts()
# ax.bar(names, heights): vertical bars.
axes[0, 0].bar(counts.index, counts.values, color="tab:blue")
# ax.set_title(text): title above that chart.
axes[0, 0].set_title("Headcount")
# ax.tick_params(axis="x", rotation=30): tilts the x labels by 30 degrees.
axes[0, 0].tick_params(axis="x", rotation=30)

# 2. salary distribution
# ax.hist(values, bins=8): counts values into 8 ranges and draws a bar for each. edgecolor: outline.
axes[0, 1].hist(emp["salary"], bins=8, color="tab:green", edgecolor="white")
axes[0, 1].set_title("Salary distribution")

# 3. age vs salary
# ax.scatter(x, y, c=...): dots; c colours each dot by performance, cmap = colour scale.
axes[0, 2].scatter(emp["age"], emp["salary"], c=emp["performance_score"], cmap="viridis")
axes[0, 2].set_title("Age vs salary (colour = performance)")

# 4. hires per year
# .dt.year: year from a date column. groupby(...).size(): number of rows per year.
hires = emp.groupby(emp["join_date"].dt.year).size()
# ax.plot(x, y, marker="o"): line with a circle on each point.
axes[1, 0].plot(hires.index, hires.values, marker="o")
axes[1, 0].set_title("Hires per year")

# 5. salary spread per department
# One list of salaries per department (groupby gives name + rows).
groups = [g["salary"] for _, g in emp.groupby("department")]
# ax.boxplot(list of arrays): one box per group. tick_labels: names under the boxes.
# .unique(): each distinct value once. sorted(): A to Z (same order as groupby).
axes[1, 1].boxplot(groups, tick_labels=sorted(emp["department"].unique()))
axes[1, 1].set_title("Salary by department")
axes[1, 1].tick_params(axis="x", rotation=30)

# 6. remote share
remote = emp["remote"].value_counts()
# ax.pie(sizes, labels=...): round chart; autopct="%1.0f%%" prints each slice's percent.
axes[1, 2].pie(remote, labels=["Remote" if k else "Office" for k in remote.index], autopct="%1.0f%%")
axes[1, 2].set_title("Remote vs office")

# fig.tight_layout(): moves charts so labels and titles do not overlap.
fig.tight_layout()
# plt.show(): displays the picture.
plt.show()

# %% Your turn
# 1. Add a bar chart: average performance per department.
# 2. Draw a line chart of cumulative hires by year.
# 3. Show male vs female average salary per department as grouped bars.

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================
# (nothing rare here, everything above is core)
