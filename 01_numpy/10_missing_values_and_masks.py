# NaN = "not a number" = missing. inf = infinity.

import numpy as np

data = np.array([1.0, 2.0, np.nan, 4.0, np.nan, 6.0])

# %% Spotting
print(np.isnan(data))
print(np.isnan(data).sum())            # how many missing
print(np.isfinite(data))
print(np.isinf(np.array([1, np.inf, -np.inf])))
print(np.nan == np.nan)                # False! always use isnan

# %% Normal functions return nan if any item is nan
print(data.sum(), data.mean(), data.max())

# %% nan-safe functions ignore missing values
print(np.nansum(data), np.nanmean(data), np.nanmedian(data))
print(np.nanmax(data), np.nanmin(data), np.nanstd(data))
print(np.nanargmax(data), np.nanpercentile(data, 50))
print(np.nancumsum(data))

# %% Replace values
print(np.nan_to_num(data))                    # nan -> 0
print(np.nan_to_num(data, nan=-1.0))
filled = data.copy()
filled[np.isnan(filled)] = np.nanmean(data)   # fill with mean
print(filled)

# %% Remove missing values
print(data[~np.isnan(data)])

# %% Infinity
with np.errstate(divide="ignore", invalid="ignore"):
    print(np.array([1.0, -1.0, 0.0]) / 0.0)   # inf, -inf, nan

# %% Masked arrays: hide values instead of deleting them
masked = np.ma.masked_invalid(data)
print(masked)
print(masked.mean(), masked.count())
print(masked.filled(0))

hidden = np.ma.masked_where(np.array([5, 15, 25, 35]) > 20, np.array([5, 15, 25, 35]))
print(hidden, hidden.sum())
print(np.ma.masked_equal(np.array([1, -999, 3]), -999))
