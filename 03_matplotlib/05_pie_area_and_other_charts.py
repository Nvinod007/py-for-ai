# More chart types.

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

DATA = Path("data") if Path("data").exists() else Path("../data")
monthly = pd.read_csv(DATA / "04_monthly_sales.csv", parse_dates=["month"])
emp = pd.read_csv(DATA / "03_employees.csv")
counts = emp["department"].value_counts()

# %% Pie chart
fig, ax = plt.subplots()
ax.pie(counts, labels=counts.index, autopct="%1.0f%%", startangle=90)
ax.set_title("People per department")
plt.show()

# %% Donut and pulled slice
fig, ax = plt.subplots()
ax.pie(counts, labels=counts.index, autopct="%1.0f%%", wedgeprops={"width": 0.4},
       explode=[0.08, 0, 0, 0, 0])
plt.show()

# %% Stacked area
fig, ax = plt.subplots(figsize=(8, 4))
ax.stackplot(monthly["month"], monthly["electronics"], monthly["clothing"], monthly["furniture"],
             labels=["Electronics", "Clothing", "Furniture"], alpha=0.8)
ax.legend(loc="upper left")
plt.show()

# %% Fill between two lines
fig, ax = plt.subplots()
ax.plot(monthly["month"], monthly["electronics"], label="Electronics")
ax.plot(monthly["month"], monthly["clothing"], label="Clothing")
ax.fill_between(monthly["month"], monthly["electronics"], monthly["clothing"], alpha=0.2)
ax.legend()
plt.show()

# %% Step plot
fig, ax = plt.subplots()
ax.step(monthly["month"], monthly["visitors"], where="mid")
plt.show()

# %% Stem plot
fig, ax = plt.subplots()
ax.stem(np.arange(8), np.arange(8) ** 2)
plt.show()

# %% Error bars on a line
x = np.arange(5)
fig, ax = plt.subplots()
ax.errorbar(x, x**2, yerr=[1, 2, 1.5, 3, 2], fmt="o-", capsize=4)
plt.show()

# %% Polar / radar style
angles = np.linspace(0, 2 * np.pi, 6)
values = np.array([4, 3, 5, 2, 4, 4])
fig, ax = plt.subplots(subplot_kw={"projection": "polar"})
ax.plot(angles, values)
ax.fill(angles, values, alpha=0.3)
plt.show()

# %% Quiver (arrows) and streamplot (flow)
gx, gy = np.meshgrid(np.linspace(-2, 2, 10), np.linspace(-2, 2, 10))
fig, ax = plt.subplots()
ax.quiver(gx, gy, -gy, gx)
plt.show()

# %% Stairs, eventplot, broken bars
fig, ax = plt.subplots()
ax.stairs([1, 3, 2, 4])
plt.show()

fig, ax = plt.subplots()
ax.eventplot([[1, 2, 5], [2, 3, 7]])
plt.show()

fig, ax = plt.subplots()
ax.broken_barh([(10, 20), (40, 10)], (5, 4))
plt.show()

# %% Candlestick-like range bars
fig, ax = plt.subplots()
ax.vlines(x=np.arange(5), ymin=[1, 2, 1, 3, 2], ymax=[4, 5, 3, 6, 5], linewidth=6)
plt.show()
