# Make charts clear and good looking.
# Each line has a short comment saying WHAT the function is.

from pathlib import Path

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np
import pandas as pd

# Path("data").exists(): True if that folder exists; otherwise use ../data.
DATA = Path("data") if Path("data").exists() else Path("../data")
# pd.read_csv(file): loads a CSV into a table. parse_dates=[col]: reads that column as dates.
m = pd.read_csv(DATA / "04_monthly_sales.csv", parse_dates=["month"])

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Title and label details
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(m["month"], m["electronics"])
# ax.set_title(text, ...): fontsize = text size, fontweight="bold" = thick text,
# loc="left" = title at the left edge, color = text colour.
ax.set_title("Electronics", fontsize=16, fontweight="bold", loc="left", color="navy")
# ax.set_xlabel(text): name under the x axis. labelpad=10: gap between axis and name.
ax.set_xlabel("Month", fontsize=11, labelpad=10)
# ax.set_ylabel(text): name beside the y axis. rotation=90: text reads bottom to top.
ax.set_ylabel("Sales ($)", rotation=90)
plt.show()

# %% Number formats on axes
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(m["month"], m["electronics"])
# ax.yaxis.set_major_formatter(...): controls how y numbers are written.
# mticker.StrMethodFormatter("${x:,.0f}"): shows like $12,000 (dollar sign, commas, no decimals).
ax.yaxis.set_major_formatter(mticker.StrMethodFormatter("${x:,.0f}"))
# mdates.DateFormatter("%b"): shows dates as short month names (Jan, Feb...).
ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
# mdates.MonthLocator(): puts one x tick at the start of every month.
ax.xaxis.set_major_locator(mdates.MonthLocator())
plt.show()

fig, ax = plt.subplots()
ax.plot([0, 0.5, 1], [0, 0.25, 1])
# mticker.PercentFormatter(1.0): shows 0.5 as 50% (1.0 means "1 = 100%").
ax.yaxis.set_major_formatter(mticker.PercentFormatter(1.0))
plt.show()

# %% Ticks
fig, ax = plt.subplots()
# range(10): 0..9. np.arange(10) ** 2: squares of those numbers.
ax.plot(range(10), np.arange(10) ** 2)
# ax.set_xticks(list): where x tick marks appear (every 2).
ax.set_xticks(range(0, 10, 2))
# ax.set_xticklabels(list): the text shown at each tick.
ax.set_xticklabels(["zero", "two", "four", "six", "eight"])
# ax.tick_params(...): styles ticks. rotation=45: tilt labels. labelsize: text size. length: tick length.
ax.tick_params(axis="x", rotation=45, labelsize=9, length=6)
# ax.minorticks_on(): adds small extra tick marks between the big ones.
ax.minorticks_on()
plt.show()

# %% Legend details
fig, ax = plt.subplots()
# label="...": legend name for this line.
ax.plot(m["month"], m["electronics"], label="Electronics")
ax.plot(m["month"], m["clothing"], label="Clothing")
# ax.legend(...): title = heading of the box. loc = position. ncol=2: two columns.
# frameon=False: no border. bbox_to_anchor=(0, 1.15): moves the box above the chart.
ax.legend(title="Category", loc="upper left", ncol=2, frameon=False, bbox_to_anchor=(0, 1.15))
plt.show()

# %% Figure size, dpi, background
# figsize: size in inches. dpi: dots per inch (sharpness). facecolor: background colour.
fig, ax = plt.subplots(figsize=(10, 3), dpi=100, facecolor="whitesmoke")
ax.plot(m["month"], m["visitors"])
plt.show()

# %% Save in different formats
out = DATA / "output"
# out.mkdir(exist_ok=True): creates the folder (no error if it already exists).
out.mkdir(exist_ok=True)
# fig.savefig(file): saves the picture; the file ending (.png/.pdf/.svg) picks the format.
# dpi=200: sharper image. bbox_inches="tight": trims white borders.
fig.savefig(out / "chart.png", dpi=200, bbox_inches="tight")
fig.savefig(out / "chart.pdf")
fig.savefig(out / "chart.svg")
# transparent=True: no background colour (see-through picture).
fig.savefig(out / "chart_transparent.png", transparent=True)

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Built-in styles
# plt.style.available: list of ready-made look names (we show the first 8).
print(plt.style.available[:8])
# plt.style.context("ggplot"): uses that look only inside this "with" block.
with plt.style.context("ggplot"):
    # plt.subplots(): makes the picture (fig) and one chart (ax).
    fig, ax = plt.subplots()
    # ax.plot(x, y): draws a line.
    ax.plot(m["month"], m["electronics"])
    # plt.show(): displays the chart.
    plt.show()

# %% Global defaults
# plt.rcParams.update({...}): changes default settings for every chart that follows.
plt.rcParams.update(
    {
        "figure.figsize": (8, 4),       # default chart size (inches)
        "axes.titlesize": 14,           # title text size
        "axes.labelsize": 11,           # axis name text size
        "axes.spines.top": False,       # hide the top border line
        "axes.spines.right": False,     # hide the right border line
        "font.size": 10,                # default text size
        "lines.linewidth": 2,           # default line thickness
    }
)
fig, ax = plt.subplots()
ax.plot(m["month"], m["electronics"])
plt.show()
# plt.rcdefaults(): puts all settings back to matplotlib's original defaults.
plt.rcdefaults()

# %% Text, lines, spans
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(m["month"], m["electronics"])
# ax.axhline(y): horizontal line across the chart (here at the average). linestyle="--": dashed.
ax.axhline(m["electronics"].mean(), color="red", linestyle="--", label="average")
# ax.axvline(x): vertical line at x. pd.Timestamp("2023-11-01"): a date value.
ax.axvline(pd.Timestamp("2023-11-01"), color="gray")
# ax.axvspan(x1, x2): shaded vertical band between two x values (light orange).
ax.axvspan(pd.Timestamp("2023-11-01"), pd.Timestamp("2023-12-31"), alpha=0.2, color="orange")
# ax.text(x, y, text): writes text at that spot on the chart.
ax.text(pd.Timestamp("2023-02-01"), 28000, "Holiday season ->", fontsize=10)
# ax.axhspan(y1, y2): shaded horizontal band between two y values.
ax.axhspan(10000, 15000, alpha=0.1)
# ax.legend(): box naming the labelled lines.
ax.legend()
plt.show()

# %% Remove clutter (spines and grid)
fig, ax = plt.subplots()
ax.plot(m["month"], m["electronics"])
# ax.spines: the four border lines of the chart. set_visible(False) hides top and right.
ax.spines[["top", "right"]].set_visible(False)
# ax.grid(axis="y", ...): grid lines only for y. linestyle=":": dotted. alpha: see-through.
ax.grid(axis="y", linestyle=":", alpha=0.5)
# ax.set_axisbelow(True): puts the grid behind the data.
ax.set_axisbelow(True)
plt.show()

# %% Colours
# plt.cm.viridis(0.5): the colour at the middle (0 to 1) of the viridis scale, as (R, G, B, A).
print(plt.cm.viridis(0.5))
fig, ax = plt.subplots()
# np.linspace(0, 1, 5): 5 evenly spaced numbers, so we get 5 colours from viridis.
colors = plt.cm.viridis(np.linspace(0, 1, 5))
# enumerate(list): gives (position, item) pairs.
for i, c in enumerate(colors):
    # ax.bar(x, height, color=c): one bar in colour c.
    ax.bar(i, i + 1, color=c)
plt.show()
# plt.rcParams["axes.prop_cycle"]: the default colour order matplotlib uses; we print the first 4.
print(plt.rcParams["axes.prop_cycle"].by_key()["color"][:4])
