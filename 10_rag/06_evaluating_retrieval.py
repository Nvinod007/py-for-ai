# "Looks good" is not a measure. Build a small test set of questions with known
# correct sources, then measure retrieval and change one thing at a time.

import re
import zlib
from pathlib import Path

import numpy as np

DATA = Path("data") if Path("data").exists() else Path("../data")
DIM = 512
STOP = {"the", "a", "an", "of", "to", "and", "is", "are", "in", "on", "for", "or", "do", "i", "my", "can", "you", "it", "we", "how", "what", "does", "much", "many", "long", "which", "when"}


def embed(text):
    v = np.zeros(DIM)
    for w in re.findall(r"[a-z0-9]+", text.lower()):
        if w not in STOP:
            v[zlib.crc32(w.encode()) % DIM] += 1
    n = np.linalg.norm(v)
    return v / n if n else v


text = (DATA / "05_company_faq.md").read_text()
sections = {}
for part in re.split(r"\n(?=## )", text):
    if part.startswith("## "):
        title, _, body = part.partition("\n")
        sections[title.removeprefix("## ").strip()] = body.strip()
names = list(sections)
matrix = np.array([embed(f"{n} {sections[n]}") for n in names])

# %% 1. A labelled test set: question -> section that contains the answer
TEST_SET = [
    ("How many days do I have to return an item?", "Returns"),
    ("Is there free shipping?", "Shipping"),
    ("Can I cancel my order after an hour?", "Order changes and cancellations"),
    ("Which payment cards do you accept?", "Payments"),
    ("How long is the warranty on electronics?", "Warranty"),
    ("I forgot my password", "Account and security"),
    ("When is support open?", "Contact support"),
    ("How many points make one dollar?", "Loyalty program"),
    ("Why was I charged twice?", "Payments"),
    ("What are the express delivery costs?", "Shipping"),
]


def rank_sections(question):
    return [names[i] for i in np.argsort(matrix @ embed(question))[::-1]]


# %% 2. Metrics
def hit_rate_at_k(k):
    return sum(expected in rank_sections(q)[:k] for q, expected in TEST_SET) / len(TEST_SET)


def mean_reciprocal_rank():
    total = 0
    for q, expected in TEST_SET:
        total += 1 / (rank_sections(q).index(expected) + 1)
    return total / len(TEST_SET)


for k in (1, 2, 3):
    print(f"hit rate @ {k}: {hit_rate_at_k(k):.0%}")
print(f"MRR: {mean_reciprocal_rank():.2f}")

# %% 3. Look at the failures (this is where you learn)
for q, expected in TEST_SET:
    ranked = rank_sections(q)
    if ranked[0] != expected:
        print(f"MISS  {q!r}\n      wanted {expected!r}, got {ranked[:2]}")

# %% 4. Compare two settings
def hit_rate_with(embed_func, k=1):
    m = np.array([embed_func(f"{n} {sections[n]}") for n in names])
    hits = 0
    for q, expected in TEST_SET:
        order = np.argsort(m @ embed_func(q))[::-1]
        hits += expected in [names[i] for i in order[:k]]
    return hits / len(TEST_SET)


def embed_no_title(t):
    return embed(t)


print("with titles in chunks   :", f"{hit_rate_with(embed):.0%}")
matrix_body = np.array([embed(sections[n]) for n in names])
body_hits = sum(names[int(np.argmax(matrix_body @ embed(q)))] == e for q, e in TEST_SET) / len(TEST_SET)
print("without titles in chunks:", f"{body_hits:.0%}")

# %% 5. Answer quality is measured separately
# Faithfulness: does the answer only use the retrieved context?
# Relevance:    does it answer the question?
# Refusal:      does it say "I don't know" when it should?
# See folder 16 for how to score these automatically.

# %% Rules
# 1. Write the test set BEFORE you tune anything.
# 2. 30-50 real questions beat 1000 invented ones.
# 3. Re-run after every change (chunk size, model, prompt, k).
