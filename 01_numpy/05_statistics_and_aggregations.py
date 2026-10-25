# Collapse many numbers into one: sum, mean, spread, rank, and so on.

import numpy as np

scores = np.array([72, 85, 90, 66, 85, 91, 78, 60])
grid = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# %% Basics
print(scores.sum(), np.sum(scores))
print(scores.mean(), np.median(scores))
print(scores.min(), scores.max(), np.ptp(scores))   # ptp = max - min
print(scores.std(), scores.var())
print(scores.prod() if scores.size < 5 else "too big to print")
print(np.average(scores, weights=[1, 1, 2, 2, 1, 1, 1, 1]))

# %% Positions of min and max
print(np.argmax(scores), np.argmin(scores))

# %% Percentiles
print(np.percentile(scores, 25), np.percentile(scores, 50), np.percentile(scores, 75))
print(np.quantile(scores, [0.1, 0.9]))

# %% axis: 0 = down the rows (per column), 1 = across (per row)
print(grid.sum())
print(grid.sum(axis=0))
print(grid.sum(axis=1))
print(grid.mean(axis=0), grid.max(axis=1))
print(grid.sum(axis=0, keepdims=True))   # keep the dimension

# %% Running aggregates
print(np.cumsum(scores))
print(np.cumprod(np.array([1, 2, 3, 4])))
print(np.maximum.accumulate(scores))     # running maximum

# %% Yes/no questions
print(np.any(scores > 90), np.all(scores > 50))
print(np.count_nonzero(scores > 80))     # how many are above 80
print((scores > 80).sum())               # same idea
print((scores > 80).mean())              # share of items

# %% Counting
values, counts = np.unique(scores, return_counts=True)
print(values, counts)
print(np.bincount(np.array([0, 1, 1, 3, 3, 3])))
hist, edges = np.histogram(scores, bins=[0, 70, 80, 90, 100])
print(hist, edges)

# %% Sorting and ranking
print(np.sort(scores), np.sort(scores)[::-1])
order = np.argsort(scores)
print(order, scores[order])
print(np.argsort(np.argsort(scores)))    # rank of each item (0 = smallest)
print(np.partition(scores, 3))           # smallest 3 land on the left
print(np.argpartition(scores, -3)[-3:])  # indexes of top 3 (unordered)

# %% Relationship between two variables
hours = np.array([1, 2, 3, 4, 5, 6])
marks = np.array([50, 55, 65, 70, 80, 85])
print(np.corrcoef(hours, marks))
print(np.cov(hours, marks))

# %% Fitting a line
slope, intercept = np.polyfit(hours, marks, 1)
print(slope, intercept)
print(np.polyval([slope, intercept], 7))  # predict for 7 hours
print(np.interp(2.5, hours, marks))       # linear interpolation

# %% Standard scores
z = (scores - scores.mean()) / scores.std()
print(np.round(z, 2))
normalized = (scores - scores.min()) / (scores.max() - scores.min())
print(np.round(normalized, 2))

# %% Group-like operations with masks
high = scores[scores >= 80]
low = scores[scores < 80]
print(high.mean(), low.mean())

# %% Digitize: put values in buckets
bins = np.array([60, 70, 80, 90])
print(np.digitize(scores, bins))
