# Scatter plots: relationship between two numbers.

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

DATA = Path("data") if Path("data").exists() else Path("../data")
emp = pd.read_csv(DATA / "03_employees.csv")

# %% Basic
fig, ax = plt.subplots()
ax.scatter(emp["age"], emp["salary"])
ax.set_xlabel("Age")
ax.set_ylabel("Salary")
plt.show()

# %% Size and colour by values (bubble chart)
fig, ax = plt.subplots(figsize=(8, 5))
points = ax.scatter(
    emp["age"],
    emp["salary"],
    s=emp["performance_score"] ** 3,       # bubble size
    c=emp["performance_score"],            # colour scale
    cmap="viridis",
    alpha=0.7,
    edgecolor="black",
)
fig.colorbar(points, ax=ax, label="Performance")
plt.show()

# %% Colour by category
fig, ax = plt.subplots()
for dept, group in emp.groupby("department"):
    ax.scatter(group["age"], group["salary"], label=dept)
ax.legend()
plt.show()

# %% Trend line
slope, intercept = np.polyfit(emp["age"], emp["salary"], 1)
line_x = np.linspace(emp["age"].min(), emp["age"].max(), 50)
fig, ax = plt.subplots()
ax.scatter(emp["age"], emp["salary"], alpha=0.7)
ax.plot(line_x, slope * line_x + intercept, color="red", label=f"slope={slope:.0f}")
ax.legend()
plt.show()

# %% Label a few points
top = emp.nlargest(3, "salary")
fig, ax = plt.subplots()
ax.scatter(emp["age"], emp["salary"], alpha=0.5)
for _, row in top.iterrows():
    ax.annotate(row["name"], (row["age"], row["salary"]), xytext=(5, 5), textcoords="offset points")
plt.show()

# %% Marker styles
fig, ax = plt.subplots()
ax.scatter(emp["age"], emp["salary"], marker="D", s=40, color="purple", alpha=0.6)
plt.show()

# %% 2D histogram when there are too many points
rng = np.random.default_rng(0)
x = rng.normal(size=5000)
y = x + rng.normal(size=5000)
fig, ax = plt.subplots()
h = ax.hist2d(x, y, bins=40, cmap="magma")
fig.colorbar(h[3], ax=ax)
plt.show()

fig, ax = plt.subplots()
ax.hexbin(x, y, gridsize=30, cmap="Blues")
plt.show()
