# First thing to do with any new dataset: look at it.

from pathlib import Path

import pandas as pd

DATA = Path("data") if Path("data").exists() else Path("../data")
df = pd.read_csv(DATA / "03_employees.csv")

# %% Look at rows
print(df.head())          # first 5
print(df.head(3))
print(df.tail(3))         # last 3
print(df.sample(3, random_state=1))     # random rows
print(df.sample(frac=0.1, random_state=1))

# %% Structure
print(df.shape)
print(df.columns.tolist())
print(df.dtypes)
df.info()                               # types + non-null counts + memory
print(df.memory_usage(deep=True))

# %% Summary statistics
print(df.describe())                    # numbers only
print(df.describe(include="all"))       # everything
print(df["salary"].describe(percentiles=[0.1, 0.9]))
print(df.describe(include="number").T)

# %% Unique values and counts
print(df["department"].unique())
print(df["department"].nunique())
print(df["department"].value_counts())
print(df["department"].value_counts(normalize=True).round(2))
print(df.nunique())                     # unique count per column
print(df[["department", "gender"]].value_counts())

# %% Missing and duplicates
print(df.isna().sum())
print(df.isna().any().any())
print(df.duplicated().sum())
print(df["name"].is_unique)

# %% Single-number helpers
print(df["salary"].mean(), df["salary"].median(), df["salary"].std())
print(df["salary"].min(), df["salary"].max(), df["salary"].sum())
print(df["salary"].quantile([0.25, 0.5, 0.75]))
print(df["age"].mode())
print(df["salary"].skew(), df["salary"].kurt())
print(df["salary"].count())             # non-missing count
print(df[["age", "salary"]].corr())     # relationship between columns
print(df[["age", "salary"]].cov())
print(df["salary"].idxmax(), df.loc[df["salary"].idxmax(), "name"])

# %% Column types
print(df.select_dtypes(include="number").columns.tolist())
print(df.select_dtypes(exclude="number").columns.tolist())
print(df.select_dtypes(include="bool").columns.tolist())

# %% Quick checks
print(len(df))
print(df.columns.get_loc("salary"))
print("salary" in df.columns)
print(df.index.is_unique)
print(df["salary"].between(60000, 90000).sum())
print(df.equals(df.copy()))
