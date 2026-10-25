# Picking elements out of arrays.
# Each line has a short comment saying WHAT it is.

import numpy as np

a = np.array([10, 20, 30, 40, 50, 60])
m = np.arange(1, 13).reshape(3, 4)    # arange: numbers 1..12, reshape: 3 rows x 4 cols

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% 1D indexing and slicing
# a[i] = item at position i (starts at 0). Negative counts from the end.
print(a[0], a[-1])        # first, last
# a[start:stop] = slice; stop is NOT included.
print(a[1:4])             # positions 1, 2, 3
print(a[:3], a[3:])       # first three / from position 3 onward
print(a[::2])             # a[::step]: every 2nd item
print(a[::-1])            # negative step: reversed

# %% 2D indexing  [row, column]
print(m)
print(m[0, 0], m[2, 3], m[-1, -1])   # single cell: m[row, col]
print(m[1])               # one whole row
print(m[:, 1])            # ":" means "all", so this is a whole column
print(m[0:2, 1:3])        # a block: rows 0-1, columns 1-2
print(m[::2, ::2])        # every other row and every other column

# %% Slices are views: changing them changes the original
view = a[1:3]             # a view = a window onto the same data, not a copy
view[0] = 999
print(a)                  # original changed too
a[1] = 20                 # undo

# %% Boolean masks
# Comparing an array gives an array of True/False (a "mask").
print(a > 30)
# Using the mask as an index keeps only the True items.
print(a[a > 30])
print(a[(a > 20) & (a < 60)])    # & = and, | = or, ~ = not (wrap each test in brackets)
print(a[~(a > 30)])              # ~ flips True/False
print(m[m % 2 == 0])             # % = remainder; keeps the even numbers

# %% Fancy indexing (list of positions)
print(a[[0, 2, 4]])              # pick items at exactly these positions
print(m[[0, 2]])                 # pick rows 0 and 2
print(m[[0, 1], [1, 2]])         # pairs: cell (0,1) and cell (1,2)

# %% Changing values
b = a.copy()                     # .copy(): separate array so a stays unchanged
b[b > 30] = 0                    # set every item matching the mask to 0
print(b)
b[[0, 1]] = [-1, -2]             # set items at positions 0 and 1
print(b)

# %% where: find positions, or choose between two values
# np.where(cond): positions where the condition is True.
print(np.where(a > 30))
# np.where(cond, x, y): per item, x if True else y (an if-else for arrays).
print(np.where(a > 30, "big", "small"))

# %% Biggest and smallest position
# np.argmax / np.argmin: position of the biggest / smallest item.
print(np.argmax(a), np.argmin(a))

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Sub-grid with ix_
# np.ix_(rows, cols): lets you pick every row/column combination (a sub-grid).
print(m[np.ix_([0, 2], [1, 3])])

# %% More position finders
# np.nonzero(arr): positions of items that are not 0/False.
print(np.nonzero(a > 30))
# np.argwhere(cond): positions as [row, col] pairs.
print(np.argwhere(m > 10))
# np.flatnonzero(arr): positions of non-zero items in the flattened array.
print(np.flatnonzero(a > 30))

# %% take, put, choose, compress, select
# np.take(arr, positions): pick items by position.
print(np.take(a, [0, 3]))
c = a.copy()
# np.put(arr, positions, values): write values into those positions.
np.put(c, [0, 1], [7, 8])
print(c)
# np.compress(mask, arr): keep items where mask is True.
print(np.compress([True, False, True, False, False, False], a))
# np.choose(picks, options): for each slot, take the value from the chosen list.
print(np.choose([0, 1, 0, 1], [[1, 2, 3, 4], [10, 20, 30, 40]]))

conditions = [a < 25, a < 45]
choices = ["low", "mid"]
# np.select(conditions, choices, default): like if / elif / else for arrays.
print(np.select(conditions, choices, default="high"))

# %% Index helpers
# np.unravel_index(i, shape): turns a flat position into (row, col).
print(np.unravel_index(5, m.shape))
# np.ravel_multi_index((r, c), shape): the opposite, (row, col) to flat position.
print(np.ravel_multi_index((1, 2), m.shape))
# np.diag_indices(n): positions of the diagonal of an n x n grid.
print(np.diag_indices(3))
print(m[np.diag_indices(3)])

# %% Iterating
for row in m:                    # looping over a 2D array gives one row at a time
    print(row)
# np.ndenumerate(arr): gives ((row, col), value) for every cell.
for index, value in np.ndenumerate(m[:2, :2]):
    print(index, value)
# .flat: a flat iterator over every item, whatever the dimensions.
for value in m[0].flat:
    print(value, end=" ")
print()
