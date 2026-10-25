# Bar charts: compare categories.

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

DATA = Path("data") if Path("data").exists() else Path("../data")
emp = pd.read_csv(DATA / "03_employees.csv")
avg = emp.groupby("department")["salary"].mean().sort_values(ascending=False)

# %% Vertical bars
fig, ax = plt.subplots()
ax.bar(avg.index, avg.values, color="tab:blue")
ax.set_title("Average salary by department")
ax.set_ylabel("Salary")
plt.show()

# %% Horizontal bars (better for long names)
fig, ax = plt.subplots()
ax.barh(avg.index, avg.values, color="tab:orange")
ax.invert_yaxis()                     # biggest on top
plt.show()

# %% Value labels on bars
fig, ax = plt.subplots()
bars = ax.bar(avg.index, avg.values)
ax.bar_label(bars, fmt="%.0f", padding=3)
ax.set_ylim(0, avg.max() * 1.15)
plt.show()

# %% Different colours per bar
colors = ["tab:red" if v == avg.max() else "lightgray" for v in avg.values]
fig, ax = plt.subplots()
ax.bar(avg.index, avg.values, color=colors, edgecolor="black")
plt.show()

# %% Grouped bars
table = emp.pivot_table(values="salary", index="department", columns="gender", aggfunc="mean")
x = np.arange(len(table))
width = 0.35
fig, ax = plt.subplots()
ax.bar(x - width / 2, table["F"], width, label="F")
ax.bar(x + width / 2, table["M"], width, label="M")
ax.set_xticks(x, table.index)
ax.legend()
plt.show()

# %% Stacked bars
counts = pd.crosstab(emp["department"], emp["gender"])
fig, ax = plt.subplots()
ax.bar(counts.index, counts["F"], label="F")
ax.bar(counts.index, counts["M"], bottom=counts["F"], label="M")
ax.legend()
plt.show()

# %% Error bars
spread = emp.groupby("department")["salary"].agg(["mean", "std"])
fig, ax = plt.subplots()
ax.bar(spread.index, spread["mean"], yerr=spread["std"], capsize=5, alpha=0.7)
plt.show()

# %% Count bars (like value_counts)
counts = emp["department"].value_counts()
fig, ax = plt.subplots()
ax.bar(counts.index, counts.values)
ax.tick_params(axis="x", rotation=30)
plt.show()

# %% Lollipop and step variations
fig, ax = plt.subplots()
ax.stem(avg.index, avg.values)
plt.show()
