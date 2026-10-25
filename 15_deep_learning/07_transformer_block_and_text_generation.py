# A tiny transformer language model that learns to continue a short text.
# It is a toy, but it contains the same parts as real LLMs.
# Each line has a short comment saying WHAT it is.

# torch (PyTorch): tensors and deep learning.
import torch
# F: ready-made functions like softmax and cross_entropy.
import torch.nn.functional as F
# nn: neural-network building blocks.
from torch import nn

# manual_seed(0): fix randomness so runs repeat.
torch.manual_seed(0)

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Data: characters of a small repeating text
# The training text, repeated 20 times.
text = "the cat sat on the mat. the dog sat on the log. " * 20
# set(text): unique characters; sorted(): in order.
chars = sorted(set(text))
# String-to-int: character -> id number; enumerate gives (number, item).
stoi = {c: i for i, c in enumerate(chars)}
# Int-to-string: id -> character (the reverse lookup).
itos = {i: c for c, i in stoi.items()}
# The whole text as a tensor of ids.
data = torch.tensor([stoi[c] for c in text])
# len: count; ''.join(list): glue characters into one text.
print(len(chars), "characters in the vocabulary:", "".join(chars))

# Context length: how many characters the model sees at once.
BLOCK = 16                                              # how many characters the model sees at once


# A batch = a small group of examples used for one update.
def get_batch(batch_size=32):
    # torch.randint(low, high, (n,)): n random start positions.
    starts = torch.randint(0, len(data) - BLOCK - 1, (batch_size,))
    # torch.stack: joins tensors into one; x = a slice of characters.
    x = torch.stack([data[i : i + BLOCK] for i in starts])
    # y = the same slice shifted by one, i.e. the 'next character' answers.
    y = torch.stack([data[i + 1 : i + BLOCK + 1] for i in starts])      # next character at every position
    return x, y


# Peek at two examples; tolist(): tensor -> Python list.
x, y = get_batch(2)
print(x[0].tolist(), y[0].tolist())


# %% One transformer block = attention + feed-forward, each with residual connection and normalization
# nn.Module: base class for models. A transformer block = attention + feed-forward.
class Block(nn.Module):
    # __init__: runs when the object is created; super().__init__() sets up nn.Module.
    def __init__(self, dim, heads):
        super().__init__()
        # nn.LayerNorm(dim): rescales numbers to keep them stable.
        self.norm1, self.norm2 = nn.LayerNorm(dim), nn.LayerNorm(dim)
        # nn.MultiheadAttention(dim, heads, batch_first=True): each position looks at others, with several heads.
        self.attention = nn.MultiheadAttention(dim, heads, batch_first=True)
        # Feed-forward: Linear -> GELU (a smooth activation that adds the 'bend') -> Linear.
        self.ff = nn.Sequential(nn.Linear(dim, 4 * dim), nn.GELU(), nn.Linear(4 * dim, dim))

    # forward(x): how data flows through; called by block(x).
    def forward(self, x):
        # x.size(1): number of positions.
        length = x.size(1)
        # torch.triu(..., diagonal=1): True above the diagonal, marking the future positions to hide.
        causal = torch.triu(torch.ones(length, length, dtype=torch.bool), diagonal=1)
        # Normalize before attention.
        h = self.norm1(x)
        # attn_mask hides the future; need_weights=False skips returning attention weights.
        attended, _ = self.attention(h, h, h, attn_mask=causal, need_weights=False)
        # Residual connection: add the input back so information isn't lost.
        x = x + attended                                # residual: add the input back
        # Feed-forward step, with another residual.
        return x + self.ff(self.norm2(x))


# The full tiny language model.
class TinyGPT(nn.Module):
    def __init__(self, vocab_size, dim=48, heads=4, layers=2):
        super().__init__()
        # nn.Embedding(vocab_size, dim): lookup table; each character id -> list of numbers (an embedding).
        self.tokens = nn.Embedding(vocab_size, dim)
        # A second embedding for the position.
        self.positions = nn.Embedding(BLOCK, dim)
        # nn.Sequential(*[...]): stacks several Blocks; * unpacks the list.
        self.blocks = nn.Sequential(*[Block(dim, heads) for _ in range(layers)])
        # Final normalization.
        self.norm = nn.LayerNorm(dim)
        # Linear layer giving one score per possible next character.
        self.head = nn.Linear(dim, vocab_size)

    def forward(self, ids):
        # arange(n): 0..n-1.
        positions = torch.arange(ids.size(1))
        # Add token and position embeddings.
        h = self.tokens(ids) + self.positions(positions)
        # Run blocks, normalize, then score each next character.
        return self.head(self.norm(self.blocks(h)))      # a score for every possible next character


# Create the model.
model = TinyGPT(len(chars))
# parameters(): all learnable numbers; numel() counts them.
print("parameters:", sum(p.numel() for p in model.parameters()))

# %% Train: predict the next character
# AdamW: optimizer that updates weights from gradients; lr=3e-3 = learning rate (step size).
optimizer = torch.optim.AdamW(model.parameters(), lr=3e-3)
# Each step trains on one batch.
for step in range(1, 401):
    # Get one batch of inputs and answers.
    xb, yb = get_batch()
    # logits = raw scores for each next character.
    logits = model(xb)
    # loss = how wrong; cross_entropy compares scores with the true next characters; reshape flattens batch and positions.
    loss = F.cross_entropy(logits.reshape(-1, len(chars)), yb.reshape(-1))
    # zero_grad(): clear old gradients.
    optimizer.zero_grad()
    # backward(): compute new gradients.
    loss.backward()
    # step(): update the weights.
    optimizer.step()
    # Print on step 1 and every 100.
    if step % 100 == 0 or step == 1:
        print(f"step {step:3d} loss={loss.item():.3f}")


# %% Generate text one character at a time
# @torch.no_grad(): decorator that turns off gradient tracking inside the function (faster).
@torch.no_grad()
# Writes text: predict one character, append it, repeat. temperature = randomness (low = safe, high = wild); top_k = only choose among the k best.
def generate(prompt, length=60, temperature=1.0, top_k=None):
    # Prompt characters -> ids, as a batch of one.
    ids = torch.tensor([[stoi[c] for c in prompt]])
    for _ in range(length):
        # Scores for the last position, divided by temperature.
        logits = model(ids[:, -BLOCK:])[:, -1, :] / max(temperature, 1e-6)
        if top_k:
            # topk(logits, k): the k best scores; keep the smallest of them as the cutoff.
            cutoff = torch.topk(logits, top_k).values[:, -1:]
            # masked_fill: set everything below the cutoff to -infinity (never chosen).
            logits = logits.masked_fill(logits < cutoff, float("-inf"))
        # softmax: scores -> probabilities; multinomial: randomly pick by those probabilities.
        next_id = torch.multinomial(F.softmax(logits, dim=-1), 1)
        # torch.cat: glue the new id onto the end.
        ids = torch.cat([ids, next_id], dim=1)
    # Ids -> characters -> one text.
    return "".join(itos[i] for i in ids[0].tolist())


# repr(): shows the text with quotes.
print(repr(generate("the cat ", temperature=0.5)))


# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Temperature and top-k control creativity (the same knobs as in LLM APIs)
# Try low, medium and high temperature.
for temperature in (0.2, 1.0, 2.0):
    print(f"temperature {temperature}:", repr(generate("the ", length=30, temperature=temperature, top_k=5)))

# %% Map to a real LLM
# characters -> tokens (words/pieces)    48 dims -> thousands    2 blocks -> dozens
# 50 thousand parameters -> billions     toy text -> trillions of tokens
# Pretraining = next-token prediction on huge text. Then instruction tuning and RLHF
# turn the base model into a helpful assistant.
