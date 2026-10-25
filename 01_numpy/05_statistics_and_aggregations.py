# Collapse many numbers into one: sum, mean, spread, rank, and so on.
# Each line has a short comment saying WHAT it is.

import numpy as np

scores = np.array([72, 85, 90, 66, 85, 91, 78, 60])
grid = np.array([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Basics
# .sum(): add everything up.
print(scores.sum(), np.sum(scores))
# .mean(): the average. np.median: the middle value when sorted.
print(scores.mean(), np.median(scores))
# .min / .max: smallest / biggest. np.ptp: "peak to peak" = max - min.
print(scores.min(), scores.max(), np.ptp(scores))
# .std: standard deviation (how spread out). .var: variance (std squared).
print(scores.std(), scores.var())

# %% Positions of min and max
# np.argmax / np.argmin: the POSITION of the biggest / smallest item.
print(np.argmax(scores), np.argmin(scores))

# %% Percentiles
# np.percentile(x, p): value below which p% of the data falls (50 = median).
print(np.percentile(scores, 25), np.percentile(scores, 50), np.percentile(scores, 75))
# np.quantile(x, q): same idea but q is 0..1 instead of 0..100.
print(np.quantile(scores, [0.1, 0.9]))

# %% axis: 0 = down the rows (per column), 1 = across (per row)
print(grid.sum())                        # no axis: everything
print(grid.sum(axis=0))                  # one total per column
print(grid.sum(axis=1))                  # one total per row
print(grid.mean(axis=0), grid.max(axis=1))
# keepdims=True: keep the result 2D instead of collapsing the dimension.
print(grid.sum(axis=0, keepdims=True))

# %% Yes/no questions
# np.any: True if at least one item matches. np.all: True if every item matches.
print(np.any(scores > 90), np.all(scores > 50))
# np.count_nonzero: how many True / non-zero items.
print(np.count_nonzero(scores > 80))
print((scores > 80).sum())               # True counts as 1, so sum = how many
print((scores > 80).mean())              # mean of True/False = share that match

# %% Counting
# np.unique(x, return_counts=True): each distinct value and how often it appears.
values, counts = np.unique(scores, return_counts=True)
print(values, counts)

# %% Sorting and ranking
# np.sort(x): sorted copy. [::-1] reverses it (biggest first).
print(np.sort(scores), np.sort(scores)[::-1])
# np.argsort(x): the positions that would sort the array.
order = np.argsort(scores)
print(order, scores[order])
print(np.argsort(np.argsort(scores)))    # rank of each item (0 = smallest)

# %% Standard scores
# z-score: how many standard deviations each value is from the mean.
z = (scores - scores.mean()) / scores.std()
print(np.round(z, 2))
# min-max scaling: squeezes values into 0..1.
normalized = (scores - scores.min()) / (scores.max() - scores.min())
print(np.round(normalized, 2))

# %% Group-like operations with masks
high = scores[scores >= 80]              # mask picks the items >= 80
low = scores[scores < 80]
print(high.mean(), low.mean())

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% prod and weighted average
# .prod(): multiply everything together (gets huge fast, so guarded here).
print(scores.prod() if scores.size < 5 else "too big to print")
# np.average(x, weights=w): average where some items count more than others.
print(np.average(scores, weights=[1, 1, 2, 2, 1, 1, 1, 1]))

# %% Running aggregates
# np.cumsum / np.cumprod: running total / running product.
print(np.cumsum(scores))
print(np.cumprod(np.array([1, 2, 3, 4])))
# np.maximum.accumulate: running maximum so far.
print(np.maximum.accumulate(scores))

# %% bincount and histogram
# np.bincount(x): counts of 0, 1, 2, 3 ... (whole non-negative numbers only).
print(np.bincount(np.array([0, 1, 1, 3, 3, 3])))
# np.histogram(x, bins): how many values fall into each range.
hist, edges = np.histogram(scores, bins=[0, 70, 80, 90, 100])
print(hist, edges)

# %% partition
# np.partition(x, k): puts the k smallest on the left, not fully sorted (fast).
print(np.partition(scores, 3))
# np.argpartition: positions version of partition (here: top 3, unordered).
print(np.argpartition(scores, -3)[-3:])

# %% Relationship between two variables
hours = np.array([1, 2, 3, 4, 5, 6])
marks = np.array([50, 55, 65, 70, 80, 85])
# np.corrcoef: correlation (-1 to 1): do the two move together?
print(np.corrcoef(hours, marks))
# np.cov: covariance: raw measure of how two variables vary together.
print(np.cov(hours, marks))

# %% Fitting a line
# np.polyfit(x, y, 1): best straight line through the points (slope, intercept).
slope, intercept = np.polyfit(hours, marks, 1)
print(slope, intercept)
# np.polyval(coeffs, x): plug x into the fitted line to predict y.
print(np.polyval([slope, intercept], 7))
# np.interp(x, xs, ys): estimate y at x by drawing straight lines between points.
print(np.interp(2.5, hours, marks))

# %% Digitize: put values in buckets
bins = np.array([60, 70, 80, 90])
# np.digitize(x, bins): which bucket number each value falls in.
print(np.digitize(scores, bins))
