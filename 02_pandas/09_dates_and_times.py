# Dates: parse them, pull parts out, shift, resample, and compare.

from pathlib import Path

import pandas as pd

DATA = Path("data") if Path("data").exists() else Path("../data")

# %% Turning text into dates
dates = pd.Series(["2024-01-05", "2024-02-10", "2024-03-15"])
print(pd.to_datetime(dates))
print(pd.to_datetime("05/01/2024", dayfirst=True))
print(pd.to_datetime("05/01/2024", format="%d/%m/%Y"))
print(pd.to_datetime(["2024-01-05", "March 3 2024"], format="mixed"))
print(pd.to_datetime(["2024-01-05", "oops"], errors="coerce"))      # bad -> NaT
print(pd.to_datetime(1_700_000_000, unit="s"))
print(pd.Timestamp("2024-03-15 14:30"))

# %% Parts of a date (the .dt accessor)
emp = pd.read_csv(DATA / "03_employees.csv", parse_dates=["join_date"])
d = emp["join_date"]
print(d.dt.year.head(3).tolist(), d.dt.month.head(3).tolist(), d.dt.day.head(3).tolist())
print(d.dt.day_name().head(3).tolist(), d.dt.month_name().head(3).tolist())
print(d.dt.dayofweek.head(3).tolist(), d.dt.dayofyear.head(3).tolist())
print(d.dt.quarter.head(3).tolist(), d.dt.isocalendar().head(3))
print(d.dt.is_month_end.head(3).tolist(), d.dt.is_leap_year.head(3).tolist())
print(d.dt.strftime("%d %b %Y").head(3).tolist())
print(d.dt.to_period("M").head(3).tolist())
print(d.dt.date.head(2).tolist())

# %% Time arithmetic
print(pd.Timestamp("2024-03-15") - pd.Timestamp("2024-01-01"))
print((pd.Timestamp("2024-03-15") - pd.Timestamp("2024-01-01")).days)
print(pd.Timestamp("2024-01-31") + pd.Timedelta(days=30))
print(pd.Timestamp("2024-01-31") + pd.DateOffset(months=1))
print(pd.Timedelta("2 days 3 hours").total_seconds())
tenure = pd.Timestamp("2026-01-01") - emp["join_date"]
print(tenure.dt.days.head(3).tolist())
print((tenure.dt.days / 365.25).round(1).head(3).tolist())

# %% Creating ranges
print(pd.date_range("2024-01-01", periods=5))                  # daily
print(pd.date_range("2024-01-01", "2024-01-10", freq="3D"))
print(pd.date_range("2024-01-31", periods=4, freq="ME"))       # month end
print(pd.date_range("2024-01-01", periods=4, freq="MS"))       # month start
print(pd.date_range("2024-01-01", periods=4, freq="W"))
print(pd.date_range("2024-01-01", periods=3, freq="h"))        # hourly
print(pd.bdate_range("2024-01-01", periods=5))                 # business days
print(pd.period_range("2024-01", periods=3, freq="M"))

# %% Filtering by date
print(emp[emp["join_date"] >= "2022-01-01"][["name", "join_date"]])
print(emp[emp["join_date"].between("2016-01-01", "2016-12-31")][["name", "join_date"]])
print(emp[emp["join_date"].dt.year == 2018][["name"]])

# %% Date index: slicing and resampling
sales = pd.read_csv(DATA / "04_monthly_sales.csv", parse_dates=["month"], index_col="month")
print(sales.loc["2023-03":"2023-05"])
print(sales.loc["2023"].shape)
print(sales.resample("QE").sum())                  # quarter totals
print(sales.resample("QE")["electronics"].mean())
print(sales.resample("YE").agg(["sum", "max"])["electronics"])

# %% Daily data and resample
days = pd.DataFrame(
    {"visits": range(1, 15)},
    index=pd.date_range("2024-01-01", periods=14, freq="D"),
)
print(days.resample("W").sum())
print(days.resample("3D").mean())
print(days.resample("12h").ffill().head(4))           # upsample
print(days.asfreq("2D"))

# %% Shift, diff, pct_change
print(sales["electronics"].shift(1).head(3))
print(sales["electronics"].diff().head(3))
print(sales["electronics"].pct_change().round(3).head(3))
print(sales["electronics"].shift(freq="MS").head(2))

# %% Rolling averages
print(sales["electronics"].rolling(3).mean().round(1).tail(3))
print(sales["electronics"].expanding().max().tail(3))
print(sales["electronics"].ewm(span=3).mean().round(1).tail(3))

# %% Time zones
stamp = pd.Timestamp("2024-03-15 09:00", tz="UTC")
print(stamp, stamp.tz_convert("Asia/Kolkata"))
print(pd.Timestamp("2024-03-15 09:00").tz_localize("US/Eastern"))

# %% Rounding times
t = pd.Series(pd.to_datetime(["2024-03-15 09:47:12"]))
print(t.dt.round("h"), t.dt.floor("D"), t.dt.ceil("h"))
print(t.dt.normalize())

# %% Useful checks
print(pd.Timestamp.now().year >= 2026)
print(sales.index.is_monotonic_increasing, sales.index.freq)
print(pd.NaT, pd.isna(pd.NaT))
