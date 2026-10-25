# Reshape, join, split, flip, sort, and set operations.
# Each line has a short comment saying WHAT it is.

import numpy as np

a = np.arange(1, 7).reshape(2, 3)
b = np.array([[10, 20, 30], [40, 50, 60]])

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Transpose and axes
# .T / np.transpose: swap rows and columns.
print(a.T, np.transpose(a))

# %% Adding and removing dimensions
v = np.array([1, 2, 3])
# np.expand_dims(arr, axis): add a new dimension of size 1.
print(v.shape, np.expand_dims(v, axis=0).shape, np.expand_dims(v, axis=1).shape)
# np.newaxis: shortcut for the same thing inside [].
print(v[:, np.newaxis].shape)
# np.squeeze: remove dimensions of size 1.
print(np.squeeze(np.zeros((1, 3, 1))).shape)

# %% Joining
# np.concatenate: glue arrays along an existing axis.
print(np.concatenate([a, b], axis=0))     # one under the other
print(np.concatenate([a, b], axis=1))     # side by side
# np.vstack: stack vertically. np.hstack: stack horizontally.
print(np.vstack([a, b]))
print(np.hstack([a, b]))
# np.stack: join along a NEW axis.
print(np.stack([a, b]).shape)
# np.append(arr, values): add values at the end (returns a new array).
print(np.append(v, [4, 5]))

# %% Splitting
big = np.arange(12).reshape(3, 4)
# np.split(arr, n): cut into n equal parts. A list = cut at those positions.
print(np.split(np.arange(9), 3))
print(np.split(np.arange(9), [2, 5]))

# %% Inserting and deleting
# np.insert(arr, pos, value): put a value in at a position.
print(np.insert(v, 1, 99))
# np.delete(arr, pos): remove items (axis picks rows or columns).
print(np.delete(v, 0))
print(np.delete(big, 1, axis=0))          # remove row 1
print(np.delete(big, [0, 2], axis=1))     # remove columns 0 and 2

# %% Sorting
data = np.array([3, 1, 2, 5, 4])
# np.sort: sorted copy.
print(np.sort(data))
# np.argsort: the positions that would sort it.
print(np.argsort(data))
table = np.array([[3, 1], [1, 2], [2, 0]])
print(np.sort(table, axis=0))             # sort each column on its own
print(table[np.argsort(table[:, 0])])     # sort whole rows by the first column

# %% Unique values and set operations
x = np.array([1, 2, 2, 3, 3, 3])
y = np.array([3, 4, 5])
# np.unique: the distinct values (sorted).
print(np.unique(x))
print(np.unique(x, return_counts=True))   # plus how many times each appears
print(np.setxor1d(x, y))
# np.isin(x, y): for each item of x, True if it is in y.

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Swap and move axes
cube = np.arange(24).reshape(2, 3, 4)
# np.swapaxes(arr, i, j): swap two dimensions.
print(np.swapaxes(cube, 0, 2).shape)
# np.moveaxis(arr, from, to): move one dimension to another place.
print(np.moveaxis(cube, 0, -1).shape)

# %% atleast_2d
# np.atleast_2d: make sure the array is at least 2D.
print(np.atleast_2d(v).shape)

# %% More joining
# np.dstack: stack along depth (3rd axis).
print(np.dstack([a, b]).shape)
# np.column_stack: turn 1D arrays into columns of a 2D array.
print(np.column_stack([[1, 2], [3, 4]]))

# %% More splitting
# np.array_split: like split but allows unequal parts.
print(np.array_split(np.arange(10), 3))
# np.hsplit: split by columns. np.vsplit: split by rows.
print(np.hsplit(big, 2))
print(np.vsplit(big, 3))

# %% Flipping and rolling
# np.flip: reverse. np.flipud: upside down. np.fliplr: left to right.
print(np.flip(v), np.flipud(a), np.fliplr(a))
# np.rot90: rotate 90 degrees.
print(np.rot90(a))
# np.roll(arr, n): shift items by n; the ones that fall off wrap around.
print(np.roll(v, 1), np.roll(v, -1))

# %% lexsort
names = np.array(["b", "a", "b", "a"])
nums = np.array([2, 2, 1, 1])
# np.lexsort((second, first)): sort by first key, ties broken by second.
print(np.lexsort((nums, names)))

# %% Searching in sorted data
sorted_data = np.array([10, 20, 30, 40])
# np.searchsorted(sorted, x): position where x would be inserted to stay sorted.
print(np.searchsorted(sorted_data, 25))
print(np.searchsorted(sorted_data, [5, 45]))

# %% Set operations
print(np.unique(x, return_index=True))    # plus where each first appears
# np.union1d: everything in either. np.intersect1d: only in both.
print(np.union1d(x, y))
print(np.intersect1d(x, y))
# np.setdiff1d: in x but not y. np.setxor1d: in one but not both.
print(np.setdiff1d(x, y))


# %% Padding
# np.pad(arr, (before, after)): add extra values around the edges.
print(np.pad(v, (1, 2), constant_values=0))
print(np.pad(np.ones((2, 2)), 1))

# %% Repeating and reshaping again
# np.repeat(arr, n, axis): repeat each row n times.
print(np.repeat(a, 2, axis=0))
# np.tile(arr, reps): repeat the whole array.
print(np.tile(v, (2, 1)))
print(a.reshape(-1))                      # -1 flattens to 1D
print(a.reshape(3, 2, order="F"))         # order="F": fill column by column
