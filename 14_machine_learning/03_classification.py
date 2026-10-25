# Classification: predict a category. Compare the classic models on one problem.
# Each line has a short comment saying WHAT it is.

# pandas: tables of data.
import pandas as pd
# load_breast_cancer: a small built-in example dataset.
from sklearn.datasets import load_breast_cancer
# RandomForestClassifier: many decision trees voting together.
from sklearn.ensemble import RandomForestClassifier
# LogisticRegression: simple model predicting a category.
from sklearn.linear_model import LogisticRegression
# train_test_split: splits data into train and test.
from sklearn.model_selection import train_test_split
# GaussianNB: fast probability-based classifier.
from sklearn.naive_bayes import GaussianNB
# KNeighborsClassifier: looks at the closest known examples.
from sklearn.neighbors import KNeighborsClassifier
# make_pipeline: chains steps into one object.
from sklearn.pipeline import make_pipeline
# StandardScaler: rescales columns to similar size.
from sklearn.preprocessing import StandardScaler
# SVC: support vector machine, draws the best dividing boundary.
from sklearn.svm import SVC
# DecisionTreeClassifier: a flowchart of yes/no questions; export_text prints it.
from sklearn.tree import DecisionTreeClassifier, export_text

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Data: tumours labelled malignant (0) or benign (1), 30 numeric measurements
# as_frame=True: return pandas tables.
data = load_breast_cancer(as_frame=True)
# X = measurements (features), y = 0/1 answer (label).
X, y = data.data, data.target
# value_counts(): counts of each label; to_dict() makes it a dict.
print(X.shape, y.value_counts().to_dict())
print(list(X.columns[:5]))

# train_test_split(..., test_size=0.25, random_state, stratify=y): 25% for testing, repeatable shuffle, same class mix in both parts.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

# %% Try several models with the same interface
# dict of name -> model; they all share fit/predict/score.
models = {
    # StandardScaler() then LogisticRegression(max_iter=2000): max_iter = max learning attempts.
    "logistic regression": make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000)),
    # n_neighbors=5: vote of the 5 closest examples.
    "k nearest neighbours": make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5)),
    # SVC(probability=True): also lets it output probabilities.
    "support vector machine": make_pipeline(StandardScaler(), SVC(probability=True)),
    "naive bayes": GaussianNB(),
    # max_depth=4: at most 4 questions deep (limits memorizing); random_state fixes randomness.
    "decision tree": DecisionTreeClassifier(max_depth=4, random_state=42),
    # n_estimators=200: use 200 trees.
    "random forest": RandomForestClassifier(n_estimators=200, random_state=42),
}
# model.fit(X, y) learns; model.score(X, y) = accuracy (share correct).
for name, model in models.items():
    model.fit(X_train, y_train)
    print(f"{name:24} train={model.score(X_train, y_train):.3f}  test={model.score(X_test, y_test):.3f}")

# %% Probabilities, not just labels
# Pick the trained logistic model back out.
logit = models["logistic regression"]
# predict_proba(X): probability for each class; iloc[:3] = first 3 rows.
print(logit.predict_proba(X_test.iloc[:3]).round(3))        # [P(class 0), P(class 1)]
# predict(X): the final class chosen.
print(logit.predict(X_test.iloc[:3]))

# %% The decision threshold is a business decision
# [:, 1] keeps the probability of class 1 for every row.
probabilities = logit.predict_proba(X_test)[:, 1]
# threshold: the probability cut-off for saying 'yes'.
for threshold in (0.3, 0.5, 0.9):
    # Compare to threshold gives True/False; astype(int) -> 1/0.
    predicted = (probabilities >= threshold).astype(int)
    print(f"threshold {threshold}: predicted benign = {predicted.sum()} of {len(predicted)}")


# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Read a decision tree like a set of rules
# A tiny tree so it is readable; fit() trains it.
tree = DecisionTreeClassifier(max_depth=2, random_state=0).fit(X_train, y_train)
# export_text(tree, feature_names): prints the tree as if/else rules.
print(export_text(tree, feature_names=list(X.columns)))

# %% Which features matter?
# Pick the random forest back out.
forest = models["random forest"]
# feature_importances_: how much each column helped; pd.Series(values, index=names) labels them; sort_values(ascending=False) = biggest first.
importance = pd.Series(forest.feature_importances_, index=X.columns).sort_values(ascending=False)
print(importance.head(5).round(3))

# %% Choosing a model
# Start with logistic regression (simple, fast, explainable) and a random forest.
# kNN and SVM need scaled data. Trees and forests do not.
# Naive Bayes is fast for text. Boosted trees (XGBoost, LightGBM) win many tabular contests.
