# Text is just features too. TF-IDF turns words into numbers, then any classifier works.
# This is the bridge between classic ML and language models.

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import make_pipeline

# %% A tiny labelled dataset: support ticket categories
texts = [
    "I was charged twice for my order", "Refund has not arrived yet", "Wrong amount on my invoice",
    "Please cancel my subscription and refund", "My card was declined at checkout", "Need a receipt for payment",
    "The app crashes when I open it", "Cannot log in to my account", "Error message on the settings page",
    "Website is very slow today", "Password reset email never comes", "The page shows a blank screen",
    "Where is my package", "Delivery is late again", "Parcel arrived damaged",
    "Tracking number shows no updates", "Package was left at the wrong address", "Shipping takes too long",
]
labels = ["billing"] * 6 + ["technical"] * 6 + ["shipping"] * 6
df = pd.DataFrame({"text": texts, "label": labels})

# %% Bag of words: count each word
counter = CountVectorizer(stop_words="english")
counts = counter.fit_transform(df["text"])
print(counts.shape, counter.get_feature_names_out()[:8])

# %% TF-IDF: down-weight words that appear everywhere, up-weight distinctive ones
tfidf = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), min_df=1)
matrix = tfidf.fit_transform(df["text"])
print(matrix.shape)
row = pd.Series(matrix[0].toarray().ravel(), index=tfidf.get_feature_names_out())
print(row[row > 0].sort_values(ascending=False).round(2).head())

# %% Train a classifier
X_train, X_test, y_train, y_test = train_test_split(df["text"], df["label"], test_size=0.33, random_state=1, stratify=df["label"])
model = make_pipeline(TfidfVectorizer(stop_words="english"), LogisticRegression(max_iter=1000))
model.fit(X_train, y_train)
print(classification_report(y_test, model.predict(X_test), zero_division=0))

# %% Predict new messages
new = ["my payment failed twice", "the app freezes on login", "where is my order"]
for text, label, proba in zip(new, model.predict(new), model.predict_proba(new).max(axis=1)):
    print(f"{label:10} {proba:.2f}  {text}")

# %% See what the model learned
vectorizer, classifier = model.named_steps["tfidfvectorizer"], model.named_steps["logisticregression"]
names = vectorizer.get_feature_names_out()
for i, label in enumerate(classifier.classes_):
    top = classifier.coef_[i].argsort()[-4:][::-1]
    print(label, "->", [names[j] for j in top])

# %% Cross-validation on the tiny set (needs more data in real life)
print(cross_val_score(make_pipeline(TfidfVectorizer(), LogisticRegression(max_iter=1000)), df["text"], df["label"], cv=3).round(2))

# %% Classic vs LLM approach
# TF-IDF + logistic regression: fast, cheap, explainable, needs hundreds+ labelled examples.
# LLM prompt (folder 09): no training data needed, flexible, slower and costs per call.
# Embeddings + logistic regression (folder 10): the best of both for many tasks.
