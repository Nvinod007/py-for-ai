# Ensembles combine many weak models into a strong one. They dominate tabular data.
# Each line has a short comment saying WHAT it is.

# pandas: tables.
import pandas as pd
# load_breast_cancer: built-in example dataset.
from sklearn.datasets import load_breast_cancer
# AdaBoost / GradientBoosting / HistGradientBoosting: boosting models; Bagging: average many models; RandomForest: many trees; Voting: models vote.
from sklearn.ensemble import (
    AdaBoostClassifier,
    BaggingClassifier,
    GradientBoostingClassifier,
    HistGradientBoostingClassifier,
    RandomForestClassifier,
    VotingClassifier,
)
# permutation_importance: shuffles a column to see how much it mattered.
from sklearn.inspection import permutation_importance
# LogisticRegression: simple classifier.
from sklearn.linear_model import LogisticRegression
# cross_val_score: score over several splits; train_test_split.
from sklearn.model_selection import cross_val_score, train_test_split
# KNeighborsClassifier: looks at the closest examples.
from sklearn.neighbors import KNeighborsClassifier
# make_pipeline: chains steps.
from sklearn.pipeline import make_pipeline
# StandardScaler: rescales columns.
from sklearn.preprocessing import StandardScaler
# DecisionTreeClassifier: yes/no question flowchart.
from sklearn.tree import DecisionTreeClassifier

# as_frame=True: return pandas tables.
data = load_breast_cancer(as_frame=True)
# X = features, y = labels.
X, y = data.data, data.target
# train_test_split(..., stratify=y): split into train/test with the same class mix.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% One tree vs many trees
# One tree; random_state fixes randomness.
single = DecisionTreeClassifier(random_state=0)
# cross_val_score(model, X, y, cv=5): 5 train/test rounds; .mean() = average.
print("single tree :", cross_val_score(single, X, y, cv=5).mean().round(3))

# %% Bagging: train many models on random samples, average them (random forest = bagging + random features)
# BaggingClassifier(base_model, n_estimators=100): trains 100 copies on random samples and averages them.
bag = BaggingClassifier(DecisionTreeClassifier(), n_estimators=100, random_state=0)
# RandomForestClassifier(n_estimators=200): 200 trees, each seeing random rows and columns.
forest = RandomForestClassifier(n_estimators=200, random_state=0)
print("bagging     :", cross_val_score(bag, X, y, cv=5).mean().round(3))
print("forest      :", cross_val_score(forest, X, y, cv=5).mean().round(3))

# %% Boosting: models trained one after another, each fixing the last one's mistakes
# AdaBoost: boosting, later models focus on earlier mistakes.
print("adaboost    :", cross_val_score(AdaBoostClassifier(random_state=0), X, y, cv=5).mean().round(3))
# GradientBoosting: each new tree fixes the previous trees' errors.
print("grad boost  :", cross_val_score(GradientBoostingClassifier(random_state=0), X, y, cv=5).mean().round(3))
# HistGradientBoosting: a faster version for bigger data.
print("hist boost  :", cross_val_score(HistGradientBoostingClassifier(random_state=0), X, y, cv=5).mean().round(3))
# XGBoost, LightGBM and CatBoost are faster, tuned versions of the same idea.

# %% Voting: let different kinds of models vote
# VotingClassifier([(name, model), ...], voting='soft'): averages predicted probabilities of different models.
vote = VotingClassifier(
    [
        ("logit", make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000))),
        ("knn", make_pipeline(StandardScaler(), KNeighborsClassifier())),
        ("forest", RandomForestClassifier(n_estimators=100, random_state=0)),
    ],
    voting="soft",
)
# Score of the voting team.
print("voting      :", cross_val_score(vote, X, y, cv=5).mean().round(3))

# %% Which features matter? (built-in importance, can be biased toward many-valued features)
# fit(X, y): train the forest.
forest.fit(X_train, y_train)
# feature_importances_: how much each column helped; sort_values(ascending=False) = biggest first.
builtin = pd.Series(forest.feature_importances_, index=X.columns).sort_values(ascending=False)
print(builtin.head(5).round(3))


# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Permutation importance: shuffle one column on the TEST set, see how much the score drops
# permutation_importance(model, X, y, n_repeats=10): shuffles each column 10 times and measures the score drop.
result = permutation_importance(forest, X_test, y_test, n_repeats=10, random_state=0)
# importances_mean: average score drop per column.
permuted = pd.Series(result.importances_mean, index=X.columns).sort_values(ascending=False)
print(permuted.head(5).round(3))

# %% Out-of-bag score: a free validation estimate from the bagging process
# oob_score=True: also scores each tree on rows it did not train on (out-of-bag).
oob = RandomForestClassifier(n_estimators=300, oob_score=True, random_state=0).fit(X_train, y_train)
# oob_score_: that free validation score.
print("oob score:", round(oob.oob_score_, 3))

# %% Practical advice
# Tabular data: try gradient boosting first. Random forest is a strong, low-fuss baseline.
# Images, text, audio: deep learning (folder 15) wins.
# Explainability: SHAP is the standard tool (pip install shap).
