# NumPy = fast arrays of numbers. Pandas and matplotlib are built on top of it.
# Run each "# %%" cell one by one and read the output.

import numpy as np

# %% From Python lists
a = np.array([1, 2, 3, 4])
print(a, type(a))

matrix = np.array([[1, 2, 3], [4, 5, 6]])
print(matrix)

cube = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])  # 3D
print(cube.shape)

# %% Force a type
print(np.array([1, 2, 3], dtype=float))
print(np.array([1, 0, 2], dtype=bool))
print(np.array([1, 2, 3], dtype=np.int8))

# %% Filled arrays
print(np.zeros(5))
print(np.zeros((2, 3)))
print(np.ones((2, 3)))
print(np.full((2, 2), 7))
print(np.empty((2, 2)))  # random junk: memory is not cleared

# %% Same shape as another array
base = np.array([[1, 2], [3, 4]])
print(np.zeros_like(base))
print(np.ones_like(base))
print(np.full_like(base, 9))
print(np.empty_like(base).shape)

# %% Ranges
print(np.arange(10))             # 0..9
print(np.arange(2, 10, 2))       # start, stop (excluded), step
print(np.arange(1, 2, 0.25))     # float steps
print(np.linspace(0, 1, 5))      # 5 points, both ends included
print(np.linspace(0, 1, 5, endpoint=False))
print(np.logspace(0, 3, 4))      # 10**0 .. 10**3

# %% Identity and diagonal
print(np.eye(3))
print(np.identity(3))
print(np.eye(3, k=1))            # shifted diagonal
print(np.diag([1, 2, 3]))        # build a diagonal matrix
print(np.diag(np.array([[1, 2], [3, 4]])))  # pull the diagonal out

# %% Triangles
m = np.arange(1, 10).reshape(3, 3)
print(np.tril(m))                # lower triangle
print(np.triu(m))                # upper triangle

# %% Repeat and tile
print(np.repeat([1, 2, 3], 2))   # 1 1 2 2 3 3
print(np.tile([1, 2, 3], 2))     # 1 2 3 1 2 3
print(np.tile([1, 2], (2, 2)))

# %% Grids (used for plots and maps)
x = np.array([1, 2, 3])
y = np.array([10, 20])
xx, yy = np.meshgrid(x, y)
print(xx)
print(yy)

# %% Built from a function
print(np.fromfunction(lambda i, j: i + j, (3, 3), dtype=int))

# %% Copy vs view
original = np.array([1, 2, 3])
alias = original          # same data
dup = original.copy()     # independent copy
alias[0] = 99
print(original, dup)
