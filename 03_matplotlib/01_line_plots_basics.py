# Matplotlib: the base of almost every Python chart.
# fig = the whole picture, ax = one chart inside it.
# Each line has a short comment saying WHAT the function is.

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Path("data"): a folder path. .exists(): True if the folder is there.
DATA = Path("data") if Path("data").exists() else Path("../data")
# pd.read_csv(file): loads a CSV into a table. parse_dates=[col]: reads that column as dates.
monthly = pd.read_csv(DATA / "04_monthly_sales.csv", parse_dates=["month"])

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Simplest plot
# plt.plot(x, y): draws a line through the points (x list, y list).
plt.plot([1, 2, 3, 4], [10, 20, 15, 30])
# plt.show(): displays the chart on screen.
plt.show()

# %% Proper style: create fig and ax yourself (use this from now on)
# plt.subplots(figsize=(w, h)): makes the picture (fig) and one chart (ax); figsize is inches.
fig, ax = plt.subplots(figsize=(8, 4))
# ax.plot(x, y): draws a line on this chart (months across, sales up).
ax.plot(monthly["month"], monthly["electronics"])
# ax.set_title(text): big title above the chart.
ax.set_title("Electronics sales 2023")
# ax.set_xlabel(text): name under the x axis.
ax.set_xlabel("Month")
# ax.set_ylabel(text): name beside the y axis.
ax.set_ylabel("Sales ($)")
plt.show()

# %% Several lines + legend
fig, ax = plt.subplots(figsize=(8, 4))
# label="...": the name shown for this line in the legend.
ax.plot(monthly["month"], monthly["electronics"], label="Electronics")
ax.plot(monthly["month"], monthly["clothing"], label="Clothing")
ax.plot(monthly["month"], monthly["furniture"], label="Furniture")
# ax.legend(loc=...): small box naming each line; loc is where it sits.
ax.legend(loc="upper left")
# ax.grid(True, alpha=0.3): faint background grid lines; alpha = see-through (0 invisible, 1 solid).
ax.grid(True, alpha=0.3)
plt.show()

# %% Line style, colour, marker, width
# np.arange(5): array [0, 1, 2, 3, 4].
x = np.arange(5)
# plt.subplots(): with no arguments gives one chart of default size.
fig, ax = plt.subplots()
# color: line colour. linestyle "-": solid. marker "o": circle on each point.
# linewidth: line thickness. markersize: marker size.
ax.plot(x, x, color="red", linestyle="-", marker="o", linewidth=2, markersize=8, label="solid")
# color "#2a9d8f": hex code colour. linestyle "--": dashed. marker "s": square.
ax.plot(x, x + 1, color="#2a9d8f", linestyle="--", marker="s", label="dashed")
# color "tab:blue": a named matplotlib colour. linestyle ":": dotted. marker "^": triangle.
ax.plot(x, x + 2, color="tab:blue", linestyle=":", marker="^", label="dotted")
ax.plot(x, x + 3, "g-.", label="dash-dot")      # shortcut: colour + style
ax.plot(x, x + 4, "m*--", label="shortcut")     # m = magenta, * = star marker, -- = dashed
ax.legend()
plt.show()

# %% Rotate dates and save to a file
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(monthly["month"], monthly["visitors"])
# fig.autofmt_xdate(): tilts date labels so they do not overlap.
fig.autofmt_xdate()
out = DATA / "output"
# out.mkdir(exist_ok=True): creates the folder (no error if it already exists).
out.mkdir(exist_ok=True)
# fig.savefig(file): saves the picture. dpi = sharpness. bbox_inches="tight" trims white borders.
fig.savefig(out / "visitors.png", dpi=150, bbox_inches="tight")
plt.show()

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Axis limits, ticks, scale
fig, ax = plt.subplots()
ax.plot(np.arange(1, 100), np.arange(1, 100) ** 2)   # a curve that rises faster and faster
# ax.set_xlim(low, high): visible range of the x axis (zooms in).
ax.set_xlim(0, 50)
# ax.set_ylim(low, high): visible range of the y axis.
ax.set_ylim(0, 3000)
# ax.set_xticks(list): exact places where x tick marks/numbers appear.
ax.set_xticks([0, 10, 20, 30, 40, 50])
# ax.set_yscale(name): "linear" = normal spacing, "log" = each step is 10x bigger.
ax.set_yscale("linear")       # try "log"
plt.show()

# %% Math curves
# np.linspace(a, b, n): n evenly spaced numbers from a to b.  np.pi = 3.14159...
t = np.linspace(0, 2 * np.pi, 200)
fig, ax = plt.subplots()
# np.sin / np.cos: wave values for each t (two smooth waves).
ax.plot(t, np.sin(t), label="sin")
ax.plot(t, np.cos(t), label="cos")
# ax.axhline(y): draws a horizontal line across the whole chart at height y.
ax.axhline(0, color="black", linewidth=0.8)
ax.legend()
plt.show()

# %% Transparent fill under a line
fig, ax = plt.subplots()
ax.plot(monthly["month"], monthly["electronics"], color="tab:blue")
# ax.fill_between(x, y): colours the area between the line and zero; alpha=0.2 = very light.
ax.fill_between(monthly["month"], monthly["electronics"], alpha=0.2)
plt.show()

# %% Mark special points
# .idxmax(): row label of the biggest value. .loc[label]: get that whole row.
best = monthly.loc[monthly["electronics"].idxmax()]
fig, ax = plt.subplots(figsize=(8, 4))
ax.plot(monthly["month"], monthly["electronics"])
# ax.scatter(x, y): draws dots; zorder=3 puts the dot on top of the line.
ax.scatter(best["month"], best["electronics"], color="red", zorder=3)
# ax.annotate(text, xy=...): writes text with an arrow.
# xy = point the arrow touches. xytext = text position. textcoords="offset points": xytext is
# measured in points away from xy. arrowprops: arrow style (here a simple "->").
ax.annotate("Best month", xy=(best["month"], best["electronics"]),
            xytext=(-90, -10), textcoords="offset points",
            arrowprops={"arrowstyle": "->"})
plt.show()
