# Overfitting: the model memorizes the training data and fails on new data.

import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import (
    GridSearchCV,
    RandomizedSearchCV,
    StratifiedKFold,
    cross_val_score,
    learning_curve,
    train_test_split,
    validation_curve,
)
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

X, y = load_breast_cancer(return_X_y=True)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)

# %% Watch a tree overfit as it gets deeper
rows = []
for depth in [1, 2, 3, 5, 8, 15, None]:
    tree = DecisionTreeClassifier(max_depth=depth, random_state=0).fit(X_train, y_train)
    rows.append({"max_depth": depth, "train": tree.score(X_train, y_train), "test": tree.score(X_test, y_test)})
print(pd.DataFrame(rows).round(3))
# Train score keeps climbing to 1.0, test score stops improving: that gap is overfitting.

# %% Underfitting is the opposite: too simple to learn the pattern (low train AND test)

# %% One split is luck. Cross-validation averages several splits.
model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000))
scores = cross_val_score(model, X, y, cv=5)
print(scores.round(3), "mean", scores.mean().round(3), "+/-", scores.std().round(3))

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
print(cross_val_score(model, X, y, cv=cv, scoring="f1").mean().round(3))

# %% Pipelines inside CV prevent leakage (scaler is re-fitted on each training fold)

# %% Tune settings (hyperparameters) with a grid search
grid = GridSearchCV(
    make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000)),
    param_grid={"logisticregression__C": [0.01, 0.1, 1, 10, 100]},
    cv=5,
    scoring="f1",
)
grid.fit(X_train, y_train)
print("best settings:", grid.best_params_, "cv score:", round(grid.best_score_, 3))
print("test score with best model:", round(grid.score(X_test, y_test), 3))

# %% Randomized search when there are many settings
search = RandomizedSearchCV(
    RandomForestClassifier(random_state=0),
    param_distributions={"n_estimators": [50, 100, 200], "max_depth": [3, 5, 10, None], "min_samples_leaf": [1, 2, 5]},
    n_iter=8, cv=3, random_state=0,
)
search.fit(X_train, y_train)
print(search.best_params_)

# %% Validation curve: score vs one setting
depths = np.arange(1, 10)
train_scores, val_scores = validation_curve(
    DecisionTreeClassifier(random_state=0), X, y, param_name="max_depth", param_range=depths, cv=5
)
print(pd.DataFrame({"depth": depths, "train": train_scores.mean(axis=1), "validation": val_scores.mean(axis=1)}).round(3))

# %% Learning curve: does more data help?
sizes, train_curve, val_curve = learning_curve(model, X, y, cv=5, train_sizes=[0.1, 0.3, 0.6, 1.0])
print(pd.DataFrame({"train_size": sizes, "train": train_curve.mean(axis=1), "validation": val_curve.mean(axis=1)}).round(3))

# %% How to fight overfitting
# More data | simpler model | regularization | limit tree depth | dropout (deep learning)
# early stopping | remove noisy features | cross-validate everything
# NEVER tune on the test set. Use cross-validation for tuning, test set once at the end.
