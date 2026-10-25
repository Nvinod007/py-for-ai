# An embedding turns text into a list of numbers (a vector).
# Similar meaning -> vectors that point in a similar direction.
#
# Real embeddings come from a model (OpenAI, Cohere, sentence-transformers).
# To learn without a key, we build a simple word-based embedding ourselves.

import os
import re
import zlib

import numpy as np
from openai import OpenAI

# %% Toy embedding: count words into a fixed-size vector (hashing trick)
DIM = 256


def embed(text):
    vector = np.zeros(DIM)
    for word in re.findall(r"[a-z0-9]+", text.lower()):
        vector[zlib.crc32(word.encode()) % DIM] += 1      # same result on every run
    norm = np.linalg.norm(vector)
    return vector / norm if norm else vector          # length 1


a = embed("Items can be returned within 30 days")
print(a.shape, round(float(np.linalg.norm(a)), 3))

# %% Similarity measures
def cosine(u, v):
    return float(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v)))


query = embed("How many days do I have to return an item?")
docs = {
    "returns": embed("Items can be returned within 30 days for a refund"),
    "shipping": embed("Standard shipping takes 3 to 5 business days"),
    "payments": embed("We accept Visa, Mastercard and PayPal"),
}
for name, vector in docs.items():
    print(f"{name:10} cosine={cosine(query, vector):.3f}")

# %% Cosine vs dot product vs distance
u = np.array([1.0, 2.0, 3.0])
v = np.array([2.0, 4.0, 6.0])               # same direction, double the length
print("cosine   :", cosine(u, v))             # 1.0 (direction only)
print("dot      :", float(u @ v))             # depends on length
print("euclidean:", float(np.linalg.norm(u - v)))
# If vectors are normalized to length 1, dot product == cosine similarity.

# %% Toy limits: no real meaning, only shared words
print(cosine(embed("car"), embed("automobile")))     # ~0, a real model gives a high score
print(cosine(embed("car"), embed("car")))             # 1

# %% What real embeddings give you
# "car" and "automobile" land close together, "bank" (river) and "bank" (money) differ by context.
# Typical sizes: 384, 768, 1536, 3072 numbers per text.

# %% Real embeddings (needs OPENAI_API_KEY, optional)
if os.environ.get("OPENAI_API_KEY"):
    client = OpenAI()
    result = client.embeddings.create(model="text-embedding-3-small", input=["return policy", "refund rules"])
    first, second = (np.array(item.embedding) for item in result.data)
    print(len(first), cosine(first, second))
