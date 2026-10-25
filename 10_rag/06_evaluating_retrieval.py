# "Looks good" is not a measure. Build a small test set of questions with known
# correct sources, then measure retrieval and change one thing at a time.
# Each line has a short comment saying WHAT it is.

import re
import zlib
from pathlib import Path

import numpy as np

# Path(...).exists(): True if the folder exists; picks whichever data folder is found.
DATA = Path("data") if Path("data").exists() else Path("../data")
# DIM: how many numbers each vector has.
DIM = 512
# STOP: 'stop words' = very common words we ignore because they carry little meaning.
STOP = {"the", "a", "an", "of", "to", "and", "is", "are", "in", "on", "for", "or", "do", "i", "my", "can", "you", "it", "we", "how", "what", "does", "much", "many", "long", "which", "when"}


# embed(text): turns text into a vector by counting non-stop words.
def embed(text):
    # np.zeros(n): array of n zeros to fill in.
    v = np.zeros(DIM)
    # re.findall(pattern, text): all pieces matching the pattern; [a-z0-9]+ = runs of letters/digits; lower() = lowercase.
    for w in re.findall(r"[a-z0-9]+", text.lower()):
        if w not in STOP:
            # crc32(word.encode()): turns the word into a fixed number; % DIM picks a slot; += 1 counts it (the 'hashing trick').
            v[zlib.crc32(w.encode()) % DIM] += 1
    # np.linalg.norm(v): the vector's length.
    n = np.linalg.norm(v)
    # Divide by length so the vector has length 1 (normalized); if length is 0 return it unchanged.
    return v / n if n else v


# read_text(): read the file as one string.
text = (DATA / "05_company_faq.md").read_text()
# sections: dictionary of title -> section text.
sections = {}
# re.split: cut before each '## ' heading.
for part in re.split(r"\n(?=## )", text):
    if part.startswith("## "):
        # partition("\n"): split at the first newline into title and body.
        title, _, body = part.partition("\n")
        sections[title.removeprefix("## ").strip()] = body.strip()
# list(dict): just the keys (section titles).
names = list(sections)
# matrix: one row (vector) per section.
matrix = np.array([embed(f"{n} {sections[n]}") for n in names])

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% 1. A labelled test set: question -> section that contains the answer
# TEST_SET: pairs of (question, the section that should be found).
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


# rank_sections: section names from best match to worst; argsort gives positions sorted small to big and [::-1] reverses.
def rank_sections(question):
    return [names[i] for i in np.argsort(matrix @ embed(question))[::-1]]

# %% 2. Metrics
# hit rate @ k: share of questions whose right section is in the top k.
def hit_rate_at_k(k):
    # sum(...): counts the True values (True = 1); divide by number of questions.
    return sum(expected in rank_sections(q)[:k] for q, expected in TEST_SET) / len(TEST_SET)


# MRR: average of 1/rank of the right answer (1st = 1, 2nd = 0.5, ...); higher is better.
def mean_reciprocal_rank():
    total = 0
    for q, expected in TEST_SET:
        # index(x): position of x in the list (starts at 0), so +1 makes it a rank.
        total += 1 / (rank_sections(q).index(expected) + 1)
    return total / len(TEST_SET)


# f"{x:.0%}": show as a percentage.
for k in (1, 2, 3):
    print(f"hit rate @ {k}: {hit_rate_at_k(k):.0%}")
print(f"MRR: {mean_reciprocal_rank():.2f}")

# %% 3. Look at the failures (this is where you learn)
for q, expected in TEST_SET:
    # Show questions where the best result was wrong; {q!r} prints the text with quotes.
    ranked = rank_sections(q)
    if ranked[0] != expected:
        print(f"MISS  {q!r}\n      wanted {expected!r}, got {ranked[:2]}")

# %% Rules
# 1. Write the test set BEFORE you tune anything.
# 2. 30-50 real questions beat 1000 invented ones.
# 3. Re-run after every change (chunk size, model, prompt, k).

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% 4. Compare two settings
# hit_rate_with: hit rate for any embedding function, so we can compare two.
def hit_rate_with(embed_func, k=1):
    m = np.array([embed_func(f"{n} {sections[n]}") for n in names])
    hits = 0
    for q, expected in TEST_SET:
        # argsort: positions sorted by score; [::-1] biggest first.
        order = np.argsort(m @ embed_func(q))[::-1]
        hits += expected in [names[i] for i in order[:k]]
    return hits / len(TEST_SET)


# A tiny wrapper that just calls embed.
def embed_no_title(t):
    return embed(t)


print("with titles in chunks   :", f"{hit_rate_with(embed):.0%}")
# Same as matrix but without the section titles.
matrix_body = np.array([embed(sections[n]) for n in names])
# np.argmax: position of the biggest score; compare to the expected name and count the matches.
body_hits = sum(names[int(np.argmax(matrix_body @ embed(q)))] == e for q, e in TEST_SET) / len(TEST_SET)
print("without titles in chunks:", f"{body_hits:.0%}")

# %% 5. Answer quality is measured separately
# Faithfulness: does the answer only use the retrieved context?
# Relevance:    does it answer the question?
# Refusal:      does it say "I don't know" when it should?
# See folder 16 for how to score these automatically.
