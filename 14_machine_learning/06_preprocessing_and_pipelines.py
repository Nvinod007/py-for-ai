# Real data is messy. A Pipeline bundles cleaning + model so the same steps run in training and in production.

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import MinMaxScaler, OneHotEncoder, OrdinalEncoder, StandardScaler

DATA = Path("data") if Path("data").exists() else Path("../data")
df = pd.read_csv(DATA / "03_employees.csv")

# %% Make it messy on purpose: some missing values
rng = np.random.default_rng(0)
df.loc[rng.choice(len(df), 4, replace=False), "age"] = np.nan
df.loc[rng.choice(len(df), 3, replace=False), "performance_score"] = np.nan
df.loc[rng.choice(len(df), 3, replace=False), "department"] = None
print(df[["age", "performance_score", "department"]].isna().sum())

# %% Individual tools
print(StandardScaler().fit_transform([[1.0], [2.0], [3.0]]).ravel().round(2))        # mean 0, std 1
print(MinMaxScaler().fit_transform([[1.0], [2.0], [3.0]]).ravel())                   # 0..1
print(OneHotEncoder(sparse_output=False).fit_transform([["a"], ["b"], ["a"]]))       # one column per category
print(OrdinalEncoder(categories=[["low", "mid", "high"]]).fit_transform([["mid"], ["high"]]).ravel())
print(SimpleImputer(strategy="median").fit_transform([[1.0], [np.nan], [3.0]]).ravel())

# %% Split features
X = df[["age", "performance_score", "department", "gender", "remote"]].copy()
X["remote"] = X["remote"].astype(int)
y = df["salary"]
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1)

numeric = ["age", "performance_score"]
categorical = ["department", "gender"]

# %% ColumnTransformer: different cleaning for different columns
preprocess = ColumnTransformer(
    [
        ("numbers", Pipeline([("fill", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), numeric),
        ("categories", Pipeline([("fill", SimpleImputer(strategy="most_frequent")),
                                 ("onehot", OneHotEncoder(handle_unknown="ignore"))]), categorical),
    ],
    remainder="passthrough",                        # keep "remote" as it is
)

# %% Full pipeline: preprocessing + model
pipe = Pipeline([("prep", preprocess), ("model", Ridge(alpha=1.0))])
pipe.fit(X_train, y_train)
print("MAE:", round(mean_absolute_error(y_test, pipe.predict(X_test))))

# %% Swap the model by changing one line
forest = Pipeline([("prep", preprocess), ("model", RandomForestRegressor(n_estimators=200, random_state=0))])
print("cv R2 ridge :", cross_val_score(pipe, X, y, cv=4, scoring="r2").mean().round(2))
print("cv R2 forest:", cross_val_score(forest, X, y, cv=4, scoring="r2").mean().round(2))

# %% Inspect what the pipeline built
forest.fit(X_train, y_train)
print(forest.named_steps["prep"].get_feature_names_out())

# %% The pipeline handles brand-new raw data (with a missing value and an unseen department)
new = pd.DataFrame([{"age": np.nan, "performance_score": 4.0, "department": "Legal", "gender": "F", "remote": 1}])
print(round(forest.predict(new)[0]))

# %% Why pipelines
# 1. No leakage: scalers and imputers learn only from training data.
# 2. One object to save and deploy (see 10_save_load_and_mini_project.py).
# 3. Easy to cross-validate and tune.
