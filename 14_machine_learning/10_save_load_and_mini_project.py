# Mini project: predict salary, save the model, load it, and use it like a service would.

import json
import tempfile
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

DATA = Path("data") if Path("data").exists() else Path("../data")
OUT = Path(tempfile.mkdtemp())

# %% 1. Question: how much should we pay a new hire given age, tenure, performance, department?
df = pd.read_csv(DATA / "03_employees.csv", parse_dates=["join_date"])
df["years"] = (pd.Timestamp("2026-01-01") - df["join_date"]).dt.days / 365.25
features = ["age", "years", "performance_score", "department"]
X, y = df[features], df["salary"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=7)

# %% 2. Baseline
baseline_mae = mean_absolute_error(y_test, np.full(len(y_test), y_train.mean()))
print("baseline MAE:", round(baseline_mae))

# %% 3. Pipeline
pipeline = Pipeline([
    ("prep", ColumnTransformer([
        ("num", Pipeline([("fill", SimpleImputer(strategy="median")), ("scale", StandardScaler())]),
         ["age", "years", "performance_score"]),
        ("cat", OneHotEncoder(handle_unknown="ignore"), ["department"]),
    ])),
    ("model", GradientBoostingRegressor(n_estimators=150, max_depth=2, learning_rate=0.08, random_state=7)),
])

# %% 4. Validate, then fit and test once
print("cv R2:", cross_val_score(pipeline, X_train, y_train, cv=4, scoring="r2").mean().round(2))
pipeline.fit(X_train, y_train)
pred = pipeline.predict(X_test)
print("test MAE:", round(mean_absolute_error(y_test, pred)), "R2:", round(r2_score(y_test, pred), 2))

# %% 5. Save the whole pipeline plus metadata
joblib.dump(pipeline, OUT / "salary_model.joblib")
(OUT / "model_card.json").write_text(json.dumps({
    "features": features,
    "target": "salary",
    "trained_on_rows": len(X_train),
    "test_mae": float(mean_absolute_error(y_test, pred)),
    "library_versions": "record them: models can break across scikit-learn versions",
}, indent=2))
print(sorted(p.name for p in OUT.iterdir()))

# %% 6. Load it later (in an API for example) and predict from raw input
loaded = joblib.load(OUT / "salary_model.joblib")


def predict_salary(age, years, performance_score, department):
    row = pd.DataFrame([{"age": age, "years": years, "performance_score": performance_score, "department": department}])
    return float(loaded.predict(row)[0])


print(round(predict_salary(30, 5, 4.2, "Engineering")))
print(round(predict_salary(45, 15, 3.9, "HR")))

# %% 7. Before production
# Monitor: do live inputs look like training data? (drift)  Is accuracy dropping?
# Retrain on a schedule or when drift is found. Version the model and the data.
# Never load joblib/pickle files from untrusted sources (they can run code).

# %% Your turn
# 1. Predict `remote` instead (classification) and choose a metric.
# 2. Wrap predict_salary in a FastAPI endpoint (folder 12).
