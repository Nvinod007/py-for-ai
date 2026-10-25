# Grids of numbers, pictures, contours, and 3D.

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

DATA = Path("data") if Path("data").exists() else Path("../data")
emp = pd.read_csv(DATA / "03_employees.csv")

# %% Heatmap of a correlation table
corr = emp[["age", "salary", "performance_score"]].corr()
fig, ax = plt.subplots()
im = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
ax.set_xticks(range(len(corr)), corr.columns)
ax.set_yticks(range(len(corr)), corr.columns)
for i in range(len(corr)):
    for j in range(len(corr)):
        ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center")
fig.colorbar(im, ax=ax)
plt.show()

# %% Heatmap of counts
table = pd.crosstab(emp["department"], emp["gender"])
fig, ax = plt.subplots()
ax.pcolormesh(table.values, cmap="Blues")
ax.set_xticks(np.arange(table.shape[1]) + 0.5, table.columns)
ax.set_yticks(np.arange(table.shape[0]) + 0.5, table.index)
plt.show()

# %% Show an array as an image
rng = np.random.default_rng(0)
pixels = rng.random((20, 20))
fig, axes = plt.subplots(1, 3, figsize=(10, 3))
axes[0].imshow(pixels, cmap="gray")
axes[1].imshow(pixels, cmap="viridis", interpolation="nearest")
axes[2].imshow(pixels, cmap="hot", interpolation="bilinear")
plt.show()

# %% Contour plots
x = np.linspace(-3, 3, 100)
y = np.linspace(-3, 3, 100)
xx, yy = np.meshgrid(x, y)
zz = np.exp(-(xx**2 + yy**2)) + 0.5 * np.exp(-((xx - 1.5) ** 2 + (yy + 1) ** 2))
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
lines = axes[0].contour(xx, yy, zz, levels=8)
axes[0].clabel(lines, inline=True, fontsize=8)
filled = axes[1].contourf(xx, yy, zz, levels=12, cmap="viridis")
fig.colorbar(filled, ax=axes[1])
plt.show()

# %% 3D surface
fig = plt.figure(figsize=(7, 5))
ax = fig.add_subplot(projection="3d")
ax.plot_surface(xx, yy, zz, cmap="viridis")
ax.set_xlabel("x")
ax.set_ylabel("y")
ax.set_zlabel("z")
plt.show()

# %% 3D scatter and line
fig = plt.figure()
ax = fig.add_subplot(projection="3d")
ax.scatter(emp["age"], emp["performance_score"], emp["salary"], c=emp["salary"], cmap="plasma")
ax.set_xlabel("Age")
ax.set_ylabel("Performance")
ax.set_zlabel("Salary")
plt.show()

t = np.linspace(0, 10, 200)
fig = plt.figure()
ax = fig.add_subplot(projection="3d")
ax.plot(np.cos(t), np.sin(t), t)
plt.show()

# %% Wireframe
fig = plt.figure()
ax = fig.add_subplot(projection="3d")
ax.plot_wireframe(xx[::5, ::5], yy[::5, ::5], zz[::5, ::5])
plt.show()

# %% Colour maps to try
print(["viridis", "plasma", "inferno", "magma", "cividis", "coolwarm", "RdYlBu", "Blues", "Greens"])
