# A tiny transformer language model that learns to continue a short text.
# It is a toy, but it contains the same parts as real LLMs.

import torch
import torch.nn.functional as F
from torch import nn

torch.manual_seed(0)

# %% Data: characters of a small repeating text
text = "the cat sat on the mat. the dog sat on the log. " * 20
chars = sorted(set(text))
stoi = {c: i for i, c in enumerate(chars)}
itos = {i: c for c, i in stoi.items()}
data = torch.tensor([stoi[c] for c in text])
print(len(chars), "characters in the vocabulary:", "".join(chars))

BLOCK = 16                                              # how many characters the model sees at once


def get_batch(batch_size=32):
    starts = torch.randint(0, len(data) - BLOCK - 1, (batch_size,))
    x = torch.stack([data[i : i + BLOCK] for i in starts])
    y = torch.stack([data[i + 1 : i + BLOCK + 1] for i in starts])      # next character at every position
    return x, y


x, y = get_batch(2)
print(x[0].tolist(), y[0].tolist())


# %% One transformer block = attention + feed-forward, each with residual connection and normalization
class Block(nn.Module):
    def __init__(self, dim, heads):
        super().__init__()
        self.norm1, self.norm2 = nn.LayerNorm(dim), nn.LayerNorm(dim)
        self.attention = nn.MultiheadAttention(dim, heads, batch_first=True)
        self.ff = nn.Sequential(nn.Linear(dim, 4 * dim), nn.GELU(), nn.Linear(4 * dim, dim))

    def forward(self, x):
        length = x.size(1)
        causal = torch.triu(torch.ones(length, length, dtype=torch.bool), diagonal=1)
        h = self.norm1(x)
        attended, _ = self.attention(h, h, h, attn_mask=causal, need_weights=False)
        x = x + attended                                # residual: add the input back
        return x + self.ff(self.norm2(x))


class TinyGPT(nn.Module):
    def __init__(self, vocab_size, dim=48, heads=4, layers=2):
        super().__init__()
        self.tokens = nn.Embedding(vocab_size, dim)
        self.positions = nn.Embedding(BLOCK, dim)
        self.blocks = nn.Sequential(*[Block(dim, heads) for _ in range(layers)])
        self.norm = nn.LayerNorm(dim)
        self.head = nn.Linear(dim, vocab_size)

    def forward(self, ids):
        positions = torch.arange(ids.size(1))
        h = self.tokens(ids) + self.positions(positions)
        return self.head(self.norm(self.blocks(h)))      # a score for every possible next character


model = TinyGPT(len(chars))
print("parameters:", sum(p.numel() for p in model.parameters()))

# %% Train: predict the next character
optimizer = torch.optim.AdamW(model.parameters(), lr=3e-3)
for step in range(1, 401):
    xb, yb = get_batch()
    logits = model(xb)
    loss = F.cross_entropy(logits.reshape(-1, len(chars)), yb.reshape(-1))
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
    if step % 100 == 0 or step == 1:
        print(f"step {step:3d} loss={loss.item():.3f}")


# %% Generate text one character at a time
@torch.no_grad()
def generate(prompt, length=60, temperature=1.0, top_k=None):
    ids = torch.tensor([[stoi[c] for c in prompt]])
    for _ in range(length):
        logits = model(ids[:, -BLOCK:])[:, -1, :] / max(temperature, 1e-6)
        if top_k:
            cutoff = torch.topk(logits, top_k).values[:, -1:]
            logits = logits.masked_fill(logits < cutoff, float("-inf"))
        next_id = torch.multinomial(F.softmax(logits, dim=-1), 1)
        ids = torch.cat([ids, next_id], dim=1)
    return "".join(itos[i] for i in ids[0].tolist())


print(repr(generate("the cat ", temperature=0.5)))

# %% Temperature and top-k control creativity (the same knobs as in LLM APIs)
for temperature in (0.2, 1.0, 2.0):
    print(f"temperature {temperature}:", repr(generate("the ", length=30, temperature=temperature, top_k=5)))

# %% Map to a real LLM
# characters -> tokens (words/pieces)    48 dims -> thousands    2 blocks -> dozens
# 50 thousand parameters -> billions     toy text -> trillions of tokens
# Pretraining = next-token prediction on huge text. Then instruction tuning and RLHF
# turn the base model into a helpful assistant.
