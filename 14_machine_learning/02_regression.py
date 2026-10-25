# Regression: predict a number. Example: predict salary.

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.dummy import DummyRegressor
from sklearn.linear_model import Lasso, LinearRegression, Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import PolynomialFeatures, StandardScaler

DATA = Path("data") if Path("data").exists() else Path("../data")
df = pd.read_csv(DATA / "03_employees.csv", parse_dates=["join_date"])
df["years"] = (pd.Timestamp("2026-01-01") - df["join_date"]).dt.days / 365.25
df["is_eng"] = (df["department"] == "Engineering").astype(int)

X = df[["age", "years", "performance_score", "is_eng"]]
y = df["salary"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0)


def report(name, model):
    pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, pred))
    print(f"{name:18} MAE={mean_absolute_error(y_test, pred):9,.0f}  RMSE={rmse:9,.0f}  R2={r2_score(y_test, pred):.2f}")


# %% Baseline: always predict the average
baseline = DummyRegressor(strategy="mean").fit(X_train, y_train)
report("baseline (mean)", baseline)

# %% Linear regression
lin = LinearRegression().fit(X_train, y_train)
report("linear", lin)
print(dict(zip(X.columns, lin.coef_.round(0))), round(lin.intercept_))
# coefficient = how much salary changes when that feature goes up by 1 (others fixed)

# %% Predict one new person
new_person = pd.DataFrame({"age": [35], "years": [8], "performance_score": [4.2], "is_eng": [1]})
print(round(lin.predict(new_person)[0]))

# %% Metrics in plain words
# MAE  : average size of the mistake, in salary units (easy to explain)
# RMSE : like MAE but punishes big mistakes more
# R2   : share of variation explained. 1 = perfect, 0 = no better than the mean, <0 = worse

# %% Regularization: stops a model from trusting noise too much
for name, model in [
    ("ridge", make_pipeline(StandardScaler(), Ridge(alpha=1.0))),
    ("lasso", make_pipeline(StandardScaler(), Lasso(alpha=100))),
]:
    model.fit(X_train, y_train)
    report(name, model)
print("lasso coefficients:", make_pipeline(StandardScaler(), Lasso(alpha=1000)).fit(X_train, y_train)[-1].coef_.round(0))

# %% Non-linear patterns with polynomial features
poly = make_pipeline(PolynomialFeatures(degree=2), StandardScaler(), Ridge(alpha=1.0)).fit(X_train, y_train)
report("polynomial deg 2", poly)

# %% Look at the errors (always)
errors = (y_test - lin.predict(X_test)).round(0)
print(pd.DataFrame({"actual": y_test, "predicted": lin.predict(X_test).round(0), "error": errors}).head())

# %% Remember
# Scale features for Ridge/Lasso/kNN/SVM/neural nets. Trees and forests do not need it.
# A high training score with a low test score means overfitting (see 05).
