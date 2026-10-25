# Two ideas behind every modern language model: embeddings and attention.

import numpy as np
import torch
from torch import nn

torch.manual_seed(0)

# %% Text must become numbers: tokens -> ids -> vectors
vocab = {"<pad>": 0, "the": 1, "cat": 2, "dog": 3, "sat": 4, "on": 5, "mat": 6, "ran": 7}
sentence = "the cat sat on the mat".split()
ids = torch.tensor([vocab[word] for word in sentence])
print(ids)

# %% An embedding layer is just a lookup table of learnable vectors
embedding = nn.Embedding(num_embeddings=len(vocab), embedding_dim=4)
vectors = embedding(ids)
print(vectors.shape)                                   # (6 words, 4 numbers each)
print(embedding.weight.shape)

# %% Self-attention by hand (NumPy): each word looks at every other word
def softmax(scores):
    exp = np.exp(scores - scores.max(axis=-1, keepdims=True))
    return exp / exp.sum(axis=-1, keepdims=True)


rng = np.random.default_rng(0)
tokens, d = 4, 8
x = rng.normal(size=(tokens, d))                       # 4 words, 8 numbers each
Wq, Wk, Wv = (rng.normal(size=(d, d)) / np.sqrt(d) for _ in range(3))

queries, keys, values = x @ Wq, x @ Wk, x @ Wv         # what I look for / what I offer / what I give
scores = queries @ keys.T / np.sqrt(d)                 # how much each word cares about each other word
weights = softmax(scores)                              # rows sum to 1
output = weights @ values                              # a weighted mix of the other words
print(weights.round(2))
print(weights.sum(axis=1))
print(output.shape)

# %% Causal mask: when generating text a word may only look at earlier words
mask = np.triu(np.ones((tokens, tokens)), k=1).astype(bool)
masked_scores = np.where(mask, -1e9, scores)
print(softmax(masked_scores).round(2))                 # upper triangle is zero

# %% The same thing in PyTorch, with several "heads"
attention = nn.MultiheadAttention(embed_dim=8, num_heads=2, batch_first=True)
batch = torch.randn(1, tokens, 8)
out, attn_weights = attention(batch, batch, batch)
print(out.shape, attn_weights.shape)

# %% Position matters: attention alone ignores word order, so we add position information
def sinusoidal_positions(length, dim):
    positions = np.arange(length)[:, None]
    freqs = np.exp(-np.log(10000) * np.arange(0, dim, 2) / dim)
    table = np.zeros((length, dim))
    table[:, 0::2] = np.sin(positions * freqs)
    table[:, 1::2] = np.cos(positions * freqs)
    return table


print(sinusoidal_positions(4, 8).round(2))

# %% Similar meanings, close vectors (same idea as folder 10)
# Training teaches the embedding table that "cat" and "dog" appear in similar contexts,
# so their vectors move close together.
