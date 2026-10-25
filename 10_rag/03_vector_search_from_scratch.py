# A vector store = embeddings + metadata + fast "give me the nearest ones".
# We build a small one with NumPy so you see there is no magic.
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
STOP = {"the", "a", "an", "of", "to", "and", "is", "are", "in", "on", "for", "or", "do", "i", "my", "can", "you", "it", "we", "how", "what"}


# embed(text): turns text into a vector by counting non-stop words.
def embed(text):
    # np.zeros(n): array of n zeros to fill in.
    vector = np.zeros(DIM)
    # re.findall(pattern, text): all pieces matching the pattern; [a-z0-9]+ = runs of letters/digits; lower() = lowercase.
    for word in re.findall(r"[a-z0-9]+", text.lower()):
        if word not in STOP:
            # crc32(word.encode()): turns the word into a fixed number; % DIM picks a slot; += 1 counts it (the 'hashing trick').
            vector[zlib.crc32(word.encode()) % DIM] += 1
    # np.linalg.norm(v): the vector's length.
    norm = np.linalg.norm(vector)
    # Divide by length so the vector has length 1 (normalized); if length is 0 return it unchanged.
    return vector / norm if norm else vector


# load_chunks: reads the FAQ and returns a list of {section, text} dictionaries.
def load_chunks():
    # read_text(): read the file as one string.
    text = (DATA / "05_company_faq.md").read_text()
    chunks = []
    # re.split: cut the text before each '## ' heading.
    for part in re.split(r"\n(?=## )", text):
        if part.startswith("## "):
            # partition("\n"): split at the first newline into title and body.
            title, _, body = part.partition("\n")
            # (?<=[.!?])\s+: split after . ! or ? (sentences).
            for sentence_group in re.split(r"(?<=[.!?])\s+", body.strip()):
                chunks.append({"section": title.removeprefix("## ").strip(), "text": sentence_group})
    return chunks

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% A minimal vector store
# VectorStore: a class = a blueprint bundling data (items, matrix) and actions (add, search).
class VectorStore:
    # __init__: runs when you create the store; self = this store.
    def __init__(self):
        self.items = []
        # np.empty((0, DIM)): an empty table with 0 rows and DIM columns.
        self.matrix = np.empty((0, DIM))

    # add(items): embed each item and store it.
    def add(self, items):
        # np.array(list of vectors): one 2D table, one row per item.
        vectors = np.array([embed(f"{i['section']}: {i['text']}") for i in items])
        # extend: add all items from a list.
        self.items.extend(items)
        # np.vstack: stack arrays on top of each other (add new rows).
        self.matrix = np.vstack([self.matrix, vectors])

    # search(query, k): returns the k best matching items with scores.
    def search(self, query, k=3):
        # matrix @ vector: dot product with every row at once; since vectors have length 1 this equals cosine similarity.
        scores = self.matrix @ embed(query)               # cosine, vectors are normalized
        # np.argsort: positions that would sort the scores (smallest first); [::-1] reverses to biggest first; [:k] keeps the first k.
        top = np.argsort(scores)[::-1][:k]
        return [(float(scores[i]), self.items[i]) for i in top]


# Create the store, then add all chunks.
store = VectorStore()
store.add(load_chunks())
# matrix.shape: (rows, columns).
print(len(store.items), "chunks,", store.matrix.shape)

# %% Search
# Try several questions; each prints its top 2 matches.
for question in [
    "How long do I have to return something?",
    "Does shipping cost money?",
    "Which payment cards do you take?",
    "when does support answer",
]:
    print("\nQ:", question)
    for score, item in store.search(question, k=2):
        # [:80] = first 80 characters; :.2f = 2 decimals.
        print(f"  {score:.2f} [{item['section']}] {item['text'][:80]}")

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Filtering by metadata
# search_in_section: like search but only inside one section.
def search_in_section(query, section, k=2):
    # mask: array of True/False, True where the item is in that section.
    mask = np.array([item["section"] == section for item in store.items])
    # np.where(test, a, b): use a where test is True, else b (-1 hides other sections).
    scores = np.where(mask, store.matrix @ embed(query), -1)
    return [store.items[i]["text"] for i in np.argsort(scores)[::-1][:k]]


print(search_in_section("how many days", "Returns"))

# %% Brute force is fine up to ~100k vectors. Beyond that use a vector database:
# Chroma, FAISS, pgvector (Postgres), Qdrant, Pinecone, Weaviate. They use approximate
# nearest neighbour indexes (HNSW) to stay fast with millions of vectors.

# %% Save and load the index
# out: the output folder path.
out = DATA / "output"
# mkdir(exist_ok=True): create the folder, no error if it exists.
out.mkdir(exist_ok=True)
# np.save(file, array): save an array to a .npy file.
np.save(out / "faq_vectors.npy", store.matrix)
# np.load(file): read the saved array back.
print(np.load(out / "faq_vectors.npy").shape)
