# Picking elements out of arrays.

import numpy as np

a = np.array([10, 20, 30, 40, 50, 60])
m = np.arange(1, 13).reshape(3, 4)

# %% 1D indexing and slicing
print(a[0], a[-1])        # first, last
print(a[1:4])             # index 1,2,3
print(a[:3], a[3:])       # up to / from
print(a[::2])             # every 2nd
print(a[::-1])            # reversed

# %% 2D indexing  [row, column]
print(m)
print(m[0, 0], m[2, 3], m[-1, -1])
print(m[1])               # whole row
print(m[:, 1])            # whole column
print(m[0:2, 1:3])        # block
print(m[::2, ::2])        # every other row and column

# %% Slices are views: changing them changes the original
view = a[1:3]
view[0] = 999
print(a)
a[1] = 20                 # undo

# %% Boolean masks
print(a > 30)
print(a[a > 30])
print(a[(a > 20) & (a < 60)])    # use & | ~ with parentheses, not and/or
print(a[~(a > 30)])
print(m[m % 2 == 0])             # all even numbers

# %% Fancy indexing (list of positions)
print(a[[0, 2, 4]])
print(m[[0, 2]])                 # rows 0 and 2
print(m[[0, 1], [1, 2]])         # pairs: (0,1) and (1,2)
print(m[np.ix_([0, 2], [1, 3])]) # rows 0,2 x columns 1,3

# %% Changing values
b = a.copy()
b[b > 30] = 0
print(b)
b[[0, 1]] = [-1, -2]
print(b)

# %% where: find positions, or choose between two values
print(np.where(a > 30))                  # positions
print(np.where(a > 30, "big", "small"))  # if-else for arrays
print(np.nonzero(a > 30))
print(np.argwhere(m > 10))
print(np.flatnonzero(a > 30))

# %% take, put, choose, compress, select
print(np.take(a, [0, 3]))
c = a.copy()
np.put(c, [0, 1], [7, 8])
print(c)
print(np.compress([True, False, True, False, False, False], a))
print(np.choose([0, 1, 0, 1], [[1, 2, 3, 4], [10, 20, 30, 40]]))

conditions = [a < 25, a < 45]
choices = ["low", "mid"]
print(np.select(conditions, choices, default="high"))

# %% Index helpers
print(np.argmax(a), np.argmin(a))
print(np.unravel_index(5, m.shape))      # flat index -> (row, col)
print(np.ravel_multi_index((1, 2), m.shape))
print(np.diag_indices(3))
print(m[np.diag_indices(3)])

# %% Iterating
for row in m:
    print(row)
for index, value in np.ndenumerate(m[:2, :2]):
    print(index, value)
for value in m[0].flat:
    print(value, end=" ")
print()
