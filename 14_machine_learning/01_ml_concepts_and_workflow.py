# Machine learning = finding patterns in data to predict something new.
#
# Supervised learning: you have the right answers (labels).
#     Regression      -> predict a number   (salary, price)
#     Classification  -> predict a category (spam / not spam)
# Unsupervised learning: no answers, find structure (clusters, compression).
# Each line has a short comment saying WHAT it is.

# Path: an object for file/folder paths.
from pathlib import Path

# numpy: fast number arrays and maths.
import numpy as np
# pandas: tables of data (DataFrames).
import pandas as pd
# DummyClassifier: a 'dumb' baseline model.
from sklearn.dummy import DummyClassifier
# LogisticRegression: a simple model that predicts a category.
from sklearn.linear_model import LogisticRegression
# accuracy_score(true, predicted): share of correct predictions.
from sklearn.metrics import accuracy_score
# train_test_split: splits data into train and test parts.
from sklearn.model_selection import train_test_split

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Words
# Feature (X): the inputs the model sees           e.g. age, department
# Label  (y): the answer to predict                e.g. will the person leave?
# Training set: data the model learns from
# Test set: data it has NEVER seen, used only to judge it
# Model: the pattern it learned    Prediction: its answer for new data

# %% The universal workflow
# 1. Define the question and the metric.   2. Get and clean data.
# 3. Split into train and test.             4. Make a baseline.
# 5. Train a model.                          6. Evaluate on the test set.
# 7. Improve (features, model, settings).    8. Save, deploy, monitor.

# %% Example data: predict whether an employee works remotely
# Use the data folder here, or one level up; Path.exists() checks it is there.
DATA = Path("data") if Path("data").exists() else Path("../data")
# pd.read_csv(file): loads a CSV file into a table (DataFrame).
df = pd.read_csv(DATA / "03_employees.csv")
# X = the feature columns (inputs) picked from the table.
X = df[["age", "salary", "performance_score"]]
# y = the label (answer); .astype(int) turns True/False into 1/0.
y = df["remote"].astype(int)
# shape = (rows, columns); y.mean() = share of 1s.
print(X.shape, y.mean())

# %% Always split BEFORE looking for patterns
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size, random_state, stratify): splits data into training and test parts; test_size=share for testing, random_state=fixed shuffle so results repeat, stratify=keep class mix equal.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
print(len(X_train), "train rows,", len(X_test), "test rows")

# %% Step 4: a baseline (the dumbest model). Your model must beat this.
# DummyClassifier(strategy='most_frequent'): always guesses the most common answer; fit(X, y) = learn from the training data.
baseline = DummyClassifier(strategy="most_frequent").fit(X_train, y_train)
# predict(X): the model's answers for new rows; round(x, 2) = 2 decimals.
print("baseline accuracy:", round(accuracy_score(y_test, baseline.predict(X_test)), 2))

# %% Step 5 and 6: train and evaluate
# LogisticRegression(max_iter=1000): max_iter = how many learning attempts it may make before stopping.
model = LogisticRegression(max_iter=1000).fit(X_train, y_train)
# predict(X_test): the model guesses labels for unseen rows.
predictions = model.predict(X_test)
print("model accuracy   :", round(accuracy_score(y_test, predictions), 2))
# to_numpy(): turns a pandas column into a plain array.
print("predictions:", predictions, "truth:", y_test.to_numpy())

# %% fit / predict / score is the same for EVERY sklearn model
# model.fit(X_train, y_train)      learn
# model.predict(X_new)             predict
# model.score(X_test, y_test)      quick metric

# %% Common mistakes
# Data leakage: information from the test set (or the future) leaks into training.
#               e.g. scaling on all the data before splitting, or using a feature that
#               contains the answer.
# Evaluating on training data: always looks great, tells you nothing.
# No baseline: "90% accuracy" means nothing if 90% of rows are one class.
# Tiny datasets: 30 rows are enough to learn the tools, not to trust results.


# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Reproducibility
# np.random.default_rng(42): random number maker with a fixed seed; integers(0, 10, 3) = 3 whole numbers from 0 to 9.
print(np.random.default_rng(42).integers(0, 10, 3))      # same seed -> same numbers
# Use random_state=42 in splits and models so results can be repeated.
