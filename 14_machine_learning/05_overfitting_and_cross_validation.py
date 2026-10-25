# Overfitting: the model memorizes the training data and fails on new data.
# Each line has a short comment saying WHAT it is.

# numpy: arrays and maths.
import numpy as np
# pandas: tables.
import pandas as pd
# load_breast_cancer: built-in example dataset.
from sklearn.datasets import load_breast_cancer
# RandomForestClassifier: many trees voting.
from sklearn.ensemble import RandomForestClassifier
# LogisticRegression: simple classifier.
from sklearn.linear_model import LogisticRegression
# GridSearchCV: try every setting combo; RandomizedSearchCV: try random combos; StratifiedKFold: fold maker keeping class mix; cross_val_score: score over several splits; learning_curve / validation_curve: scores vs data size / one setting; train_test_split.
from sklearn.model_selection import (
    GridSearchCV,
    RandomizedSearchCV,
    StratifiedKFold,
    cross_val_score,
    learning_curve,
    train_test_split,
    validation_curve,
)
# make_pipeline: chains steps.
from sklearn.pipeline import make_pipeline
# StandardScaler: rescales columns.
from sklearn.preprocessing import StandardScaler
# DecisionTreeClassifier: a flowchart of yes/no questions.
from sklearn.tree import DecisionTreeClassifier

# return_X_y=True: gives features and labels directly.
X, y = load_breast_cancer(return_X_y=True)
# train_test_split(..., stratify=y): split into train/test with equal class mix; random_state repeats the split.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Watch a tree overfit as it gets deeper
# Empty list to collect results.
rows = []
# max_depth: how many questions deep the tree may go (None = unlimited).
for depth in [1, 2, 3, 5, 8, 15, None]:
    # fit(X, y) trains the tree.
    tree = DecisionTreeClassifier(max_depth=depth, random_state=0).fit(X_train, y_train)
    # score(X, y) = accuracy; append adds a result to the list.
    rows.append({"max_depth": depth, "train": tree.score(X_train, y_train), "test": tree.score(X_test, y_test)})
# DataFrame: a table; round(3) = 3 decimals.
print(pd.DataFrame(rows).round(3))
# Train score keeps climbing to 1.0, test score stops improving: that gap is overfitting.

# %% Underfitting is the opposite: too simple to learn the pattern (low train AND test)

# %% One split is luck. Cross-validation averages several splits.
# Scale then LogisticRegression(max_iter=2000).
model = make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000))
# cross_val_score(model, X, y, cv=5): trains and tests 5 times on different splits and returns 5 scores.
scores = cross_val_score(model, X, y, cv=5)
print(scores.round(3), "mean", scores.mean().round(3), "+/-", scores.std().round(3))

# StratifiedKFold(n_splits=5, shuffle=True): 5 folds, shuffled first, class mix kept.
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
# scoring='f1': use the F1 metric instead of accuracy.
print(cross_val_score(model, X, y, cv=cv, scoring="f1").mean().round(3))

# %% Pipelines inside CV prevent leakage (scaler is re-fitted on each training fold)

# %% Tune settings (hyperparameters) with a grid search
# GridSearchCV(model, param_grid, cv, scoring): tries each setting with cross-validation; 'logisticregression__C' = setting C of that pipeline step (smaller = simpler).
grid = GridSearchCV(
    make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000)),
    param_grid={"logisticregression__C": [0.01, 0.1, 1, 10, 100]},
    cv=5,
    scoring="f1",
)
# fit(): runs the search and keeps the best model.
grid.fit(X_train, y_train)
# best_params_ = winning settings; best_score_ = its cross-validation score.
print("best settings:", grid.best_params_, "cv score:", round(grid.best_score_, 3))
# score(X, y): accuracy on the test set.
print("test score with best model:", round(grid.score(X_test, y_test), 3))


# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Randomized search when there are many settings
# RandomizedSearchCV: tries n_iter random combos; min_samples_leaf = smallest group a leaf may hold.
search = RandomizedSearchCV(
    RandomForestClassifier(random_state=0),
    param_distributions={"n_estimators": [50, 100, 200], "max_depth": [3, 5, 10, None], "min_samples_leaf": [1, 2, 5]},
    n_iter=8, cv=3, random_state=0,
)
# Run the search.
search.fit(X_train, y_train)
print(search.best_params_)

# %% Validation curve: score vs one setting
# np.arange(1, 10): numbers 1 to 9.
depths = np.arange(1, 10)
# validation_curve: scores for each value of one setting (param_name, param_range).
train_scores, val_scores = validation_curve(
    DecisionTreeClassifier(random_state=0), X, y, param_name="max_depth", param_range=depths, cv=5
)
# mean(axis=1): average across the folds for each row.
print(pd.DataFrame({"depth": depths, "train": train_scores.mean(axis=1), "validation": val_scores.mean(axis=1)}).round(3))

# %% Learning curve: does more data help?
# learning_curve: scores as training data grows; train_sizes = shares of the data.
sizes, train_curve, val_curve = learning_curve(model, X, y, cv=5, train_sizes=[0.1, 0.3, 0.6, 1.0])
print(pd.DataFrame({"train_size": sizes, "train": train_curve.mean(axis=1), "validation": val_curve.mean(axis=1)}).round(3))

# %% How to fight overfitting
# More data | simpler model | regularization | limit tree depth | dropout (deep learning)
# early stopping | remove noisy features | cross-validate everything
# NEVER tune on the test set. Use cross-validation for tuning, test set once at the end.
