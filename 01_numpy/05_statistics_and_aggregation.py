# Collapse many numbers into one (or one per row/column).

import numpy as np

scores = np.array([[70, 85, 90], [60, 75, 80], [95, 88, 92]])
data = np.array([4, 8, 15, 16, 23, 42])

# %% Basics
print(data.sum(), data.mean(), np.median(data))
print(data.min(), data.max(), np.ptp(data))      # ptp = max - min
print(data.std(), data.var())
print(data.prod())
print(np.average(data, weights=[1, 1, 1, 1, 1, 5]))

# %% Positions of min / max
print(data.argmin(), data.argmax())
print(scores.argmax(), np.unravel_index(scores.argmax(), scores.shape))

# %% axis: 0 = down the rows (per column), 1 = across (per row)
print(scores.sum(axis=0))
print(scores.sum(axis=1))
print(scores.mean(axis=0))
print(scores.max(axis=1))
print(scores.sum(axis=1, keepdims=True))   # keeps 2D shape

# %% Sample vs population standard deviation
print(np.std(data))            # divides by n
print(np.std(data, ddof=1))    # divides by n-1 (sample)

# %% Percentiles and quantiles
print(np.percentile(data, [25, 50, 75]))
print(np.quantile(data, [0.1, 0.9]))
q1, q3 = np.percentile(data, [25, 75])
print("IQR:", q3 - q1)

# %% Counting and testing
print(np.count_nonzero(data > 10))
print((data > 10).sum())       # True counts as 1
print(np.any(data > 40), np.all(data > 0))
print(np.any(scores > 90, axis=1))

# %% Unique values
v = np.array([3, 1, 2, 3, 3, 1])
print(np.unique(v))
values, counts = np.unique(v, return_counts=True)
print(values, counts)
print(np.unique(v, return_index=True))
print(np.unique(v, return_inverse=True))
print(np.bincount(v))

# %% Histogram numbers (not the plot)
counts, edges = np.histogram(data, bins=3)
print(counts, edges)
print(np.digitize(data, bins=[10, 20]))

# %% Cumulative
print(np.cumsum(data), np.cumprod(np.array([1, 2, 3])))
print(np.maximum.accumulate(np.array([1, 3, 2, 5, 4])))

# %% Relationships between variables
hours = np.array([1, 2, 3, 4, 5])
marks = np.array([50, 55, 65, 70, 85])
print(np.corrcoef(hours, marks))
print(np.cov(hours, marks))

# %% NaN-safe versions (skip missing values)
dirty = np.array([1.0, np.nan, 3.0])
print(dirty.sum(), np.nansum(dirty))
print(np.nanmean(dirty), np.nanmedian(dirty), np.nanstd(dirty))
print(np.nanmin(dirty), np.nanmax(dirty), np.nanargmax(dirty))
print(np.nanpercentile(dirty, 50), np.nancumsum(dirty))

# %% Sorting related
print(np.sort(data)[::-1])
print(np.argsort(data))
print(np.partition(data, 2))         # 3 smallest first, not fully sorted
print(np.searchsorted(np.array([1, 3, 5, 7]), 4))
