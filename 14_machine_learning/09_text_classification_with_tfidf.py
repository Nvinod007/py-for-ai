# Text is just features too. TF-IDF turns words into numbers, then any classifier works.
# This is the bridge between classic ML and language models.
# Each line has a short comment saying WHAT it is.

# pandas: tables.
import pandas as pd
# CountVectorizer: counts words; TfidfVectorizer: weighs words by how special they are.
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
# LogisticRegression: simple classifier.
from sklearn.linear_model import LogisticRegression
# classification_report: precision/recall/F1 per class.
from sklearn.metrics import classification_report
# cross_val_score: score over several splits; train_test_split.
from sklearn.model_selection import cross_val_score, train_test_split
# make_pipeline: chains steps.
from sklearn.pipeline import make_pipeline

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% A tiny labelled dataset: support ticket categories
# A list of example sentences.
texts = [
    "I was charged twice for my order", "Refund has not arrived yet", "Wrong amount on my invoice",
    "Please cancel my subscription and refund", "My card was declined at checkout", "Need a receipt for payment",
    "The app crashes when I open it", "Cannot log in to my account", "Error message on the settings page",
    "Website is very slow today", "Password reset email never comes", "The page shows a blank screen",
    "Where is my package", "Delivery is late again", "Parcel arrived damaged",
    "Tracking number shows no updates", "Package was left at the wrong address", "Shipping takes too long",
]
# ['a'] * 6 repeats an item 6 times; joined lists = one label per sentence.
labels = ["billing"] * 6 + ["technical"] * 6 + ["shipping"] * 6
# Build a table from a dict of columns.
df = pd.DataFrame({"text": texts, "label": labels})

# %% Bag of words: count each word
# CountVectorizer(stop_words='english'): counts words, ignoring common ones like 'the'.
counter = CountVectorizer(stop_words="english")
# fit_transform(texts): learn the vocabulary and turn each text into word counts.
counts = counter.fit_transform(df["text"])
# shape = (texts, words); get_feature_names_out() = the words.
print(counts.shape, counter.get_feature_names_out()[:8])

# %% TF-IDF: down-weight words that appear everywhere, up-weight distinctive ones
# TfidfVectorizer(ngram_range=(1, 2), min_df=1): also uses 2-word phrases; min_df = a word must appear in at least this many texts.
tfidf = TfidfVectorizer(stop_words="english", ngram_range=(1, 2), min_df=1)
# Each text becomes numbers (TF-IDF scores).
matrix = tfidf.fit_transform(df["text"])
# shape = (texts, features).
print(matrix.shape)
# toarray().ravel(): sparse matrix -> flat normal array; pd.Series(values, index=words) labels each score.
row = pd.Series(matrix[0].toarray().ravel(), index=tfidf.get_feature_names_out())
# Keep words with a score above 0; sort_values(ascending=False) = biggest first; head() = top 5.
print(row[row > 0].sort_values(ascending=False).round(2).head())

# %% Train a classifier
# train_test_split(..., test_size=0.33, stratify=labels): split texts into train/test with equal label mix.
X_train, X_test, y_train, y_test = train_test_split(df["text"], df["label"], test_size=0.33, random_state=1, stratify=df["label"])
# Turn text into numbers, then LogisticRegression(max_iter=1000) (max learning attempts).
model = make_pipeline(TfidfVectorizer(stop_words="english"), LogisticRegression(max_iter=1000))
# fit(X, y): learn from training texts.
model.fit(X_train, y_train)
# zero_division=0: print 0 instead of warning when a class is never predicted.
print(classification_report(y_test, model.predict(X_test), zero_division=0))

# %% Predict new messages
# New messages to classify.
new = ["my payment failed twice", "the app freezes on login", "where is my order"]
# zip pairs items from lists; predict_proba(...).max(axis=1) = confidence of the chosen label.
for text, label, proba in zip(new, model.predict(new), model.predict_proba(new).max(axis=1)):
    print(f"{label:10} {proba:.2f}  {text}")

# %% See what the model learned
# named_steps[name]: pull out a step from the pipeline.
vectorizer, classifier = model.named_steps["tfidfvectorizer"], model.named_steps["logisticregression"]
# The words the model knows.
names = vectorizer.get_feature_names_out()
# enumerate: gives (number, item); classes_ = label names.
for i, label in enumerate(classifier.classes_):
    # coef_[i]: word weights for this label; argsort()[-4:][::-1] = the 4 biggest, largest first.
    top = classifier.coef_[i].argsort()[-4:][::-1]
    print(label, "->", [names[j] for j in top])


# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Cross-validation on the tiny set (needs more data in real life)
# cross_val_score(..., cv=3): 3 train/test rounds; cv = number of splits.
print(cross_val_score(make_pipeline(TfidfVectorizer(), LogisticRegression(max_iter=1000)), df["text"], df["label"], cv=3).round(2))

# %% Classic vs LLM approach
# TF-IDF + logistic regression: fast, cheap, explainable, needs hundreds+ labelled examples.
# LLM prompt (folder 09): no training data needed, flexible, slower and costs per call.
# Embeddings + logistic regression (folder 10): the best of both for many tasks.
