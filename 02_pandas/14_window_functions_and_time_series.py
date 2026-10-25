# Rolling windows and trend tools. Great for charts of change over time.

from pathlib import Path

import pandas as pd

DATA = Path("data") if Path("data").exists() else Path("../data")
m = pd.read_csv(DATA / "04_monthly_sales.csv", parse_dates=["month"], index_col="month")
s = m["electronics"]

# %% Rolling: look at the last N rows
print(s.rolling(3).mean().head(5))              # first 2 are NaN (not enough data)
print(s.rolling(3, min_periods=1).mean().head(3))
print(s.rolling(3).sum().tail(2), s.rolling(3).max().tail(2), s.rolling(3).min().tail(2))
print(s.rolling(3).std().tail(2).round(1))
print(s.rolling(3, center=True).mean().head(3))
print(s.rolling("90D").mean().tail(2))          # window by time

# %% Expanding: everything so far
print(s.expanding().mean().tail(2))
print(s.expanding().sum().tail(2))
print(s.expanding().max().tail(2))

# %% Exponentially weighted (recent data matters more)
print(s.ewm(span=3, adjust=False).mean().round(0).tail(3))
print(s.ewm(alpha=0.5).mean().round(0).tail(3))

# %% Change from before
print(s.diff().head(3))
print(s.diff(3).head(5))
print(s.pct_change().head(3).round(3))
print(s.pct_change(periods=12))
print(s.shift(1).head(3), s.shift(-1).head(3))

# %% Growth
m["growth_pct"] = (m["electronics"].pct_change() * 100).round(1)
m["vs_first"] = m["electronics"] / m["electronics"].iloc[0]
m["cumulative"] = m["electronics"].cumsum()
m["best_so_far"] = m["electronics"].cummax()
print(m[["electronics", "growth_pct", "vs_first", "cumulative", "best_so_far"]].head(4))

# %% Rolling over several columns, custom function
print(m[["electronics", "clothing"]].rolling(3).mean().tail(2).round(0))
print(s.rolling(3).apply(lambda w: w.max() - w.min()).tail(2))
print(s.rolling(3).agg(["mean", "max"]).tail(2))

# %% Ranks and best/worst
print(s.idxmax(), s.idxmin(), s.nlargest(2))
print(s.rank(ascending=False).head(3))
print((s > s.rolling(3).mean()).tail(3))

# %% Seasonal view: average by month number
by_month = m["electronics"].groupby(m.index.month).mean()
print(by_month)

# %% Correlation over time
print(m["visitors"].corr(m["electronics"]).round(3))
print(m["visitors"].rolling(6).corr(m["electronics"]).tail(2).round(3))
print(m[["electronics", "clothing", "furniture", "visitors"]].corr().round(2))

# %% Outliers with z-score
z = (s - s.mean()) / s.std()
print(z[z.abs() > 1.5])
