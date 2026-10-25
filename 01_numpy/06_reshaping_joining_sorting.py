# Change shape, join arrays, split arrays, sort arrays.

import numpy as np

a = np.arange(1, 7).reshape(2, 3)
b = np.array([[10, 20, 30], [40, 50, 60]])

# %% Transpose and axes
print(a.T)
print(np.transpose(a))
t3 = np.arange(24).reshape(2, 3, 4)
print(np.transpose(t3, (1, 0, 2)).shape)
print(np.swapaxes(t3, 0, 2).shape)
print(np.moveaxis(t3, 0, -1).shape)

# %% Adding or removing dimensions
v = np.array([1, 2, 3])
print(v.shape, v[:, np.newaxis].shape, v[np.newaxis, :].shape)
print(np.expand_dims(v, axis=0).shape)
print(np.squeeze(np.zeros((1, 3, 1))).shape)
print(np.atleast_2d(v).shape)

# %% Joining
print(np.concatenate([a, b], axis=0))
print(np.concatenate([a, b], axis=1))
print(np.vstack([a, b]))          # stack vertically
print(np.hstack([a, b]))          # stack horizontally
print(np.stack([a, b]).shape)     # new axis -> (2, 2, 3)
print(np.dstack([a, b]).shape)
print(np.column_stack([[1, 2, 3], [4, 5, 6]]))
print(np.r_[1:4, 10, 20])
print(np.c_[[1, 2, 3], [4, 5, 6]])

# %% Splitting
x = np.arange(12).reshape(3, 4)
print(np.split(np.arange(9), 3))
print(np.array_split(np.arange(10), 3))   # allows uneven pieces
print(np.hsplit(x, 2))
print(np.vsplit(x, [1]))

# %% Flip, rotate, roll
print(np.flip(a))
print(np.flip(a, axis=1), np.fliplr(a), np.flipud(a))
print(np.rot90(a))
print(np.roll(np.arange(5), 2))
print(np.roll(a, 1, axis=1))

# %% Insert, delete, append
base = np.array([1, 2, 3, 4])
print(np.append(base, [5, 6]))
print(np.insert(base, 1, 99))
print(np.delete(base, [0, 2]))
print(np.pad(base, (1, 2), constant_values=0))

# %% Sorting
messy = np.array([3, 1, 2, 5, 4])
print(np.sort(messy))
print(np.sort(messy)[::-1])
print(np.argsort(messy))
messy.sort()                      # in place
print(messy)

grid = np.array([[3, 1, 2], [9, 8, 7]])
print(np.sort(grid, axis=1))
print(np.sort(grid, axis=0))

# %% Sort one array by another
names = np.array(["Ann", "Bob", "Cy"])
ages = np.array([30, 20, 25])
print(names[np.argsort(ages)])
print(np.lexsort((names, ages)))   # sort by ages, then names

# %% Set operations
s1 = np.array([1, 2, 3, 4])
s2 = np.array([3, 4, 5])
print(np.union1d(s1, s2), np.intersect1d(s1, s2))
print(np.setdiff1d(s1, s2), np.setxor1d(s1, s2))
print(np.isin(s1, s2), np.in1d(s1, s2) if hasattr(np, "in1d") else "")

# %% Max/min positions in 2D and meshes
print(np.unravel_index(5, (2, 3)), np.ravel_multi_index((1, 2), (2, 3)))
print(np.indices((2, 2)))
