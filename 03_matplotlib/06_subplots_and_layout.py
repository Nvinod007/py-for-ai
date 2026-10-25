# Many charts in one picture.

from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
import numpy as np
import pandas as pd

DATA = Path("data") if Path("data").exists() else Path("../data")
m = pd.read_csv(DATA / "04_monthly_sales.csv", parse_dates=["month"])
emp = pd.read_csv(DATA / "03_employees.csv")

# %% Side by side
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4))
ax1.plot(m["month"], m["electronics"])
ax1.set_title("Electronics")
ax2.plot(m["month"], m["clothing"], color="orange")
ax2.set_title("Clothing")
fig.suptitle("Sales")
fig.tight_layout()
plt.show()

# %% Grid of charts
fig, axes = plt.subplots(2, 2, figsize=(10, 7))
axes[0, 0].plot(m["month"], m["electronics"])
axes[0, 1].bar(m["month"].dt.month, m["clothing"])
axes[1, 0].hist(emp["salary"], bins=8)
axes[1, 1].scatter(emp["age"], emp["salary"])
for ax in axes.flat:
    ax.grid(alpha=0.3)
fig.tight_layout()
plt.show()

# %% Share an axis
fig, axes = plt.subplots(3, 1, sharex=True, figsize=(8, 7))
for ax, column in zip(axes, ["electronics", "clothing", "furniture"]):
    ax.plot(m["month"], m[column])
    ax.set_ylabel(column)
fig.tight_layout()
plt.show()

fig, axes = plt.subplots(1, 3, sharey=True, figsize=(12, 3))
for ax, column in zip(axes, ["electronics", "clothing", "furniture"]):
    ax.bar(m["month"].dt.month, m[column])
    ax.set_title(column)
plt.show()

# %% Two y-axes on one chart
fig, ax1 = plt.subplots(figsize=(8, 4))
ax1.bar(m["month"], m["electronics"], width=20, alpha=0.5, label="sales")
ax1.set_ylabel("Sales")
ax2 = ax1.twinx()
ax2.plot(m["month"], m["visitors"], color="red", marker="o")
ax2.set_ylabel("Visitors")
plt.show()

# %% Uneven layout with GridSpec
fig = plt.figure(figsize=(9, 6))
gs = GridSpec(2, 3, figure=fig)
big = fig.add_subplot(gs[0, :])           # top row, all columns
big.plot(m["month"], m["electronics"])
left = fig.add_subplot(gs[1, 0])
left.hist(emp["age"])
right = fig.add_subplot(gs[1, 1:])        # bottom row, last two columns
right.scatter(emp["age"], emp["salary"])
fig.tight_layout()
plt.show()

# %% Mosaic: draw the layout as text
fig, axd = plt.subplot_mosaic([["top", "top"], ["left", "right"]], figsize=(8, 6))
axd["top"].plot(m["month"], m["visitors"])
axd["left"].bar(["a", "b"], [3, 4])
axd["right"].pie([1, 2, 3])
plt.show()

# %% Chart inside a chart
fig, ax = plt.subplots()
ax.plot(m["month"], m["electronics"])
inset = ax.inset_axes((0.1, 0.55, 0.35, 0.35))
inset.hist(m["electronics"], bins=5)
plt.show()

# %% Spacing control
fig, axes = plt.subplots(2, 2)
fig.subplots_adjust(hspace=0.5, wspace=0.3)
plt.show()

fig, axes = plt.subplots(2, 2, layout="constrained")     # automatic spacing
plt.show()

# %% Many small charts quickly
fig, axes = plt.subplots(1, 5, figsize=(14, 2), sharey=True)
for ax, (dept, group) in zip(axes, emp.groupby("department")):
    ax.hist(group["salary"], bins=4)
    ax.set_title(dept)
plt.show()
