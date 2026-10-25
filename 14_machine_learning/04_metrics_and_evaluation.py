# Accuracy alone can lie. Learn the metrics that tell the truth.
# Each line has a short comment saying WHAT it is.

# numpy: arrays and maths.
import numpy as np
# make_classification: creates fake practice data.
from sklearn.datasets import make_classification
# LogisticRegression: simple classifier.
from sklearn.linear_model import LogisticRegression
# Scores: accuracy (share right), precision, recall, F1, ROC AUC, confusion matrix, classification_report.
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
# train_test_split: splits data into train and test.
from sklearn.model_selection import train_test_split

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% An imbalanced problem: only 5 percent are fraud
# make_classification(n_samples, n_features, n_informative, weights, random_state): fake data; weights=[0.95, 0.05] makes class 1 rare (5%); n_informative = columns that really matter.
X, y = make_classification(n_samples=4000, n_features=10, n_informative=5, weights=[0.95, 0.05], random_state=1)
# train_test_split(..., stratify=y): keeps the rare-class share equal in both parts.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=1, stratify=y)
# y.mean() = share of 1s.
print("fraud share:", y.mean().round(3))

# %% The accuracy trap
# np.zeros_like(y_test): an array of 0s the same size, i.e. 'never fraud'.
always_no = np.zeros_like(y_test)
# accuracy_score(true, predicted): share correct.
print("accuracy of 'never fraud':", round(accuracy_score(y_test, always_no), 3), "(useless but looks great)")
# recall_score: of all real fraud, how many were caught.
print("recall of 'never fraud'  :", recall_score(y_test, always_no))

# %% A real model
# LogisticRegression(max_iter=1000).fit(X, y): create and train.
model = LogisticRegression(max_iter=1000).fit(X_train, y_train)
# predict(X): the predicted class (0/1).
pred = model.predict(X_test)
# predict_proba(X)[:, 1]: probability of class 1.
proba = model.predict_proba(X_test)[:, 1]

# %% The confusion matrix: where mistakes happen
# confusion_matrix(true, predicted): 2x2 counts; ravel() flattens it into 4 numbers (true/false negatives/positives).
tn, fp, fn, tp = confusion_matrix(y_test, pred).ravel()
print(confusion_matrix(y_test, pred))
print(f"true negatives={tn} false positives={fp} false negatives={fn} true positives={tp}")

# %% Precision, recall, F1
# precision_score: of those flagged, how many were right. f1_score: balance of precision and recall.
print("precision:", round(precision_score(y_test, pred), 3), "  of those flagged, how many were truly fraud")
print("recall   :", round(recall_score(y_test, pred), 3), "  of all real fraud, how many we caught")
print("f1       :", round(f1_score(y_test, pred), 3), "  balance of the two")
# Same numbers calculated manually.
print(f"by hand: precision={tp / (tp + fp):.3f}, recall={tp / (tp + fn):.3f}")
# classification_report: a table of precision/recall/F1 per class; digits = decimals.
print(classification_report(y_test, pred, digits=3))

# %% Which mistake costs more?
# Fraud / disease / safety: missing a case is worse -> push for HIGH RECALL.
# Spam filter / recommendations: false alarms annoy people -> push for HIGH PRECISION.
# threshold: cut-off probability for 'yes'; zero_division=0 avoids errors when nothing is flagged.
for threshold in (0.1, 0.3, 0.5, 0.7):
    p = (proba >= threshold).astype(int)
    print(f"threshold {threshold}: precision={precision_score(y_test, p, zero_division=0):.2f} "
          f"recall={recall_score(y_test, p):.2f}")


# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Metrics that do not depend on a threshold
# roc_auc_score: quality across all thresholds (1 perfect, 0.5 random).
print("ROC AUC          :", round(roc_auc_score(y_test, proba), 3), "(1 perfect, 0.5 random)")
# average_precision_score: summary of the precision-recall curve.
print("Average precision:", round(average_precision_score(y_test, proba), 3), "(better when positives are rare)")
# precision_recall_curve: precision and recall at many thresholds.
precision, recall, thresholds = precision_recall_curve(y_test, proba)
print(len(thresholds), "points on the precision-recall curve")

# %% Class weights help with imbalance
# class_weight='balanced': pays more attention to the rare class.
weighted = LogisticRegression(max_iter=1000, class_weight="balanced").fit(X_train, y_train)
print("recall with class_weight=balanced:", round(recall_score(y_test, weighted.predict(X_test)), 3))

# %% Regression metrics (for numbers): MAE, RMSE, R2 -> see 02_regression.py
# Multi-class: use average="macro" (every class equal) or "weighted" (by class size)
