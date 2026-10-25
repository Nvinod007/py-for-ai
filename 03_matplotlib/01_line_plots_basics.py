# Matplotlib: the base of almost every Python chart.
# fig = the whole picture, ax = one chart inside it.

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

DATA = Path("data") if Path("data").exists() else Path("../data")
monthly = pd.read_csv(DATA / "04_monthly_sales.csv", parse_dates=["month"])

# %% Simplest plot
plt.plot([1, 2, 3, 4], [10, 20, 15, 30])
plt.show()

# %% Proper style: create fig and ax yourself (use this from now on)
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(monthly["month"], monthly["electronics"])
ax.set_title("Electronics sales 2023")
ax.set_xlabel("Month")
ax.set_ylabel("Sales ($)")
plt.show()

# %% Several lines + legend
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(monthly["month"], monthly["electronics"], label="Electronics")
ax.plot(monthly["month"], monthly["clothing"], label="Clothing")
ax.plot(monthly["month"], monthly["furniture"], label="Furniture")
ax.legend(loc="upper left")
ax.grid(True, alpha=0.3)
plt.show()

# %% Line style, colour, marker, width
x = np.arange(5)
fig, ax = plt.subplots()
ax.plot(x, x, color="red", linestyle="-", marker="o", linewidth=2, markersize=8, label="solid")
ax.plot(x, x + 1, color="#2a9d8f", linestyle="--", marker="s", label="dashed")
ax.plot(x, x + 2, color="tab:blue", linestyle=":", marker="^", label="dotted")
ax.plot(x, x + 3, "g-.", label="dash-dot")      # shortcut: colour + style
ax.plot(x, x + 4, "m*--", label="shortcut")
ax.legend()
plt.show()

# %% Axis limits, ticks, scale
fig, ax = plt.subplots()
ax.plot(np.arange(1, 100), np.arange(1, 100) ** 2)
ax.set_xlim(0, 50)
ax.set_ylim(0, 3000)
ax.set_xticks([0, 10, 20, 30, 40, 50])
ax.set_yscale("linear")       # try "log"
plt.show()

# %% Math curves
t = np.linspace(0, 2 * np.pi, 200)
fig, ax = plt.subplots()
ax.plot(t, np.sin(t), label="sin")
ax.plot(t, np.cos(t), label="cos")
ax.axhline(0, color="black", linewidth=0.8)
ax.legend()
plt.show()

# %% Transparent fill under a line
fig, ax = plt.subplots()
ax.plot(monthly["month"], monthly["electronics"], color="tab:blue")
ax.fill_between(monthly["month"], monthly["electronics"], alpha=0.2)
plt.show()

# %% Mark special points
best = monthly.loc[monthly["electronics"].idxmax()]
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(monthly["month"], monthly["electronics"])
ax.scatter(best["month"], best["electronics"], color="red", zorder=3)
ax.annotate("Best month", xy=(best["month"], best["electronics"]),
            xytext=(-90, -10), textcoords="offset points",
            arrowprops={"arrowstyle": "->"})
plt.show()

# %% Rotate dates and save to a file
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(monthly["month"], monthly["visitors"])
fig.autofmt_xdate()
out = DATA / "output"
out.mkdir(exist_ok=True)
fig.savefig(out / "visitors.png", dpi=150, bbox_inches="tight")
plt.show()
