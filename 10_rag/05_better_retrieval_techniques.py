# Improving retrieval: keyword search, hybrid search, reranking, query rewriting.
# Each line has a short comment saying WHAT it is.

import math
import re
import zlib
from collections import Counter
from pathlib import Path

import numpy as np

# Path(...).exists(): True if the folder exists; picks whichever data folder is found.
DATA = Path("data") if Path("data").exists() else Path("../data")
# STOP: 'stop words' = very common words we ignore because they carry little meaning.
STOP = {"the", "a", "an", "of", "to", "and", "is", "are", "in", "on", "for", "or", "do", "i", "my", "can", "you", "it", "we", "how", "what", "does", "after", "within"}


# tokens(text): lowercase words without stop words.
def tokens(text):
    return [w for w in re.findall(r"[a-z0-9$]+", text.lower()) if w not in STOP]


# read_text(): read the file as one string.
text = (DATA / "05_company_faq.md").read_text()
# docs: one text per '## ' section.
docs = []
# re.split: cut before each '## ' heading.
for part in re.split(r"\n(?=## )", text):
    if part.startswith("## "):
        # partition("\n"): split at the first newline into title and body.
        title, _, body = part.partition("\n")
        docs.append(f"{title.removeprefix('## ')}: {body.strip()}")
print(len(docs), "documents")

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Keyword search with BM25 (still beats embeddings for exact terms like IDs and names)
# BM25: a keyword scoring method; rare words that appear often in a doc score high.
class BM25:
    # k1 and b: tuning knobs (word-repeat effect, length effect).
    def __init__(self, documents, k1=1.5, b=0.75):
        self.docs = [tokens(d) for d in documents]
        self.k1, self.b = k1, b
        # avg_len: average document length in words.
        self.avg_len = sum(len(d) for d in self.docs) / len(self.docs)
        # Counter: counts items; df = in how many documents each word appears.
        df = Counter(word for d in self.docs for word in set(d))
        n = len(self.docs)
        # idf: rarer words get a bigger weight; log is a maths function.
        self.idf = {w: math.log((n - c + 0.5) / (c + 0.5) + 1) for w, c in df.items()}

    # scores(query): one score per document for the query.
    def scores(self, query):
        # np.zeros(n): array of n zeros.
        result = np.zeros(len(self.docs))
        # enumerate: gives a counter i and each item.
        for i, doc in enumerate(self.docs):
            # counts: how many times each word is in this doc.
            counts = Counter(doc)
            for word in tokens(query):
                if word in counts:
                    # tf = term frequency: times the word appears here.
                    tf = counts[word]
                    # Adjusts for document length so long docs don't win just by size.
                    norm = tf + self.k1 * (1 - self.b + self.b * len(doc) / self.avg_len)
                    result[i] += self.idf[word] * tf * (self.k1 + 1) / norm
        return result


# Build the keyword index.
bm25 = BM25(docs)
query = "refund time"
# np.round(array, 2): round to 2 decimals.
print(np.round(bm25.scores(query), 2))
# np.argmax: position of the biggest score.
print(docs[int(np.argmax(bm25.scores(query)))][:60])

# %% Vector search (toy) for comparison
# DIM: how many numbers each vector has.
DIM = 512


# embed(t): turns text into a vector by counting words into slots (crc32 gives a fixed number per word; % DIM picks the slot).
def embed(t):
    v = np.zeros(DIM)
    for w in tokens(t):
        v[zlib.crc32(w.encode()) % DIM] += 1
    n = np.linalg.norm(v)
    return v / n if n else v


# matrix: one row (vector) per document.
matrix = np.array([embed(d) for d in docs])

# %% Hybrid: combine both rankings with Reciprocal Rank Fusion
# rrf = Reciprocal Rank Fusion: combines several rankings; higher positions earn more points (1 / (k + position)).
def rrf(rankings, k=60):
    # Counter that adds up points per document.
    scores = Counter()
    for ranking in rankings:
        # enumerate(ranking): position 0 is the best.
        for position, doc_index in enumerate(ranking):
            scores[doc_index] += 1 / (k + position + 1)
    # most_common(): items sorted by points, highest first.
    return [index for index, _ in scores.most_common()]


# hybrid_search: combines keyword and vector rankings.
def hybrid_search(query, top=3):
    # np.argsort(scores)[::-1]: document positions from best to worst score.
    keyword_rank = list(np.argsort(bm25.scores(query))[::-1])
    # matrix @ embed(query): similarity of the query to every doc.
    vector_rank = list(np.argsort(matrix @ embed(query))[::-1])
    return rrf([keyword_rank, vector_rank])[:top]


# Try three queries; split(':')[0] = the section title before the colon.
for q in ["refund time", "free shipping threshold", "2FA password"]:
    print(q, "->", [docs[i].split(":")[0] for i in hybrid_search(q)])

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Rerank: a second, smarter step on the top results
# 1. Retrieve 20 candidates quickly (cheap).
# 2. Rerank them with a cross-encoder or an LLM that reads query + chunk together (slower, better).
# 3. Send the best 3-5 to the prompt.
# fake_rerank: stand-in reranker that prefers chunks sharing the most query words.
def fake_rerank(query, candidates):
    """Stand-in: prefer chunks that share the most query words."""
    # set: unique words only.
    query_words = set(tokens(query))
    # sorted(key=...): sort by a score; the minus sign puts the biggest overlap first; & = words in both sets.
    return sorted(candidates, key=lambda c: -len(query_words & set(tokens(docs[c]))))


print([docs[i].split(":")[0] for i in fake_rerank("return shoes refund", hybrid_search("return shoes refund", 4))])

# %% Query rewriting: users write messy questions
# "it broke how long do i have" + chat history  ->  "How long is the warranty on electronics?"
# Ask an LLM to rewrite the question into a clear standalone search query.
# A template text with {history} and {message} blanks to fill in with .format().
REWRITE_PROMPT = """Rewrite the latest user message as a standalone search query.
Chat history:
{history}
Latest message: {message}
Search query:"""
print(REWRITE_PROMPT.format(history="user: I bought a laptop", message="how long is it covered?"))

# %% Other improvements
# - Metadata filters (product, language, date, access rights)
# - Parent-child chunks: search small, send the surrounding big chunk
# - Multi-query: search several rewrites and merge
# - Return top-k with a score threshold, if nothing is good enough say "I don't know"
