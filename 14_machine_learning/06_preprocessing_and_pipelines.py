# Real data is messy. A Pipeline bundles cleaning + model so the same steps run in training and in production.
# Each line has a short comment saying WHAT it is.

# Path: an object for file/folder paths.
from pathlib import Path

# numpy: fast number arrays and maths.
import numpy as np
# pandas: tables of data (DataFrames).
import pandas as pd
# ColumnTransformer: applies different cleaning to different columns.
from sklearn.compose import ColumnTransformer
# RandomForestRegressor: many trees averaging a number.
from sklearn.ensemble import RandomForestRegressor
# SimpleImputer: fills in missing values.
from sklearn.impute import SimpleImputer
# Ridge: linear model with a penalty on big weights.
from sklearn.linear_model import Ridge
# mean_absolute_error: average size of the mistake.
from sklearn.metrics import mean_absolute_error
# cross_val_score: score over several splits; train_test_split.
from sklearn.model_selection import cross_val_score, train_test_split
# Pipeline: chains named steps into one model.
from sklearn.pipeline import Pipeline
# Scalers and encoders: MinMaxScaler (0 to 1), OneHotEncoder (one column per category), OrdinalEncoder (ordered categories as numbers), StandardScaler (mean 0, spread 1).
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, OrdinalEncoder, StandardScaler

# Use the data folder here, or one level up.
DATA = Path("data") if Path("data").exists() else Path("../data")
# pd.read_csv(file): loads a CSV into a table.
df = pd.read_csv(DATA / "03_employees.csv")

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Make it messy on purpose: some missing values
# np.random.default_rng(0): random maker with a fixed seed.
rng = np.random.default_rng(0)
# rng.choice(n, 4, replace=False): pick 4 different row numbers; .loc[rows, col] = ... overwrites those cells; np.nan = missing number.
df.loc[rng.choice(len(df), 4, replace=False), "age"] = np.nan
# Same idea for another column.
df.loc[rng.choice(len(df), 3, replace=False), "performance_score"] = np.nan
# None = missing text.
df.loc[rng.choice(len(df), 3, replace=False), "department"] = None
# isna().sum(): count of missing values per column.
print(df[["age", "performance_score", "department"]].isna().sum())

# %% Individual tools
# fit_transform(data): learn the scaling and apply it; ravel() flattens; result has mean 0, spread 1.
print(StandardScaler().fit_transform([[1.0], [2.0], [3.0]]).ravel().round(2))        # mean 0, std 1
# Squeezes values into the range 0 to 1.
print(MinMaxScaler().fit_transform([[1.0], [2.0], [3.0]]).ravel())                   # 0..1
# OneHotEncoder: turns each category into its own 0/1 column; sparse_output=False gives a normal array.
print(OneHotEncoder(sparse_output=False).fit_transform([["a"], ["b"], ["a"]]))       # one column per category
# OrdinalEncoder(categories=[[...]]): maps ordered words to 0, 1, 2.
print(OrdinalEncoder(categories=[["low", "mid", "high"]]).fit_transform([["mid"], ["high"]]).ravel())
# SimpleImputer(strategy='median'): replaces missing values with the middle value.
print(SimpleImputer(strategy="median").fit_transform([[1.0], [np.nan], [3.0]]).ravel())

# %% Split features
# X = input columns; .copy() makes an independent table.
X = df[["age", "performance_score", "department", "gender", "remote"]].copy()
# astype(int): True/False -> 1/0.
X["remote"] = X["remote"].astype(int)
# y = the number to predict.
y = df["salary"]
# train_test_split(...): split into train and test; random_state repeats it.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

# Lists of column names by type.
numeric = ["age", "performance_score"]
categorical = ["department", "gender"]

# %% ColumnTransformer: different cleaning for different columns
# ColumnTransformer([(name, steps, columns), ...]): each group of columns gets its own cleaning.
preprocess = ColumnTransformer(
    [
        # Pipeline: fill missing with median, then scale.
        ("numbers", Pipeline([("fill", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), numeric),
        # Fill missing with the most common value, then one-hot encode; handle_unknown='ignore' avoids errors on new categories.
        ("categories", Pipeline([("fill", SimpleImputer(strategy="most_frequent")),
                                 ("onehot", OneHotEncoder(handle_unknown="ignore"))]), categorical),
    ],
    # remainder='passthrough': leave other columns untouched.
    remainder="passthrough",                        # keep "remote" as it is
)

# %% Full pipeline: preprocessing + model
# Pipeline([(name, step), ...]): cleaning + Ridge(alpha=1.0) (alpha = penalty strength).
pipe = Pipeline([("prep", preprocess), ("model", Ridge(alpha=1.0))])
# fit(X, y): learns the cleaning AND the model from training data only.
pipe.fit(X_train, y_train)
# predict(X): guesses; the pipeline cleans the data first.
print("MAE:", round(mean_absolute_error(y_test, pipe.predict(X_test))))

# %% Swap the model by changing one line
# Same cleaning, new model: RandomForestRegressor(n_estimators=200) = 200 trees.
forest = Pipeline([("prep", preprocess), ("model", RandomForestRegressor(n_estimators=200, random_state=0))])
# cross_val_score(model, X, y, cv=4, scoring='r2'): 4 train/test rounds scored with R2 (1 = perfect).
print("cv R2 ridge :", cross_val_score(pipe, X, y, cv=4, scoring="r2").mean().round(2))
print("cv R2 forest:", cross_val_score(forest, X, y, cv=4, scoring="r2").mean().round(2))


# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Inspect what the pipeline built
# Train the forest pipeline.
forest.fit(X_train, y_train)
# named_steps[name]: grab one step; get_feature_names_out(): names of the final columns.
print(forest.named_steps["prep"].get_feature_names_out())

# %% The pipeline handles brand-new raw data (with a missing value and an unseen department)
# One new raw row, with a missing age and an unseen department.
new = pd.DataFrame([{"age": np.nan, "performance_score": 4.0, "department": "Legal", "gender": "F", "remote": 1}])
# The pipeline handles the messy row by itself.
print(round(forest.predict(new)[0]))

# %% Why pipelines
# 1. No leakage: scalers and imputers learn only from training data.
# 2. One object to save and deploy (see 10_save_load_and_mini_project.py).
# 3. Easy to cross-validate and tune.
