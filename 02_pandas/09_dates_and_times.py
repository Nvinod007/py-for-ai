# Dates: parse them, pull parts out, shift, resample, and compare.
# Each line has a short comment saying WHAT the function is.

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

from pathlib import Path

import pandas as pd

# Path(...).exists(): True if the folder exists. Path / "file" joins a folder and a file name.
DATA = Path("data") if Path("data").exists() else Path("../data")

# %% Turning text into dates
# pd.Series(list): a single labelled column of values.
dates = pd.Series(["2024-01-05", "2024-02-10", "2024-03-15"])
# pd.to_datetime(x): converts text into real dates (shows as datetime64).
print(pd.to_datetime(dates))
# dayfirst=True: read 05/01/2024 as 5 January (day comes first).
print(pd.to_datetime("05/01/2024", dayfirst=True))
# format=...: tells pandas the exact pattern (%d day, %m month, %Y year).
print(pd.to_datetime("05/01/2024", format="%d/%m/%Y"))
# format="mixed": allows each text to have a different date style.
print(pd.to_datetime(["2024-01-05", "March 3 2024"], format="mixed"))
# errors="coerce": bad text becomes NaT (Not-a-Time = missing date) instead of crashing.
print(pd.to_datetime(["2024-01-05", "oops"], errors="coerce"))      # bad -> NaT

# %% Parts of a date (the .dt accessor)
# pd.read_csv(file, parse_dates=[col]): loads a CSV file; parse_dates turns that column into dates.
# .head(n): first n rows. .tolist(): turns a column into a plain Python list.
emp = pd.read_csv(DATA / "03_employees.csv", parse_dates=["join_date"])
d = emp["join_date"]
# d.dt: the date toolbox of a date column. .dt.year / .month / .day: that part of each date as a number.
print(d.dt.year.head(3).tolist(), d.dt.month.head(3).tolist(), d.dt.day.head(3).tolist())
# .dt.day_name() / .month_name(): the name as text, e.g. Friday / March.
print(d.dt.day_name().head(3).tolist(), d.dt.month_name().head(3).tolist())
# .dt.dayofweek: weekday number (Monday=0). .dt.dayofyear: day number in the year (1-366).
print(d.dt.dayofweek.head(3).tolist(), d.dt.dayofyear.head(3).tolist())

# %% Time arithmetic
# Subtracting two dates gives a Timedelta (a length of time), e.g. 74 days.
print(pd.Timestamp("2024-03-15") - pd.Timestamp("2024-01-01"))
# .days: the whole days inside a Timedelta.
print((pd.Timestamp("2024-03-15") - pd.Timestamp("2024-01-01")).days)
# pd.Timedelta(days=30): a length of time to add or subtract (exactly 30 days).
print(pd.Timestamp("2024-01-31") + pd.Timedelta(days=30))
# pd.DateOffset(months=1): a calendar step (1 month, handles month lengths).
print(pd.Timestamp("2024-01-31") + pd.DateOffset(months=1))
# Timedelta(text).total_seconds(): the whole length expressed in seconds.
print(pd.Timedelta("2 days 3 hours").total_seconds())
# date column minus a date: time gap for every row.
tenure = pd.Timestamp("2026-01-01") - emp["join_date"]
# tenure.dt.days: days part of each gap as a number.
print(tenure.dt.days.head(3).tolist())
# Series.round(n): rounds numbers to n decimals. 365.25 = days in a year (turns days into years).
print((tenure.dt.days / 365.25).round(1).head(3).tolist())

# %% Creating ranges
# pd.date_range(start, periods=n, freq=...): makes a list of n dates; freq sets the step (default daily).
print(pd.date_range("2024-01-01", periods=5))                  # daily
# freq="3D": every 3 days (end= date given instead of periods).
print(pd.date_range("2024-01-01", "2024-01-10", freq="3D"))
# freq="ME": month End dates.
print(pd.date_range("2024-01-31", periods=4, freq="ME"))       # month end
# freq="MS": Month Start dates.
print(pd.date_range("2024-01-01", periods=4, freq="MS"))       # month start
# freq="W": weekly (Sundays).
print(pd.date_range("2024-01-01", periods=4, freq="W"))
# freq="h": every hour.
print(pd.date_range("2024-01-01", periods=3, freq="h"))        # hourly

# %% Filtering by date
# emp[condition]: keeps only rows where the condition is True. [["a", "b"]] then picks those columns.
print(emp[emp["join_date"] >= "2022-01-01"][["name", "join_date"]])
# Series.between(a, b): True when value is from a to b (both included).
print(emp[emp["join_date"].between("2016-01-01", "2016-12-31")][["name", "join_date"]])
# == checks equality; here: joined in 2018.
print(emp[emp["join_date"].dt.year == 2018][["name"]])

# %% Date index: slicing and resampling
# index_col="month": use that column as the row labels (the index), so we can slice by date.
sales = pd.read_csv(DATA / "04_monthly_sales.csv", parse_dates=["month"], index_col="month")
# .loc[a:b]: picks rows by label; with a date index, "2023-03":"2023-05" means March to May (both included).
print(sales.loc["2023-03":"2023-05"])
# .shape: (rows, columns). Here: all rows of 2023.
print(sales.loc["2023"].shape)
# .resample("QE"): groups rows by time chunk (QE = quarter end); then .sum() adds each chunk.
print(sales.resample("QE").sum())                  # quarter totals
# .mean(): the average of each chunk.
print(sales.resample("QE")["electronics"].mean())
# .agg([...]): runs several functions at once (sum and max). "YE" = year end.
print(sales.resample("YE").agg(["sum", "max"])["electronics"])

# %% Daily data and resample
# pd.DataFrame({...}, index=...): builds a table from a dictionary; index sets the row labels. range(1, 15): numbers 1 to 14.
days = pd.DataFrame(
    {"visits": range(1, 15)},
    index=pd.date_range("2024-01-01", periods=14, freq="D"),
)
# "W" = weekly chunks.
print(days.resample("W").sum())
# "3D" = 3-day chunks.
print(days.resample("3D").mean())
# .ffill(): fills new empty slots with the previous value (forward fill).
print(days.resample("12h").ffill().head(4))           # upsample
# .asfreq("2D"): keeps only the rows that fall every 2 days (no adding up).
print(days.asfreq("2D"))

# %% Shift, diff, pct_change
# .shift(1): moves values down 1 row (gives the previous row's value; first becomes NaN).
print(sales["electronics"].shift(1).head(3))
# .diff(): this row minus the previous row.
print(sales["electronics"].diff().head(3))
# .pct_change(): percent change from the previous row (0.1 = 10%).
print(sales["electronics"].pct_change().round(3).head(3))
# shift(freq=...): moves the dates (labels) instead of the values.
print(sales["electronics"].shift(freq="MS").head(2))

# %% Rolling averages
# .rolling(3).mean(): average of the latest 3 rows (moving average). .tail(n): last n rows.
print(sales["electronics"].rolling(3).mean().round(1).tail(3))

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Rare to_datetime options
# unit="s": the number is seconds since 1970-01-01 (a Unix timestamp).
print(pd.to_datetime(1_700_000_000, unit="s"))
# pd.Timestamp(text): one single date-and-time value.
print(pd.Timestamp("2024-03-15 14:30"))

# %% More date parts
# .dt.quarter: 1-4. .dt.isocalendar(): table with ISO year, week number and weekday.
print(d.dt.quarter.head(3).tolist(), d.dt.isocalendar().head(3))
# .dt.is_month_end: True if last day of month. .dt.is_leap_year: True if leap year.
print(d.dt.is_month_end.head(3).tolist(), d.dt.is_leap_year.head(3).tolist())
# .dt.strftime(pattern): formats a date as text, e.g. "%d %b %Y" -> 05 Jan 2024.
print(d.dt.strftime("%d %b %Y").head(3).tolist())
# .dt.to_period("M"): turns a date into a whole month ("Y" year, "Q" quarter).
print(d.dt.to_period("M").head(3).tolist())
# .dt.date: just the date part, no time.
print(d.dt.date.head(2).tolist())

# %% Special date ranges
# pd.bdate_range(...): like date_range but skips Saturdays and Sundays.
print(pd.bdate_range("2024-01-01", periods=5))                 # business days
# pd.period_range(...): a range of whole months (periods) instead of exact dates.
print(pd.period_range("2024-01", periods=3, freq="M"))

# %% Expanding and ewm
# .expanding().max(): biggest value seen so far, from the start.
print(sales["electronics"].expanding().max().tail(3))
# .ewm(span=3).mean(): moving average where newer rows count more.
print(sales["electronics"].ewm(span=3).mean().round(1).tail(3))

# %% Time zones
# tz="UTC": attaches a time zone to the time.
stamp = pd.Timestamp("2024-03-15 09:00", tz="UTC")
# .tz_convert(zone): shows the same moment in another time zone.
print(stamp, stamp.tz_convert("Asia/Kolkata"))
# .tz_localize(zone): says which time zone a time without zone belongs to.
print(pd.Timestamp("2024-03-15 09:00").tz_localize("US/Eastern"))

# %% Rounding times
# pd.Series(...): a column of values (here one date-time).
t = pd.Series(pd.to_datetime(["2024-03-15 09:47:12"]))
# .dt.round("h"): nearest hour. .dt.floor("D"): round down to the day. .dt.ceil("h"): round up to the hour.
print(t.dt.round("h"), t.dt.floor("D"), t.dt.ceil("h"))
# .dt.normalize(): sets the time to midnight.
print(t.dt.normalize())

# %% Useful checks
# pd.Timestamp.now(): the current date and time.
print(pd.Timestamp.now().year >= 2026)
# index.is_monotonic_increasing: True if dates only go up. index.freq: the regular step of the dates (None if unknown).
print(sales.index.is_monotonic_increasing, sales.index.freq)
# pd.NaT: a missing date. pd.isna(x): True if x is missing.
print(pd.NaT, pd.isna(pd.NaT))
