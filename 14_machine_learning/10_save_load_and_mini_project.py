# Mini project: predict salary, save the model, load it, and use it like a service would.
# Each line has a short comment saying WHAT it is.

# json: read/write JSON text.
import json
# tempfile: makes temporary folders.
import tempfile
# Path: an object for file/folder paths.
from pathlib import Path

# joblib: saves and loads Python objects (like trained models) to a file.
import joblib
# numpy: arrays and maths.
import numpy as np
# pandas: tables.
import pandas as pd
# ColumnTransformer: different cleaning for different columns.
from sklearn.compose import ColumnTransformer
# GradientBoostingRegressor: trees added one by one, each fixing earlier errors.
from sklearn.ensemble import GradientBoostingRegressor
# SimpleImputer: fills in missing values.
from sklearn.impute import SimpleImputer
# mean_absolute_error: average mistake size; r2_score: 1 = perfect.
from sklearn.metrics import mean_absolute_error, r2_score
# cross_val_score: score over several splits; train_test_split.
from sklearn.model_selection import cross_val_score, train_test_split
# Pipeline: chains named steps.
from sklearn.pipeline import Pipeline
# OneHotEncoder: category -> 0/1 columns; StandardScaler: rescales columns.
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Use the data folder here, or one level up.
DATA = Path("data") if Path("data").exists() else Path("../data")
# tempfile.mkdtemp(): creates a temporary folder and returns its path.
OUT = Path(tempfile.mkdtemp())

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% 1. Question: how much should we pay a new hire given age, tenure, performance, department?
# pd.read_csv(file, parse_dates=[col]): loads a CSV, turning that column into dates.
df = pd.read_csv(DATA / "03_employees.csv", parse_dates=["join_date"])
# Years since joining (.dt.days = days).
df["years"] = (pd.Timestamp("2026-01-01") - df["join_date"]).dt.days / 365.25
# Input columns.
features = ["age", "years", "performance_score", "department"]
# X = inputs, y = the salary to predict.
X, y = df[features], df["salary"]
# train_test_split(..., test_size=0.25, random_state=7): split into train/test; repeatable.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=7)

# %% 2. Baseline
# np.full(n, value): array of n copies; guessing the training average gives the baseline error.
baseline_mae = mean_absolute_error(y_test, np.full(len(y_test), y_train.mean()))
print("baseline MAE:", round(baseline_mae))

# %% 3. Pipeline
# Pipeline([(name, step), ...]): cleaning + model in one object.
pipeline = Pipeline([
    # ColumnTransformer: numeric columns get median-fill + scaling; 'department' gets one-hot encoding (handle_unknown='ignore' = no crash on new categories).
    ("prep", ColumnTransformer([
        ("num", Pipeline([("fill", SimpleImputer(strategy="median")), ("scale", StandardScaler())]),
         ["age", "years", "performance_score"]),
        ("cat", OneHotEncoder(handle_unknown="ignore"), ["department"]),
    ])),
    # GradientBoostingRegressor(n_estimators=150, max_depth=2, learning_rate=0.08): 150 small trees, each 2 levels deep; learning_rate = how big each correction step is.
    ("model", GradientBoostingRegressor(n_estimators=150, max_depth=2, learning_rate=0.08, random_state=7)),
])

# %% 4. Validate, then fit and test once
# cross_val_score(pipeline, X, y, cv=4, scoring='r2'): 4 train/test rounds scored with R2.
print("cv R2:", cross_val_score(pipeline, X_train, y_train, cv=4, scoring="r2").mean().round(2))
# fit(X, y): train the whole pipeline.
pipeline.fit(X_train, y_train)
# predict(X): salary guesses.
pred = pipeline.predict(X_test)
print("test MAE:", round(mean_absolute_error(y_test, pred)), "R2:", round(r2_score(y_test, pred), 2))

# %% 5. Save the whole pipeline plus metadata
# joblib.dump(obj, file): save the trained pipeline to a file.
joblib.dump(pipeline, OUT / "salary_model.joblib")
# Path / 'name' joins paths; write_text(text) saves text; json.dumps(dict, indent=2) makes pretty JSON.
(OUT / "model_card.json").write_text(json.dumps({
    "features": features,
    "target": "salary",
    "trained_on_rows": len(X_train),
    "test_mae": float(mean_absolute_error(y_test, pred)),
    "library_versions": "record them: models can break across scikit-learn versions",
}, indent=2))
# iterdir(): lists the folder's files; .name = file name.
print(sorted(p.name for p in OUT.iterdir()))

# %% 6. Load it later (in an API for example) and predict from raw input
# joblib.load(file): read the saved pipeline back.
loaded = joblib.load(OUT / "salary_model.joblib")


# Helper: takes raw values and returns a salary guess.
def predict_salary(age, years, performance_score, department):
    # A one-row table, because the pipeline expects a DataFrame.
    row = pd.DataFrame([{"age": age, "years": years, "performance_score": performance_score, "department": department}])
    # predict(row)[0]: first (only) guess, as a normal number.
    return float(loaded.predict(row)[0])


print(round(predict_salary(30, 5, 4.2, "Engineering")))
print(round(predict_salary(45, 15, 3.9, "HR")))


# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% 7. Before production
# Monitor: do live inputs look like training data? (drift)  Is accuracy dropping?
# Retrain on a schedule or when drift is found. Version the model and the data.
# Never load joblib/pickle files from untrusted sources (they can run code).

# %% Your turn
# 1. Predict `remote` instead (classification) and choose a metric.
# 2. Wrap predict_salary in a FastAPI endpoint (folder 12).
