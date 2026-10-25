# Try to solve each task BEFORE looking at the answer under it.

import numpy as np

# %% 1. Make an array of the numbers 1 to 20
answer = np.arange(1, 21)
print(answer)

# %% 2. Pick the even numbers from it
print(answer[answer % 2 == 0])

# %% 3. Make a 4x4 array of numbers 0..15, print its diagonal and the sum of each row
grid = np.arange(16).reshape(4, 4)
print(np.diag(grid))
print(grid.sum(axis=1))

# %% 4. Replace all negative numbers in [3, -1, 4, -5, 9] with 0
nums = np.array([3, -1, 4, -5, 9])
print(np.where(nums < 0, 0, nums))

# %% 5. Normalize [10, 20, 30, 40, 50] to the range 0..1
vals = np.array([10, 20, 30, 40, 50])
print((vals - vals.min()) / (vals.max() - vals.min()))

# %% 6. Make a 5x5 checkerboard of 0s and 1s
board = np.zeros((5, 5), dtype=int)
board[::2, ::2] = 1
board[1::2, 1::2] = 1
print(board)

# %% 7. Find the second largest value in [7, 3, 9, 1, 8]
arr = np.array([7, 3, 9, 1, 8])
print(np.sort(arr)[-2])

# %% 8. Count how many times each number shows up in [1, 2, 2, 3, 3, 3]
print(np.unique(np.array([1, 2, 2, 3, 3, 3]), return_counts=True))

# %% 9. Replace missing values (nan) with the column mean
table = np.array([[1.0, 2.0], [np.nan, 4.0], [5.0, np.nan]])
means = np.nanmean(table, axis=0)
table = np.where(np.isnan(table), means, table)
print(table)

# %% 10. Simulate 1000 coin flips and print the share of heads
rng = np.random.default_rng(0)
flips = rng.integers(0, 2, size=1000)
print(flips.mean())

# %% 11. Distance between two points (1, 2) and (4, 6)
print(np.linalg.norm(np.array([1, 2]) - np.array([4, 6])))

# %% 12. Moving average of [1, 2, 3, 4, 5, 6] with window 3
series = np.array([1, 2, 3, 4, 5, 6])
print(np.convolve(series, np.ones(3) / 3, mode="valid"))
