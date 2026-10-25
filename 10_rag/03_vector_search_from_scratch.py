# A vector store = embeddings + metadata + fast "give me the nearest ones".
# We build a small one with NumPy so you see there is no magic.

import re
import zlib
from pathlib import Path

import numpy as np

DATA = Path("data") if Path("data").exists() else Path("../data")
DIM = 512
STOP = {"the", "a", "an", "of", "to", "and", "is", "are", "in", "on", "for", "or", "do", "i", "my", "can", "you", "it", "we", "how", "what"}


def embed(text):
    vector = np.zeros(DIM)
    for word in re.findall(r"[a-z0-9]+", text.lower()):
        if word not in STOP:
            vector[zlib.crc32(word.encode()) % DIM] += 1
    norm = np.linalg.norm(vector)
    return vector / norm if norm else vector


def load_chunks():
    text = (DATA / "05_company_faq.md").read_text()
    chunks = []
    for part in re.split(r"\n(?=## )", text):
        if part.startswith("## "):
            title, _, body = part.partition("\n")
            for sentence_group in re.split(r"(?<=[.!?])\s+", body.strip()):
                chunks.append({"section": title.removeprefix("## ").strip(), "text": sentence_group})
    return chunks


# %% A minimal vector store
class VectorStore:
    def __init__(self):
        self.items = []
        self.matrix = np.empty((0, DIM))

    def add(self, items):
        vectors = np.array([embed(f"{i['section']}: {i['text']}") for i in items])
        self.items.extend(items)
        self.matrix = np.vstack([self.matrix, vectors])

    def search(self, query, k=3):
        scores = self.matrix @ embed(query)               # cosine, vectors are normalized
        top = np.argsort(scores)[::-1][:k]
        return [(float(scores[i]), self.items[i]) for i in top]


store = VectorStore()
store.add(load_chunks())
print(len(store.items), "chunks,", store.matrix.shape)

# %% Search
for question in [
    "How long do I have to return something?",
    "Does shipping cost money?",
    "Which payment cards do you take?",
    "when does support answer",
]:
    print("\nQ:", question)
    for score, item in store.search(question, k=2):
        print(f"  {score:.2f} [{item['section']}] {item['text'][:80]}")

# %% Filtering by metadata
def search_in_section(query, section, k=2):
    mask = np.array([item["section"] == section for item in store.items])
    scores = np.where(mask, store.matrix @ embed(query), -1)
    return [store.items[i]["text"] for i in np.argsort(scores)[::-1][:k]]


print(search_in_section("how many days", "Returns"))

# %% Brute force is fine up to ~100k vectors. Beyond that use a vector database:
# Chroma, FAISS, pgvector (Postgres), Qdrant, Pinecone, Weaviate. They use approximate
# nearest neighbour indexes (HNSW) to stay fast with millions of vectors.

# %% Save and load the index
out = DATA / "output"
out.mkdir(exist_ok=True)
np.save(out / "faq_vectors.npy", store.matrix)
print(np.load(out / "faq_vectors.npy").shape)
