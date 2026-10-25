# Ensembles combine many weak models into a strong one. They dominate tabular data.

import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import (
    AdaBoostClassifier,
    BaggingClassifier,
    GradientBoostingClassifier,
    HistGradientBoostingClassifier,
    RandomForestClassifier,
    VotingClassifier,
)
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

data = load_breast_cancer(as_frame=True)
X, y = data.data, data.target
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0, stratify=y)

# %% One tree vs many trees
single = DecisionTreeClassifier(random_state=0)
print("single tree :", cross_val_score(single, X, y, cv=5).mean().round(3))

# %% Bagging: train many models on random samples, average them (random forest = bagging + random features)
bag = BaggingClassifier(DecisionTreeClassifier(), n_estimators=100, random_state=0)
forest = RandomForestClassifier(n_estimators=200, random_state=0)
print("bagging     :", cross_val_score(bag, X, y, cv=5).mean().round(3))
print("forest      :", cross_val_score(forest, X, y, cv=5).mean().round(3))

# %% Boosting: models trained one after another, each fixing the last one's mistakes
print("adaboost    :", cross_val_score(AdaBoostClassifier(random_state=0), X, y, cv=5).mean().round(3))
print("grad boost  :", cross_val_score(GradientBoostingClassifier(random_state=0), X, y, cv=5).mean().round(3))
print("hist boost  :", cross_val_score(HistGradientBoostingClassifier(random_state=0), X, y, cv=5).mean().round(3))
# XGBoost, LightGBM and CatBoost are faster, tuned versions of the same idea.

# %% Voting: let different kinds of models vote
vote = VotingClassifier(
    [
        ("logit", make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000))),
        ("knn", make_pipeline(StandardScaler(), KNeighborsClassifier())),
        ("forest", RandomForestClassifier(n_estimators=100, random_state=0)),
    ],
    voting="soft",
)
print("voting      :", cross_val_score(vote, X, y, cv=5).mean().round(3))

# %% Which features matter? (built-in importance, can be biased toward many-valued features)
forest.fit(X_train, y_train)
builtin = pd.Series(forest.feature_importances_, index=X.columns).sort_values(ascending=False)
print(builtin.head(5).round(3))

# %% Permutation importance: shuffle one column on the TEST set, see how much the score drops
result = permutation_importance(forest, X_test, y_test, n_repeats=10, random_state=0)
permuted = pd.Series(result.importances_mean, index=X.columns).sort_values(ascending=False)
print(permuted.head(5).round(3))

# %% Out-of-bag score: a free validation estimate from the bagging process
oob = RandomForestClassifier(n_estimators=300, oob_score=True, random_state=0).fit(X_train, y_train)
print("oob score:", round(oob.oob_score_, 3))

# %% Practical advice
# Tabular data: try gradient boosting first. Random forest is a strong, low-fuss baseline.
# Images, text, audio: deep learning (folder 15) wins.
# Explainability: SHAP is the standard tool (pip install shap).
