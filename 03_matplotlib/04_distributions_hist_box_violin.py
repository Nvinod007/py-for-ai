# Show how values are spread out.

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

DATA = Path("data") if Path("data").exists() else Path("../data")
emp = pd.read_csv(DATA / "03_employees.csv")

# %% Histogram
fig, ax = plt.subplots()
ax.hist(emp["salary"], bins=8, color="skyblue", edgecolor="black")
ax.set_xlabel("Salary")
ax.set_ylabel("People")
plt.show()

# %% Histogram options
fig, ax = plt.subplots()
ax.hist(emp["salary"], bins=[40000, 60000, 80000, 100000, 140000], density=True, alpha=0.7)
ax.axvline(emp["salary"].mean(), color="red", linestyle="--", label="mean")
ax.axvline(emp["salary"].median(), color="green", linestyle="--", label="median")
ax.legend()
plt.show()

# %% Compare two groups
fig, ax = plt.subplots()
ax.hist(emp[emp["gender"] == "F"]["salary"], bins=8, alpha=0.6, label="F")
ax.hist(emp[emp["gender"] == "M"]["salary"], bins=8, alpha=0.6, label="M")
ax.legend()
plt.show()

# %% Cumulative
fig, ax = plt.subplots()
ax.hist(emp["salary"], bins=10, cumulative=True, histtype="step")
plt.show()

# %% Box plot
fig, ax = plt.subplots()
ax.boxplot(emp["salary"])
plt.show()

# %% Box plot per group
groups = [g["salary"].values for _, g in emp.groupby("department")]
labels = [name for name, _ in emp.groupby("department")]
fig, ax = plt.subplots()
ax.boxplot(groups, tick_labels=labels, patch_artist=True, showmeans=True)
ax.set_ylabel("Salary")
plt.show()

# %% Horizontal box plot
fig, ax = plt.subplots()
ax.boxplot(groups, tick_labels=labels, orientation="horizontal")
plt.show()

# %% Violin plot
fig, ax = plt.subplots()
ax.violinplot(groups, showmedians=True)
ax.set_xticks(range(1, len(labels) + 1), labels)
plt.show()

# %% Normal data for a bell curve
rng = np.random.default_rng(1)
data = rng.normal(100, 15, 2000)
fig, ax = plt.subplots()
ax.hist(data, bins=40, density=True, alpha=0.6)
xs = np.linspace(40, 160, 200)
ax.plot(xs, np.exp(-((xs - 100) ** 2) / (2 * 15**2)) / (15 * np.sqrt(2 * np.pi)), color="red")
plt.show()

# %% Histogram counts without drawing
counts, edges = np.histogram(emp["salary"], bins=5)
print(counts, edges)
