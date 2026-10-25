# An embedding turns text into a list of numbers (a vector).
# Similar meaning -> vectors that point in a similar direction.
#
# Real embeddings come from a model (OpenAI, Cohere, sentence-transformers).
# To learn without a key, we build a simple word-based embedding ourselves.
# Each line has a short comment saying WHAT it is.

import os
import re
import zlib

import numpy as np
from openai import OpenAI

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Toy embedding: count words into a fixed-size vector (hashing trick)
# DIM: how many numbers each vector has.
DIM = 256


# embed(text): turns text into a vector (list of numbers) by counting words.
def embed(text):
    # np.zeros(n): array of n zeros to fill in.
    vector = np.zeros(DIM)
    # re.findall(pattern, text): all pieces matching the pattern; [a-z0-9]+ = runs of letters/digits; lower() = lowercase.
    for word in re.findall(r"[a-z0-9]+", text.lower()):
        # crc32(word.encode()): turns the word into a fixed number; % DIM picks a slot; += 1 counts it (the 'hashing trick').
        vector[zlib.crc32(word.encode()) % DIM] += 1      # same result on every run
    # np.linalg.norm(v): the vector's length.
    norm = np.linalg.norm(vector)
    # Divide by length so the vector has length 1 (normalized); if length is 0 return it unchanged.
    return vector / norm if norm else vector          # length 1


# shape: size of the array (256 numbers); round(x, 3): 3 decimals; float(): plain number.
a = embed("Items can be returned within 30 days")
print(a.shape, round(float(np.linalg.norm(a)), 3))

# %% Similarity measures
# cosine similarity: how much two vectors point the same way (1 = same, 0 = unrelated). np.dot = multiply pairwise and add up; dividing by the lengths removes the size effect.
def cosine(u, v):
    return float(np.dot(u, v) / (np.linalg.norm(u) * np.linalg.norm(v)))


# query: the question as a vector.
query = embed("How many days do I have to return an item?")
# docs: dictionary of name -> vector for each text.
docs = {
    "returns": embed("Items can be returned within 30 days for a refund"),
    "shipping": embed("Standard shipping takes 3 to 5 business days"),
    "payments": embed("We accept Visa, Mastercard and PayPal"),
}
# items(): gives key and value; :10 pads the name; :.3f = 3 decimals.
for name, vector in docs.items():
    print(f"{name:10} cosine={cosine(query, vector):.3f}")

# %% What real embeddings give you
# "car" and "automobile" land close together, "bank" (river) and "bank" (money) differ by context.
# Typical sizes: 384, 768, 1536, 3072 numbers per text.

# %% Real embeddings (needs OPENAI_API_KEY, optional)
# os.environ.get(NAME): reads a setting from the terminal; None if missing.
if os.environ.get("OPENAI_API_KEY"):
    # OpenAI(): creates the API client (reads the key from settings).
    client = OpenAI()
    # embeddings.create(model, input): asks the API for vectors; model = which embedding model, input = list of texts.
    result = client.embeddings.create(model="text-embedding-3-small", input=["return policy", "refund rules"])
    # Generator: np.array(item.embedding) turns each returned vector into an array; unpacked into two variables.
    first, second = (np.array(item.embedding) for item in result.data)
    # len(first): how many numbers in one embedding.
    print(len(first), cosine(first, second))

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Cosine vs dot product vs distance
# np.array(list): make a NumPy array of numbers.
u = np.array([1.0, 2.0, 3.0])
v = np.array([2.0, 4.0, 6.0])               # same direction, double the length
# cosine: same direction = 1.0 even if lengths differ.
print("cosine   :", cosine(u, v))             # 1.0 (direction only)
# u @ v: dot product (multiply pairwise, then add up); bigger when vectors are longer.
print("dot      :", float(u @ v))             # depends on length
# euclidean distance: straight-line distance between the two points (np.linalg.norm of the difference).
print("euclidean:", float(np.linalg.norm(u - v)))
# If vectors are normalized to length 1, dot product == cosine similarity.

# %% Toy limits: no real meaning, only shared words
# Different words share no slots, so the toy score is ~0.
print(cosine(embed("car"), embed("automobile")))     # ~0, a real model gives a high score
print(cosine(embed("car"), embed("car")))             # 1
