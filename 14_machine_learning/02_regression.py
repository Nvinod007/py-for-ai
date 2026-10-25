# Regression: predict a number. Example: predict salary.
# Each line has a short comment saying WHAT it is.

# Path: an object for file/folder paths.
from pathlib import Path

# numpy: fast number arrays and maths.
import numpy as np
# pandas: tables of data (DataFrames).
import pandas as pd
# DummyRegressor: a baseline that ignores the inputs.
from sklearn.dummy import DummyRegressor
# LinearRegression: draws the best straight-line fit; Ridge/Lasso: same with a penalty on big weights.
from sklearn.linear_model import Lasso, LinearRegression, Ridge
# Error measures: mean_absolute_error, mean_squared_error, r2_score.
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
# train_test_split: splits data into train and test parts.
from sklearn.model_selection import train_test_split
# make_pipeline: chains steps (e.g. scale then model) into one object.
from sklearn.pipeline import make_pipeline
# PolynomialFeatures: adds squared/product columns; StandardScaler: rescales columns to mean 0, spread 1.
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

# Use the data folder here, or one level up.
DATA = Path("data") if Path("data").exists() else Path("../data")
# pd.read_csv(file, parse_dates=[col]): loads a CSV and turns that column into dates.
df = pd.read_csv(DATA / "03_employees.csv", parse_dates=["join_date"])
# Date maths: years since joining (.dt.days = number of days).
df["years"] = (pd.Timestamp("2026-01-01") - df["join_date"]).dt.days / 365.25
# True/False -> 1/0 column: is the person in Engineering?
df["is_eng"] = (df["department"] == "Engineering").astype(int)

# X = input columns; y = the number to predict.
X = df[["age", "years", "performance_score", "is_eng"]]
y = df["salary"]
# train_test_split(...): split into train and test; random_state keeps the split repeatable.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)


# Helper: prints three error scores for a model on the test set.
def report(name, model):
    # predict(X): the model's guesses.
    pred = model.predict(X_test)
    # np.sqrt: square root; RMSE is the root of the mean squared error.
    rmse = np.sqrt(mean_squared_error(y_test, pred))
    # {:9,.0f} formats a number with commas and 0 decimals; {:18} pads text.
    print(f"{name:18} MAE={mean_absolute_error(y_test, pred):9,.0f}  RMSE={rmse:9,.0f}  R2={r2_score(y_test, pred):.2f}")


# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Baseline: always predict the average
# DummyRegressor(strategy='mean'): always guesses the average; fit(X, y) = learn from training data.
baseline = DummyRegressor(strategy="mean").fit(X_train, y_train)
report("baseline (mean)", baseline)

# %% Linear regression
# LinearRegression(): learns one weight per feature; fit() trains it.
lin = LinearRegression().fit(X_train, y_train)
report("linear", lin)
# coef_ = learned weights; intercept_ = starting value; zip pairs names with weights; round(0) = no decimals.
print(dict(zip(X.columns, lin.coef_.round(0))), round(lin.intercept_))
# coefficient = how much salary changes when that feature goes up by 1 (others fixed)

# %% Predict one new person
# pd.DataFrame({...}): builds a small table with one new row.
new_person = pd.DataFrame({"age": [35], "years": [8], "performance_score": [4.2], "is_eng": [1]})
# predict(...)[0]: first (only) guess.
print(round(lin.predict(new_person)[0]))

# %% Metrics in plain words
# MAE  : average size of the mistake, in salary units (easy to explain)
# RMSE : like MAE but punishes big mistakes more
# R2   : share of variation explained. 1 = perfect, 0 = no better than the mean, <0 = worse


# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Regularization: stops a model from trusting noise too much
# make_pipeline(StandardScaler(), Ridge(alpha=1.0)): scale then fit; alpha = strength of the penalty (bigger = simpler model).
for name, model in [
    ("ridge", make_pipeline(StandardScaler(), Ridge(alpha=1.0))),
    ("lasso", make_pipeline(StandardScaler(), Lasso(alpha=100))),
]:
    # fit(X, y): train the model.
    model.fit(X_train, y_train)
    report(name, model)
# Lasso with a big alpha can shrink weights to exactly 0; [-1] picks the last pipeline step; .coef_ = its weights.
print("lasso coefficients:", make_pipeline(StandardScaler(), Lasso(alpha=1000)).fit(X_train, y_train)[-1].coef_.round(0))

# %% Non-linear patterns with polynomial features
# PolynomialFeatures(degree=2): adds squared and multiplied columns so curves can be learned.
poly = make_pipeline(PolynomialFeatures(degree=2), StandardScaler(), Ridge(alpha=1.0)).fit(X_train, y_train)
report("polynomial deg 2", poly)

# %% Look at the errors (always)
# error = actual - predicted.
errors = (y_test - lin.predict(X_test)).round(0)
# head(): shows the first 5 rows.
print(pd.DataFrame({"actual": y_test, "predicted": lin.predict(X_test).round(0), "error": errors}).head())

# %% Remember
# Scale features for Ridge/Lasso/kNN/SVM/neural nets. Trees and forests do not need it.
# A high training score with a low test score means overfitting (see 05).
