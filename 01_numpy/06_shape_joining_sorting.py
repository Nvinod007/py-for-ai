# Reshape, join, split, flip, sort, and set operations.

import numpy as np

a = np.arange(1, 7).reshape(2, 3)
b = np.array([[10, 20, 30], [40, 50, 60]])

# %% Transpose and axes
print(a.T, np.transpose(a))
cube = np.arange(24).reshape(2, 3, 4)
print(np.swapaxes(cube, 0, 2).shape)
print(np.moveaxis(cube, 0, -1).shape)

# %% Adding and removing dimensions
v = np.array([1, 2, 3])
print(v.shape, np.expand_dims(v, axis=0).shape, np.expand_dims(v, axis=1).shape)
print(v[:, np.newaxis].shape)             # same as expand_dims(axis=1)
print(np.squeeze(np.zeros((1, 3, 1))).shape)
print(np.atleast_2d(v).shape)

# %% Joining
print(np.concatenate([a, b], axis=0))     # stack rows
print(np.concatenate([a, b], axis=1))     # side by side
print(np.vstack([a, b]))
print(np.hstack([a, b]))
print(np.dstack([a, b]).shape)
print(np.stack([a, b]).shape)             # new axis
print(np.column_stack([[1, 2], [3, 4]]))
print(np.append(v, [4, 5]))

# %% Splitting
big = np.arange(12).reshape(3, 4)
print(np.split(np.arange(9), 3))
print(np.split(np.arange(9), [2, 5]))     # cut before index 2 and 5
print(np.array_split(np.arange(10), 3))   # uneven sizes allowed
print(np.hsplit(big, 2))
print(np.vsplit(big, 3))

# %% Inserting and deleting
print(np.insert(v, 1, 99))
print(np.delete(v, 0))
print(np.delete(big, 1, axis=0))
print(np.delete(big, [0, 2], axis=1))

# %% Flipping and rolling
print(np.flip(v), np.flipud(a), np.fliplr(a))
print(np.rot90(a))
print(np.roll(v, 1), np.roll(v, -1))

# %% Sorting
data = np.array([3, 1, 2, 5, 4])
print(np.sort(data))
print(np.argsort(data))
table = np.array([[3, 1], [1, 2], [2, 0]])
print(np.sort(table, axis=0))
print(table[np.argsort(table[:, 0])])     # sort rows by first column
names = np.array(["b", "a", "b", "a"])
nums = np.array([2, 2, 1, 1])
print(np.lexsort((nums, names)))          # sort by names, then nums

# %% Searching in sorted data
sorted_data = np.array([10, 20, 30, 40])
print(np.searchsorted(sorted_data, 25))   # where 25 would be inserted
print(np.searchsorted(sorted_data, [5, 45]))

# %% Unique values and set operations
x = np.array([1, 2, 2, 3, 3, 3])
y = np.array([3, 4, 5])
print(np.unique(x))
print(np.unique(x, return_counts=True))
print(np.unique(x, return_index=True))
print(np.union1d(x, y))
print(np.intersect1d(x, y))
print(np.setdiff1d(x, y))
print(np.setxor1d(x, y))
print(np.isin(x, y))                      # for each x, is it in y?
# %% Padding
print(np.pad(v, (1, 2), constant_values=0))
print(np.pad(np.ones((2, 2)), 1))

# %% Repeating and reshaping again
print(np.repeat(a, 2, axis=0))
print(np.tile(v, (2, 1)))
print(a.reshape(-1))
print(a.reshape(3, 2, order="F"))         # Fortran (column-first) order
