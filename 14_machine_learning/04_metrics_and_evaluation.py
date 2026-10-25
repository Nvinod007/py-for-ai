# Accuracy alone can lie. Learn the metrics that tell the truth.

import numpy as np
from sklearn.datasets import make_classification
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import train_test_split

# %% An imbalanced problem: only 5 percent are fraud
X, y = make_classification(n_samples=4000, n_features=10, n_informative=5, weights=[0.95, 0.05], random_state=1)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1, stratify=y)
print("fraud share:", y.mean().round(3))

# %% The accuracy trap
always_no = np.zeros_like(y_test)
print("accuracy of 'never fraud':", round(accuracy_score(y_test, always_no), 3), "(useless but looks great)")
print("recall of 'never fraud'  :", recall_score(y_test, always_no))

# %% A real model
model = LogisticRegression(max_iter=1000).fit(X_train, y_train)
pred = model.predict(X_test)
proba = model.predict_proba(X_test)[:, 1]

# %% The confusion matrix: where mistakes happen
tn, fp, fn, tp = confusion_matrix(y_test, pred).ravel()
print(confusion_matrix(y_test, pred))
print(f"true negatives={tn} false positives={fp} false negatives={fn} true positives={tp}")

# %% Precision, recall, F1
print("precision:", round(precision_score(y_test, pred), 3), "  of those flagged, how many were truly fraud")
print("recall   :", round(recall_score(y_test, pred), 3), "  of all real fraud, how many we caught")
print("f1       :", round(f1_score(y_test, pred), 3), "  balance of the two")
print(f"by hand: precision={tp / (tp + fp):.3f}, recall={tp / (tp + fn):.3f}")
print(classification_report(y_test, pred, digits=3))

# %% Which mistake costs more?
# Fraud / disease / safety: missing a case is worse -> push for HIGH RECALL.
# Spam filter / recommendations: false alarms annoy people -> push for HIGH PRECISION.
for threshold in (0.1, 0.3, 0.5, 0.7):
    p = (proba >= threshold).astype(int)
    print(f"threshold {threshold}: precision={precision_score(y_test, p, zero_division=0):.2f} "
          f"recall={recall_score(y_test, p):.2f}")

# %% Metrics that do not depend on a threshold
print("ROC AUC          :", round(roc_auc_score(y_test, proba), 3), "(1 perfect, 0.5 random)")
print("Average precision:", round(average_precision_score(y_test, proba), 3), "(better when positives are rare)")
precision, recall, thresholds = precision_recall_curve(y_test, proba)
print(len(thresholds), "points on the precision-recall curve")

# %% Class weights help with imbalance
weighted = LogisticRegression(max_iter=1000, class_weight="balanced").fit(X_train, y_train)
print("recall with class_weight=balanced:", round(recall_score(y_test, weighted.predict(X_test)), 3))

# %% Regression metrics (for numbers): MAE, RMSE, R2 -> see 02_regression.py
# Multi-class: use average="macro" (every class equal) or "weighted" (by class size)
