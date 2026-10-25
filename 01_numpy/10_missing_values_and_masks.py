# NaN = "not a number" = missing. inf = infinity.
# Each line has a short comment saying WHAT it is.

import numpy as np

data = np.array([1.0, 2.0, np.nan, 4.0, np.nan, 6.0])   # np.nan = a missing value

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Spotting
# np.isnan(x): True where the value is missing.
print(np.isnan(data))
print(np.isnan(data).sum())            # True counts as 1, so this = how many missing
# np.isfinite(x): True for normal numbers (not nan, not infinity).
print(np.isfinite(data))
# np.isinf(x): True where the value is infinity.
print(np.isinf(np.array([1, np.inf, -np.inf])))
print(np.nan == np.nan)                # False! nan never equals anything, use isnan

# %% Normal functions return nan if any item is nan
print(data.sum(), data.mean(), data.max())

# %% nan-safe functions ignore missing values
# np.nan* functions do the same job but skip the missing items.
print(np.nansum(data), np.nanmean(data), np.nanmedian(data))
print(np.nanmax(data), np.nanmin(data), np.nanstd(data))
print(np.nanargmax(data), np.nanpercentile(data, 50))
print(np.nancumsum(data))

# %% Replace values
# np.nan_to_num(x): replaces nan with 0 (or with the value you choose).
print(np.nan_to_num(data))
print(np.nan_to_num(data, nan=-1.0))
filled = data.copy()
filled[np.isnan(filled)] = np.nanmean(data)   # fill the gaps with the average
print(filled)

# %% Remove missing values
print(data[~np.isnan(data)])           # ~ flips the mask, keeping only real numbers

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Infinity
# np.errstate(...): temporarily silences warnings (here: dividing by zero).
with np.errstate(divide="ignore", invalid="ignore"):
    print(np.array([1.0, -1.0, 0.0]) / 0.0)   # inf, -inf, nan

# %% Masked arrays: hide values instead of deleting them
# np.ma.masked_invalid(x): hides nan/inf values but keeps the array's shape.
masked = np.ma.masked_invalid(data)
print(masked)
print(masked.mean(), masked.count())   # .count(): how many visible values
print(masked.filled(0))                # .filled(v): replace hidden values with v

# np.ma.masked_where(cond, x): hide values where the condition is True.
hidden = np.ma.masked_where(np.array([5, 15, 25, 35]) > 20, np.array([5, 15, 25, 35]))
print(hidden, hidden.sum())
# np.ma.masked_equal(x, v): hide every value equal to v.
print(np.ma.masked_equal(np.array([1, -999, 3]), -999))
