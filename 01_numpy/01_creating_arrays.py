# NumPy = fast arrays of numbers. Pandas and matplotlib are built on top of it.
# Run each "# %%" cell one by one and read the output.
# Each line has a short comment saying WHAT the function is.

import numpy as np

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% From Python lists
# np.array(list): turns a Python list into a NumPy array.
a = np.array([1, 2, 3, 4])
# type(x): tells you what kind of object x is (here: numpy.ndarray).
print(a, type(a))

# A list of lists becomes a 2D array (rows x columns).
matrix = np.array([[1, 2, 3], [4, 5, 6]])
print(matrix)

# A list of lists of lists becomes a 3D array.
cube = np.array([[[1, 2], [3, 4]], [[5, 6], [7, 8]]])
# .shape: tuple with the size of each dimension -> (2, 2, 2).
print(cube.shape)

# %% Force a type
# dtype=: choose the data type of the numbers (float, bool, int8 ...).
print(np.array([1, 2, 3], dtype=float))      # 1.0, 2.0, 3.0
print(np.array([1, 0, 2], dtype=bool))       # 0 -> False, anything else -> True
print(np.array([1, 2, 3], dtype=np.int8))    # tiny 8-bit integers (-128..127)

# %% Filled arrays
# np.zeros(shape): array full of 0.0.
print(np.zeros(5))
print(np.zeros((2, 3)))                      # 2 rows, 3 columns
# np.ones(shape): array full of 1.0.
print(np.ones((2, 3)))
# np.full(shape, value): array full of the value you choose.
print(np.full((2, 2), 7))
# np.empty(shape): array with whatever garbage was in memory (fast, unsafe).
print(np.empty((2, 2)))

# %% Same shape as another array
base = np.array([[1, 2], [3, 4]])
# *_like(arr): makes a new array with the same shape/type as arr.
print(np.zeros_like(base))                   # zeros, same shape
print(np.ones_like(base))                    # ones, same shape
print(np.full_like(base, 9))                 # all 9s, same shape
print(np.empty_like(base).shape)             # junk values, same shape

# %% Ranges
# np.arange(stop): numbers 0 up to (not including) stop.
print(np.arange(10))
# np.arange(start, stop, step): count from start in jumps of step.
print(np.arange(2, 10, 2))
print(np.arange(1, 2, 0.25))                 # steps can be decimals
# np.linspace(start, stop, n): n evenly spaced numbers, both ends included.
print(np.linspace(0, 1, 5))
print(np.linspace(0, 1, 5, endpoint=False))  # endpoint=False: leave out the stop

# %% Copy vs view
original = np.array([1, 2, 3])
alias = original                             # NOT a copy: both names, same data
# .copy(): makes a separate array with its own data.
dup = original.copy()
alias[0] = 99                                # changes original too
print(original, dup)                         # dup is untouched

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Log spaced
# np.logspace(a, b, n): n numbers spaced evenly on a log scale (10**a .. 10**b).
print(np.logspace(0, 3, 4))

# %% Identity and diagonal
# np.eye(N): N x N grid of zeros with 1s down the main diagonal.
print(np.eye(7))
# np.identity(n): same as eye, square only, no k option.
print(np.identity(3))
# k=: moves the diagonal up (k=1) or down (k=-1).
print(np.eye(3, k=1))
# np.diag(list): builds a matrix with your list on the diagonal.
print(np.diag([1, 2, 3, 4]))
# np.diag(matrix): does the opposite, pulls the diagonal out of a matrix.
print(np.diag(np.array([[1, 2], [3, 4]])))

# %% Triangles
m = np.arange(1, 10).reshape(3, 3)           # reshape: change the layout (3x3)
# np.tril(m): keep the lower triangle, set the rest to 0.
print(np.tril(m))
# np.triu(m): keep the upper triangle, set the rest to 0.
print(np.triu(m))

# %% Repeat and tile
# np.repeat(arr, n): repeat each element n times -> 1 1 2 2 3 3.
print(np.repeat([1, 2, 3], 2))
# np.tile(arr, n): repeat the whole array n times -> 1 2 3 1 2 3.
print(np.tile([1, 2, 3], 2))
print(np.tile([1, 2], (2, 2)))               # tile in 2 rows and 2 columns

# %% Grids (used for plots and maps)
x = np.array([1, 2, 3])
y = np.array([10, 20])
# np.meshgrid(x, y): makes two grids holding every (x, y) coordinate pair.
xx, yy = np.meshgrid(x, y)
print(xx)
print(yy)

# %% Built from a function
# np.fromfunction(f, shape): fills each cell with f(row, col).
print(np.fromfunction(lambda i, j: i + j, (3, 3), dtype=int))

# %%
