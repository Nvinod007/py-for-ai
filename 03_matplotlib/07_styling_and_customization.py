# Make charts clear and good looking.

from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd

DATA = Path("data") if Path("data").exists() else Path("../data")
m = pd.read_csv(DATA / "04_monthly_sales.csv", parse_dates=["month"])

# %% Built-in styles
print(plt.style.available[:8])
with plt.style.context("ggplot"):
    fig, ax = plt.subplots()
    ax.plot(m["month"], m["electronics"])
    plt.show()

# %% Global defaults
plt.rcParams.update(
    {
        "figure.figsize": (8, 4),
        "axes.titlesize": 14,
        "axes.labelsize": 11,
        "axes.spines.top": False,
        "axes.spines.right": False,
        "font.size": 10,
        "lines.linewidth": 2,
    }
)
fig, ax = plt.subplots()
ax.plot(m["month"], m["electronics"])
plt.show()
plt.rcdefaults()

# %% Title and label details
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(m["month"], m["electronics"])
ax.set_title("Electronics", fontsize=16, fontweight="bold", loc="left", color="navy")
ax.set_xlabel("Month", fontsize=11, labelpad=10)
ax.set_ylabel("Sales ($)", rotation=90)
plt.show()

# %% Number formats on axes
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(m["month"], m["electronics"])
ax.yaxis.set_major_formatter(mticker.StrMethodFormatter("${x:,.0f}"))
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
ax.xaxis.set_major_locator(mdates.MonthLocator())
plt.show()

fig, ax = plt.subplots()
ax.plot([0, 0.5, 1], [0, 0.25, 1])
ax.yaxis.set_major_formatter(mticker.PercentFormatter(1.0))
plt.show()

# %% Ticks
fig, ax = plt.subplots()
ax.plot(range(10), np.arange(10) ** 2)
ax.set_xticks(range(0, 10, 2))
ax.set_xticklabels(["zero", "two", "four", "six", "eight"])
ax.tick_params(axis="x", rotation=45, labelsize=9, length=6)
ax.minorticks_on()
plt.show()

# %% Text, lines, spans
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(m["month"], m["electronics"])
ax.axhline(m["electronics"].mean(), color="red", linestyle="--", label="average")
ax.axvline(pd.Timestamp("2023-11-01"), color="gray")
ax.axvspan(pd.Timestamp("2023-11-01"), pd.Timestamp("2023-12-31"), alpha=0.2, color="orange")
ax.text(pd.Timestamp("2023-02-01"), 28000, "Holiday season ->", fontsize=10)
ax.axhspan(10000, 15000, alpha=0.1)
ax.legend()
plt.show()

# %% Remove clutter (spines and grid)
fig, ax = plt.subplots()
ax.plot(m["month"], m["electronics"])
ax.spines[["top", "right"]].set_visible(False)
ax.grid(axis="y", linestyle=":", alpha=0.5)
ax.set_axisbelow(True)
plt.show()

# %% Colours
print(plt.cm.viridis(0.5))
fig, ax = plt.subplots()
colors = plt.cm.viridis(np.linspace(0, 1, 5))
for i, c in enumerate(colors):
    ax.bar(i, i + 1, color=c)
plt.show()
print(plt.rcParams["axes.prop_cycle"].by_key()["color"][:4])

# %% Legend details
fig, ax = plt.subplots()
ax.plot(m["month"], m["electronics"], label="Electronics")
ax.plot(m["month"], m["clothing"], label="Clothing")
ax.legend(title="Category", loc="upper left", ncol=2, frameon=False, bbox_to_anchor=(0, 1.15))
plt.show()

# %% Figure size, dpi, background
fig, ax = plt.subplots(figsize=(10, 3), dpi=100, facecolor="whitesmoke")
ax.plot(m["month"], m["visitors"])
plt.show()

# %% Save in different formats
out = DATA / "output"
out.mkdir(exist_ok=True)
fig.savefig(out / "chart.png", dpi=200, bbox_inches="tight")
fig.savefig(out / "chart.pdf")
fig.savefig(out / "chart.svg")
fig.savefig(out / "chart_transparent.png", transparent=True)
