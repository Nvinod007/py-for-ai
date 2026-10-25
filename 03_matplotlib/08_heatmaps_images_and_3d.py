# Grids of numbers, pictures, contours, and 3D.
# Each line has a short comment saying WHAT the function is.

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Path("data").exists(): True if that folder exists; otherwise use ../data.
DATA = Path("data") if Path("data").exists() else Path("../data")
# pd.read_csv(file): loads a CSV into a table.
emp = pd.read_csv(DATA / "03_employees.csv")

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Heatmap of a correlation table
# .corr(): table of how strongly each pair of columns moves together (-1 to 1).
corr = emp[["age", "salary", "performance_score"]].corr()
# plt.subplots(): makes the picture (fig) and one chart (ax).
fig, ax = plt.subplots()
# ax.imshow(grid): shows numbers as coloured squares. cmap="coolwarm": blue low, red high.
# vmin / vmax: numbers that map to the lowest / highest colour.
im = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
# ax.set_xticks(positions, names) / set_yticks: put column names on the axes.
ax.set_xticks(range(len(corr)), corr.columns)
ax.set_yticks(range(len(corr)), corr.columns)
for i in range(len(corr)):
    for j in range(len(corr)):
        # ax.text(x, y, text): writes the number inside the square. ha / va = centre it.
        # .iloc[i, j]: the table cell at row i, column j. :.2f = 2 decimals.
        ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center")
# fig.colorbar(im, ax=ax): side strip showing what each colour means.
fig.colorbar(im, ax=ax)
# plt.show(): displays the chart.
plt.show()

# %% Heatmap of counts
# pd.crosstab(a, b): counts rows for each pair (department x gender).
table = pd.crosstab(emp["department"], emp["gender"])
fig, ax = plt.subplots()
# ax.pcolormesh(grid): coloured cells (darker blue = bigger count).
ax.pcolormesh(table.values, cmap="Blues")
# np.arange(n) + 0.5: puts the name in the middle of each cell. .shape: (rows, columns).
ax.set_xticks(np.arange(table.shape[1]) + 0.5, table.columns)
ax.set_yticks(np.arange(table.shape[0]) + 0.5, table.index)
plt.show()

# %% Show an array as an image
# np.random.default_rng(0): random number maker; 0 = fixed seed so results repeat.
rng = np.random.default_rng(0)
# rng.random((20, 20)): 20x20 grid of random numbers between 0 and 1 (like pixels).
pixels = rng.random((20, 20))
fig, axes = plt.subplots(1, 3, figsize=(10, 3))      # 1 row, 3 charts
# cmap="gray": black-to-white shades.
axes[0].imshow(pixels, cmap="gray")
# interpolation="nearest": sharp square pixels.
axes[1].imshow(pixels, cmap="viridis", interpolation="nearest")
# interpolation="bilinear": smooth blurry blend between pixels. cmap="hot": black-red-yellow.
axes[2].imshow(pixels, cmap="hot", interpolation="bilinear")
plt.show()

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Contour plots
# np.linspace(a, b, n): n evenly spaced numbers from a to b.
x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
# np.meshgrid(x, y): turns two lists into a grid of x and y coordinates.
xx, yy = np.meshgrid(x, y)
# np.exp: e to the power. This builds a height (zz) with two smooth hills.
zz = np.exp(-(xx**2 + yy**2)) + 0.5 * np.exp(-((xx - 1.5) ** 2 + (yy + 1) ** 2))
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
# ax.contour(x, y, z, levels=n): outline lines of equal height, like a map. levels: number of lines.
lines = axes[0].contour(xx, yy, zz, levels=8)
# ax.clabel(lines): writes the height value on each line. inline=True: cuts the line behind text.
axes[0].clabel(lines, inline=True, fontsize=8)
# ax.contourf(...): same as contour but the areas between lines are filled with colour.
filled = axes[1].contourf(xx, yy, zz, levels=12, cmap="viridis")
fig.colorbar(filled, ax=axes[1])
plt.show()

# %% 3D surface
# plt.figure(figsize=(w, h)): an empty picture.
fig = plt.figure(figsize=(7, 5))
# fig.add_subplot(projection="3d"): adds a 3D chart (x, y, z).
ax = fig.add_subplot(projection="3d")
# ax.plot_surface(x, y, z): draws a coloured 3D hill-like sheet.
ax.plot_surface(xx, yy, zz, cmap="viridis")
ax.set_xlabel("x")          # name of the x axis
ax.set_ylabel("y")          # name of the y axis
# ax.set_zlabel(text): name of the vertical (z) axis.
ax.set_zlabel("z")
plt.show()

# %% 3D scatter and line
fig = plt.figure()
ax = fig.add_subplot(projection="3d")
# ax.scatter(x, y, z): dots floating in 3D. c=...: colour from salary. cmap="plasma": purple-to-yellow.
ax.scatter(emp["age"], emp["performance_score"], emp["salary"], c=emp["salary"], cmap="plasma")
ax.set_xlabel("Age")
ax.set_ylabel("Performance")
ax.set_zlabel("Salary")
plt.show()

t = np.linspace(0, 10, 200)
fig = plt.figure()
ax = fig.add_subplot(projection="3d")
# ax.plot(x, y, z): a 3D line; cos and sin make circles while t rises, so it draws a spiral.
ax.plot(np.cos(t), np.sin(t), t)
plt.show()

# %% Wireframe
fig = plt.figure()
ax = fig.add_subplot(projection="3d")
# [::5, ::5]: take every 5th row and column (fewer lines). plot_wireframe: 3D net of lines.
ax.plot_wireframe(xx[::5, ::5], yy[::5, ::5], zz[::5, ::5])
plt.show()

# %% Colour maps to try
# A plain list of colour scale names you can pass to cmap=.
print(["viridis", "plasma", "inferno", "magma", "cividis", "coolwarm", "RdYlBu", "Blues", "Greens"])
