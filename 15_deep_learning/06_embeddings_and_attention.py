# Two ideas behind every modern language model: embeddings and attention.
# Each line has a short comment saying WHAT it is.

# numpy: array maths.
import numpy as np
# torch (PyTorch): tensors and deep learning.
import torch
# nn: neural-network building blocks.
from torch import nn

# manual_seed(0): fix randomness so runs repeat.
torch.manual_seed(0)

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Text must become numbers: tokens -> ids -> vectors
# vocab: dictionary mapping each word to an id number.
vocab = {"<pad>": 0, "the": 1, "cat": 2, "dog": 3, "sat": 4, "on": 5, "mat": 6, "ran": 7}
# split(): breaks text into a list of words.
sentence = "the cat sat on the mat".split()
# torch.tensor(list): list of ids -> tensor.
ids = torch.tensor([vocab[word] for word in sentence])
print(ids)

# %% An embedding layer is just a lookup table of learnable vectors
# nn.Embedding(num_embeddings, embedding_dim): a lookup table giving each id a learnable list of numbers (an embedding = a vector that represents meaning).
embedding = nn.Embedding(num_embeddings=len(vocab), embedding_dim=4)
# Look up the vector for each id.
vectors = embedding(ids)
# shape: size of each dimension.
print(vectors.shape)                                   # (6 words, 4 numbers each)
print(embedding.weight.shape)

# %% Self-attention by hand (NumPy): each word looks at every other word
# softmax: turns scores into positive numbers that add up to 1 (like percentages); subtracting the max keeps numbers stable.
def softmax(scores):
    exp = np.exp(scores - scores.max(axis=-1, keepdims=True))
    return exp / exp.sum(axis=-1, keepdims=True)


# np.random.default_rng(0): random maker with a fixed seed.
rng = np.random.default_rng(0)
# tokens = number of words; d = numbers per word.
tokens, d = 4, 8
# rng.normal(size=...): random bell-curve numbers standing in for word vectors.
x = rng.normal(size=(tokens, d))                       # 4 words, 8 numbers each
# Three weight matrices (Wq, Wk, Wv); / np.sqrt(d) keeps values small.
Wq, Wk, Wv = (rng.normal(size=(d, d)) / np.sqrt(d) for _ in range(3))

# '@' = matrix multiplication. Query = what a word looks for, key = what it offers, value = what it hands over.
queries, keys, values = x @ Wq, x @ Wk, x @ Wv         # what I look for / what I offer / what I give
# keys.T = transpose; dot products show how much each word cares about others.
scores = queries @ keys.T / np.sqrt(d)                 # how much each word cares about each other word
# softmax makes each row add up to 1 (attention weights).
weights = softmax(scores)                              # rows sum to 1
# Each word becomes a weighted mix of the values.
output = weights @ values                              # a weighted mix of the other words
# round(2): 2 decimals.
print(weights.round(2))
# sum(axis=1): total of each row (should be 1).
print(weights.sum(axis=1))
# shape: (words, numbers per word).
print(output.shape)


# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Causal mask: when generating text a word may only look at earlier words
# np.triu(..., k=1): keeps only the upper triangle (the future words); astype(bool): True/False.
mask = np.triu(np.ones((tokens, tokens)), k=1).astype(bool)
# np.where(cond, a, b): use a where True, else b; -1e9 makes softmax give those words ~0.
masked_scores = np.where(mask, -1e9, scores)
# Upper triangle is 0: words can't see the future.
print(softmax(masked_scores).round(2))                 # upper triangle is zero

# %% The same thing in PyTorch, with several "heads"
# MultiheadAttention(embed_dim, num_heads, batch_first=True): attention with several 'heads' looking at different things; batch_first = data shaped (batch, words, numbers).
attention = nn.MultiheadAttention(embed_dim=8, num_heads=2, batch_first=True)
# randn(1, words, 8): random numbers standing in for one sentence.
batch = torch.randn(1, tokens, 8)
# Passing the same input as query, key and value = self-attention.
out, attn_weights = attention(batch, batch, batch)
# Output keeps the same shape; weights show who looked at whom.
print(out.shape, attn_weights.shape)

# %% Position matters: attention alone ignores word order, so we add position information
# Builds a table of position codes using sin/cos waves, so the model knows word order.
def sinusoidal_positions(length, dim):
    # np.arange(length)[:, None]: 0..length-1 as a column.
    positions = np.arange(length)[:, None]
    # Wave speeds, from fast to slow.
    freqs = np.exp(-np.log(10000) * np.arange(0, dim, 2) / dim)
    # np.zeros: empty table to fill.
    table = np.zeros((length, dim))
    # Even columns get sin; odd columns (1::2) get cos.
    table[:, 0::2] = np.sin(positions * freqs)
    table[:, 1::2] = np.cos(positions * freqs)
    return table


# First 4 positions, 8 numbers each.
print(sinusoidal_positions(4, 8).round(2))

# %% Similar meanings, close vectors (same idea as folder 10)
# Training teaches the embedding table that "cat" and "dog" appear in similar contexts,
# so their vectors move close together.
