# Broadcasting = NumPy stretches smaller arrays so shapes can match.
# Rule: compare shapes from the right. Each pair must be equal or one must be 1.

import numpy as np

# %% Number with array
a = np.array([1, 2, 3])
print(a + 10)                        # 10 is stretched to [10, 10, 10]

# %% Row with matrix
m = np.array([[1, 2, 3], [4, 5, 6]])    # shape (2, 3)
row = np.array([10, 20, 30])            # shape (3,)
print(m + row)                          # row is added to every row

# %% Column with matrix
col = np.array([[100], [200]])          # shape (2, 1)
print(m + col)                          # col is added to every column

# %% Column and row make a table
r = np.array([1, 2, 3])
c = np.array([[10], [20], [30]])
print(c + r)                            # (3,1) + (3,) -> (3,3)
print(np.multiply.outer(r, r))          # multiplication table

# %% Practical: centre every column (subtract its mean)
data = np.array([[1.0, 100.0], [2.0, 200.0], [3.0, 300.0]])
centered = data - data.mean(axis=0)
print(centered)

# %% Practical: scale every column to 0..1
scaled = (data - data.min(axis=0)) / (data.max(axis=0) - data.min(axis=0))
print(scaled)

# %% Practical: distances from one point to many points
points = np.array([[0, 0], [3, 4], [6, 8]])
origin = np.array([0, 0])
print(np.sqrt(((points - origin) ** 2).sum(axis=1)))
print(np.linalg.norm(points - origin, axis=1))  # same result

# %% When it fails
try:
    np.ones((2, 3)) + np.ones((2, 2))
except ValueError as error:
    print("Error:", error)

# %% Fix a failure with newaxis
x = np.array([1, 2])                        # (2,)
y = np.ones((2, 3))                         # (2,3)
print(y + x[:, np.newaxis])                 # (2,1) now fits

# %% Check the result shape without calculating
print(np.broadcast_shapes((3, 1), (1, 4)))
print(np.broadcast_to(np.array([1, 2, 3]), (2, 3)))
