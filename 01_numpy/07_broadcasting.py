# Broadcasting = NumPy stretches smaller arrays so shapes can match.
# Rule: compare shapes from the right. Each pair must be equal or one must be 1.
# Each line has a short comment saying WHAT it is.

import numpy as np

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Number with array
a = np.array([1, 2, 3])
print(a + 10)                        # 10 is stretched to [10, 10, 10]

# %% Row with matrix
m = np.array([[1, 2, 3], [4, 5, 6]])    # shape (2, 3) = 2 rows, 3 columns
row = np.array([10, 20, 30])            # shape (3,)
print(m + row)                          # row is added to every row

# %% Column with matrix
col = np.array([[100], [200]])          # shape (2, 1) = a column
print(m + col)                          # col is added to every column

# %% Practical: centre every column (subtract its mean)
data = np.array([[1.0, 100.0], [2.0, 200.0], [3.0, 300.0]])
# .mean(axis=0): average of each column.
centered = data - data.mean(axis=0)
print(centered)

# %% Practical: scale every column to 0..1
scaled = (data - data.min(axis=0)) / (data.max(axis=0) - data.min(axis=0))
print(scaled)

# %% Practical: distances from one point to many points
points = np.array([[0, 0], [3, 4], [6, 8]])
origin = np.array([0, 0])
print(np.sqrt(((points - origin) ** 2).sum(axis=1)))   # Pythagoras per row
# np.linalg.norm(x, axis=1): length of each row vector (same result).
print(np.linalg.norm(points - origin, axis=1))

# %% When it fails
try:
    np.ones((2, 3)) + np.ones((2, 2))   # np.ones: array of 1s. Shapes don't fit.
except ValueError as error:
    print("Error:", error)

# %% Fix a failure with newaxis
x = np.array([1, 2])                        # (2,)
y = np.ones((2, 3))                         # (2,3)
# x[:, np.newaxis]: turns x into a column (2,1) so it can stretch across 3 columns.
print(y + x[:, np.newaxis])

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Column and row make a table
r = np.array([1, 2, 3])
c = np.array([[10], [20], [30]])
print(c + r)                            # (3,1) + (3,) -> (3,3) table
# np.multiply.outer(x, y): every x times every y (a multiplication table).
print(np.multiply.outer(r, r))

# %% Check the result shape without calculating
# np.broadcast_shapes(a, b): the shape you'd get from combining shapes a and b.
print(np.broadcast_shapes((3, 1), (1, 4)))
# np.broadcast_to(arr, shape): stretch an array to a bigger shape.
print(np.broadcast_to(np.array([1, 2, 3]), (2, 3)))
