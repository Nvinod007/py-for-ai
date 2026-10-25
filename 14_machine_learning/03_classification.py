# Classification: predict a category. Compare the classic models on one problem.

import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier, export_text

# %% Data: tumours labelled malignant (0) or benign (1), 30 numeric measurements
data = load_breast_cancer(as_frame=True)
X, y = data.data, data.target
print(X.shape, y.value_counts().to_dict())
print(list(X.columns[:5]))

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

# %% Try several models with the same interface
models = {
    "logistic regression": make_pipeline(StandardScaler(), LogisticRegression(max_iter=2000)),
    "k nearest neighbours": make_pipeline(StandardScaler(), KNeighborsClassifier(n_neighbors=5)),
    "support vector machine": make_pipeline(StandardScaler(), SVC(probability=True)),
    "naive bayes": GaussianNB(),
    "decision tree": DecisionTreeClassifier(max_depth=4, random_state=42),
    "random forest": RandomForestClassifier(n_estimators=200, random_state=42),
}
for name, model in models.items():
    model.fit(X_train, y_train)
    print(f"{name:24} train={model.score(X_train, y_train):.3f}  test={model.score(X_test, y_test):.3f}")

# %% Probabilities, not just labels
logit = models["logistic regression"]
print(logit.predict_proba(X_test.iloc[:3]).round(3))        # [P(class 0), P(class 1)]
print(logit.predict(X_test.iloc[:3]))

# %% The decision threshold is a business decision
probabilities = logit.predict_proba(X_test)[:, 1]
for threshold in (0.3, 0.5, 0.9):
    predicted = (probabilities >= threshold).astype(int)
    print(f"threshold {threshold}: predicted benign = {predicted.sum()} of {len(predicted)}")

# %% Read a decision tree like a set of rules
tree = DecisionTreeClassifier(max_depth=2, random_state=0).fit(X_train, y_train)
print(export_text(tree, feature_names=list(X.columns)))

# %% Which features matter?
forest = models["random forest"]
importance = pd.Series(forest.feature_importances_, index=X.columns).sort_values(ascending=False)
print(importance.head(5).round(3))

# %% Choosing a model
# Start with logistic regression (simple, fast, explainable) and a random forest.
# kNN and SVM need scaled data. Trees and forests do not.
# Naive Bayes is fast for text. Boosted trees (XGBoost, LightGBM) win many tabular contests.
