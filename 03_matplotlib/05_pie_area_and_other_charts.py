# More chart types.
# Each line has a short comment saying WHAT the function is.

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Path("data").exists(): True if that folder exists; otherwise use ../data.
DATA = Path("data") if Path("data").exists() else Path("../data")
# pd.read_csv(file): loads a CSV into a table. parse_dates=[col]: reads that column as dates.
monthly = pd.read_csv(DATA / "04_monthly_sales.csv", parse_dates=["month"])
emp = pd.read_csv(DATA / "03_employees.csv")
# .value_counts(): how many times each department appears.
counts = emp["department"].value_counts()

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Pie chart
# plt.subplots(): makes the picture (fig) and one chart (ax).
fig, ax = plt.subplots()
# ax.pie(sizes): round chart cut into slices. labels: name per slice.
# autopct="%1.0f%%": prints each slice's percent on it. startangle=90: first slice starts at the top.
ax.pie(counts, labels=counts.index, autopct="%1.0f%%", startangle=90)
# ax.set_title(text): title above the chart.
ax.set_title("People per department")
# plt.show(): displays the chart.
plt.show()

# %% Stacked area
# figsize=(w, h): chart size in inches.
fig, ax = plt.subplots(figsize=(8, 4))
# ax.stackplot(x, y1, y2, y3): coloured areas piled on top of each other over time.
# labels: legend names in order. alpha=0.8: slightly see-through.
ax.stackplot(monthly["month"], monthly["electronics"], monthly["clothing"], monthly["furniture"],
             labels=["Electronics", "Clothing", "Furniture"], alpha=0.8)
# ax.legend(loc=...): box naming each area; loc is where it sits.
ax.legend(loc="upper left")
plt.show()

# %% Fill between two lines
fig, ax = plt.subplots()
# ax.plot(x, y): draws a line. label: legend name.
ax.plot(monthly["month"], monthly["electronics"], label="Electronics")
ax.plot(monthly["month"], monthly["clothing"], label="Clothing")
# ax.fill_between(x, y1, y2): colours the gap between two lines (light, alpha=0.2).
ax.fill_between(monthly["month"], monthly["electronics"], monthly["clothing"], alpha=0.2)
ax.legend()
plt.show()

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Donut and pulled slice
fig, ax = plt.subplots()
# wedgeprops={"width": 0.4}: makes slices thin rings, so the middle is a hole (donut).
# explode=[...]: how far each slice is pulled out (0.08 = first slice sticks out).
ax.pie(counts, labels=counts.index, autopct="%1.0f%%", wedgeprops={"width": 0.4},
       explode=[0.08, 0, 0, 0, 0])
plt.show()

# %% Step plot
fig, ax = plt.subplots()
# ax.step(x, y): staircase line (flat, then jump). where="mid": jump happens halfway between points.
ax.step(monthly["month"], monthly["visitors"], where="mid")
plt.show()

# %% Stem plot
fig, ax = plt.subplots()
# np.arange(8): numbers 0..7. ax.stem(x, y): a thin stick with a dot on top for each point.
ax.stem(np.arange(8), np.arange(8) ** 2)
plt.show()

# %% Error bars on a line
x = np.arange(5)
fig, ax = plt.subplots()
# ax.errorbar(x, y, yerr=...): points with +/- whiskers showing uncertainty.
# fmt="o-": dots joined by a line. capsize=4: width of whisker caps.
ax.errorbar(x, x**2, yerr=[1, 2, 1.5, 3, 2], fmt="o-", capsize=4)
plt.show()

# %% Polar / radar style
# np.linspace(a, b, n): n evenly spaced numbers; here angles around a full circle (2*pi radians).
angles = np.linspace(0, 2 * np.pi, 6)
values = np.array([4, 3, 5, 2, 4, 4])
# subplot_kw={"projection": "polar"}: makes the chart round (angle + distance from centre).
fig, ax = plt.subplots(subplot_kw={"projection": "polar"})
ax.plot(angles, values)
# ax.fill(x, y): colours inside the shape (alpha=0.3 = light).
ax.fill(angles, values, alpha=0.3)
plt.show()

# %% Quiver (arrows) and streamplot (flow)
# np.meshgrid(x, y): turns two lists into a grid of x and y coordinates (10 x 10 points).
gx, gy = np.meshgrid(np.linspace(-2, 2, 10), np.linspace(-2, 2, 10))
fig, ax = plt.subplots()
# ax.quiver(x, y, dx, dy): draws an arrow at each grid point pointing (dx, dy); here they swirl.
ax.quiver(gx, gy, -gy, gx)
plt.show()

# %% Stairs, eventplot, broken bars
fig, ax = plt.subplots()
# ax.stairs(values): step outline where each value is a flat level.
ax.stairs([1, 3, 2, 4])
plt.show()

fig, ax = plt.subplots()
# ax.eventplot(lists): one row of short tick marks per list (shows when events happen).
ax.eventplot([[1, 2, 5], [2, 3, 7]])
plt.show()

fig, ax = plt.subplots()
# ax.broken_barh([(start, length), ...], (y, height)): horizontal bars with gaps (like a timeline).
ax.broken_barh([(10, 20), (40, 10)], (5, 4))
plt.show()

# %% Candlestick-like range bars
fig, ax = plt.subplots()
# ax.vlines(x, ymin, ymax): vertical lines from ymin to ymax; linewidth=6 makes them thick bars.
ax.vlines(x=np.arange(5), ymin=[1, 2, 1, 3, 2], ymax=[4, 5, 3, 6, 5], linewidth=6)
plt.show()
