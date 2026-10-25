# Improving retrieval: keyword search, hybrid search, reranking, query rewriting.

import math
import re
import zlib
from collections import Counter
from pathlib import Path

import numpy as np

DATA = Path("data") if Path("data").exists() else Path("../data")
STOP = {"the", "a", "an", "of", "to", "and", "is", "are", "in", "on", "for", "or", "do", "i", "my", "can", "you", "it", "we", "how", "what", "does", "after", "within"}


def tokens(text):
    return [w for w in re.findall(r"[a-z0-9$]+", text.lower()) if w not in STOP]


text = (DATA / "05_company_faq.md").read_text()
docs = []
for part in re.split(r"\n(?=## )", text):
    if part.startswith("## "):
        title, _, body = part.partition("\n")
        docs.append(f"{title.removeprefix('## ')}: {body.strip()}")
print(len(docs), "documents")

# %% Keyword search with BM25 (still beats embeddings for exact terms like IDs and names)
class BM25:
    def __init__(self, documents, k1=1.5, b=0.75):
        self.docs = [tokens(d) for d in documents]
        self.k1, self.b = k1, b
        self.avg_len = sum(len(d) for d in self.docs) / len(self.docs)
        df = Counter(word for d in self.docs for word in set(d))
        n = len(self.docs)
        self.idf = {w: math.log((n - c + 0.5) / (c + 0.5) + 1) for w, c in df.items()}

    def scores(self, query):
        result = np.zeros(len(self.docs))
        for i, doc in enumerate(self.docs):
            counts = Counter(doc)
            for word in tokens(query):
                if word in counts:
                    tf = counts[word]
                    norm = tf + self.k1 * (1 - self.b + self.b * len(doc) / self.avg_len)
                    result[i] += self.idf[word] * tf * (self.k1 + 1) / norm
        return result


bm25 = BM25(docs)
query = "refund time"
print(np.round(bm25.scores(query), 2))
print(docs[int(np.argmax(bm25.scores(query)))][:60])

# %% Vector search (toy) for comparison
DIM = 512


def embed(t):
    v = np.zeros(DIM)
    for w in tokens(t):
        v[zlib.crc32(w.encode()) % DIM] += 1
    n = np.linalg.norm(v)
    return v / n if n else v


matrix = np.array([embed(d) for d in docs])

# %% Hybrid: combine both rankings with Reciprocal Rank Fusion
def rrf(rankings, k=60):
    scores = Counter()
    for ranking in rankings:
        for position, doc_index in enumerate(ranking):
            scores[doc_index] += 1 / (k + position + 1)
    return [index for index, _ in scores.most_common()]


def hybrid_search(query, top=3):
    keyword_rank = list(np.argsort(bm25.scores(query))[::-1])
    vector_rank = list(np.argsort(matrix @ embed(query))[::-1])
    return rrf([keyword_rank, vector_rank])[:top]


for q in ["refund time", "free shipping threshold", "2FA password"]:
    print(q, "->", [docs[i].split(":")[0] for i in hybrid_search(q)])

# %% Rerank: a second, smarter step on the top results
# 1. Retrieve 20 candidates quickly (cheap).
# 2. Rerank them with a cross-encoder or an LLM that reads query + chunk together (slower, better).
# 3. Send the best 3-5 to the prompt.
def fake_rerank(query, candidates):
    """Stand-in: prefer chunks that share the most query words."""
    query_words = set(tokens(query))
    return sorted(candidates, key=lambda c: -len(query_words & set(tokens(docs[c]))))


print([docs[i].split(":")[0] for i in fake_rerank("return shoes refund", hybrid_search("return shoes refund", 4))])

# %% Query rewriting: users write messy questions
# "it broke how long do i have" + chat history  ->  "How long is the warranty on electronics?"
# Ask an LLM to rewrite the question into a clear standalone search query.
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
