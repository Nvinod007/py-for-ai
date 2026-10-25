# Rolling windows and trend tools. Great for charts of change over time.
# Each line has a short comment saying WHAT the function is.

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

from pathlib import Path

import pandas as pd

# Path(...).exists(): True if the folder exists. Path / "file" joins a folder and a file name.
DATA = Path("data") if Path("data").exists() else Path("../data")
# pd.read_csv(...): loads a CSV file; parse_dates makes dates; index_col uses that column as row labels.
m = pd.read_csv(DATA / "04_monthly_sales.csv", parse_dates=["month"], index_col="month")
# m["col"]: picks one column (a Series).
s = m["electronics"]

# %% Rolling: look at the last N rows
# .rolling(3).mean(): average of the last 3 rows (moving average). .head(n): first n rows.
print(s.rolling(3).mean().head(5))              # first 2 are NaN (not enough data)
# min_periods=1: calculate even if fewer than 3 rows are available.
print(s.rolling(3, min_periods=1).mean().head(3))
# .sum() / .max() / .min(): total / biggest / smallest of the window. .tail(n): last n rows.
print(s.rolling(3).sum().tail(2), s.rolling(3).max().tail(2), s.rolling(3).min().tail(2))
# .std(): how spread out the window values are. .round(1): 1 decimal.
print(s.rolling(3).std().tail(2).round(1))
# center=True: the window is centred on the row, not behind it.
print(s.rolling(3, center=True).mean().head(3))
# rolling("90D"): window is the last 90 days (needs a date index).
print(s.rolling("90D").mean().tail(2))          # window by time

# %% Change from before
# .diff(): this row minus the previous row.
print(s.diff().head(3))
# .diff(3): this row minus the row 3 earlier.
print(s.diff(3).head(5))
# .pct_change(): percent change from the previous row (0.1 = 10%).
print(s.pct_change().head(3).round(3))
# periods=12: compare with 12 rows earlier (same month last year).
print(s.pct_change(periods=12))
# .shift(1): moves values down one row; shift(-1) moves them up.
print(s.shift(1).head(3), s.shift(-1).head(3))

# %% Growth
# m["new"] = ...: makes a new column.
m["growth_pct"] = (m["electronics"].pct_change() * 100).round(1)
# .iloc[0]: the value at position 0 (first row).
m["vs_first"] = m["electronics"] / m["electronics"].iloc[0]
# .cumsum(): running total.
m["cumulative"] = m["electronics"].cumsum()
# .cummax(): biggest value so far.
m["best_so_far"] = m["electronics"].cummax()
# [["a", "b"]]: pick several columns.
print(m[["electronics", "growth_pct", "vs_first", "cumulative", "best_so_far"]].head(4))

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Expanding: everything so far
# .expanding(): window grows from the first row to the current one.
print(s.expanding().mean().tail(2))
print(s.expanding().sum().tail(2))
print(s.expanding().max().tail(2))

# %% Exponentially weighted (recent data matters more)
# .ewm(span=3).mean(): moving average where newer rows count more.
print(s.ewm(span=3, adjust=False).mean().round(0).tail(3))
# alpha=0.5: how fast old values fade (bigger = faster).
print(s.ewm(alpha=0.5).mean().round(0).tail(3))

# %% Rolling over several columns, custom function
# Rolling works on several columns at once.
print(m[["electronics", "clothing"]].rolling(3).mean().tail(2).round(0))
# .apply(function): runs your function on each window (w = the 3 values).
print(s.rolling(3).apply(lambda w: w.max() - w.min()).tail(2))
# .agg([...]): several functions at once.
print(s.rolling(3).agg(["mean", "max"]).tail(2))

# %% Ranks and best/worst
# .idxmax() / .idxmin(): the row label of the biggest / smallest value. .nlargest(2): the 2 biggest values.
print(s.idxmax(), s.idxmin(), s.nlargest(2))
# .rank(ascending=False): 1 = biggest.
print(s.rank(ascending=False).head(3))
# s > x: True/False per row (is it above its moving average?).
print((s > s.rolling(3).mean()).tail(3))

# %% Seasonal view: average by month number
# .index.month: month number of each date. .groupby(...).mean(): average per month number.
by_month = m["electronics"].groupby(m.index.month).mean()
print(by_month)

# %% Correlation over time
# a.corr(b): how strongly two columns move together (-1 to 1).
print(m["visitors"].corr(m["electronics"]).round(3))
# rolling(6).corr(b): that correlation over the last 6 rows.
print(m["visitors"].rolling(6).corr(m["electronics"]).tail(2).round(3))
# df.corr(): correlation of every column pair.
print(m[["electronics", "clothing", "furniture", "visitors"]].corr().round(2))

# %% Outliers with z-score
# z-score: how many standard deviations a value is from the average. s.mean(): average.
z = (s - s.mean()) / s.std()
# .abs(): ignore minus sign. z[test]: keep rows where the test is True.
print(z[z.abs() > 1.5])
