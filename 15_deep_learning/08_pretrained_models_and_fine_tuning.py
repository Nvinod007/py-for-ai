# In practice you rarely train from scratch. You reuse pretrained models.
# This file explains the options. The Hugging Face parts run only if `transformers` is installed:
#     uv add transformers
# (it downloads models from the internet on first use)
# Each line has a short comment saying WHAT it is.

# torch (PyTorch): tensors and deep learning.
import torch
# nn: neural-network building blocks.
from torch import nn

# try/except ImportError: use transformers if installed, otherwise carry on.
try:
    # pipeline(task): Hugging Face helper that downloads a ready-made model and wraps it in one call.
    from transformers import pipeline
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False

# Shows whether the optional package is available.
print("transformers installed:", HAS_TRANSFORMERS)

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Ways to use a pretrained model (easiest first)
# 1. Call a hosted API (folder 09)                      no GPU, pay per use
# 2. Run an open model with a pipeline                   free, needs RAM/GPU
# 3. Fine-tune a small model on your labelled data       better for narrow tasks
# 4. Train from scratch                                  almost never

# %% Hugging Face pipelines: one line per task
if HAS_TRANSFORMERS:
    # pipeline('sentiment-analysis'): model labelling text positive/negative.
    classifier = pipeline("sentiment-analysis")
    print(classifier(["I love this course", "This is confusing"]))
    # pipeline('feature-extraction', model=...): turns text into embeddings (lists of numbers capturing meaning).
    embedder = pipeline("feature-extraction", model="sentence-transformers/all-MiniLM-L6-v2")
    print(len(embedder("hello world")[0][0]), "dimensional embedding")

# %% Transfer learning with torch only: freeze a "pretrained" body and train a new head
# manual_seed(0): fix randomness so runs repeat.
torch.manual_seed(0)
# nn.Sequential: layers run in order; Linear = weights layer, ReLU = zero out negatives.
body = nn.Sequential(nn.Linear(10, 32), nn.ReLU(), nn.Linear(32, 16), nn.ReLU())     # pretend it is pretrained
# The new final layer for our task (2 classes).
head = nn.Linear(16, 2)                                                                # new task: 2 classes

# parameters(): all learnable numbers.
for parameter in body.parameters():
    # requires_grad=False: freeze, no gradients so the weights stay the same.
    parameter.requires_grad = False                    # frozen: weights will not change

# Join the body and head.
model = nn.Sequential(body, head)
# numel(): count of items; counts only unfrozen parameters.
trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
# Count of all parameters.
total = sum(p.numel() for p in model.parameters())
print(f"training {trainable} of {total} parameters")

# randn(200, 10): 200 rows of 10 random numbers.
X = torch.randn(200, 10)
# Label rule: 1 if the first two columns add to > 0; long() = whole numbers.
y = (X[:, 0] + X[:, 1] > 0).long()
# Adam optimizer: updates only the head's weights; lr = learning rate (step size).
optimizer = torch.optim.Adam(head.parameters(), lr=0.05)
# Training loop (200 rounds).
for _ in range(200):
    # cross_entropy: loss (how wrong) for multi-class answers.
    loss = nn.functional.cross_entropy(model(X), y)
    # zero_grad(): clear old gradients.
    optimizer.zero_grad()
    # backward(): compute gradients.
    loss.backward()
    # step(): update weights.
    optimizer.step()
# argmax(1): pick the highest-scoring class; compare with y; mean() = share correct; item() = plain number.
print("train accuracy:", (model(X).argmax(1) == y).float().mean().item())


# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Fine-tuning large language models
# Full fine-tuning: update every weight (needs lots of GPU memory).
# LoRA / QLoRA: train small adapter matrices only (cheap, popular, `peft` library).
# Before fine-tuning, try: better prompts, few-shot examples, RAG (folder 10).
# Fine-tune when you need a consistent style/format or a small fast model for one task.

# %% Evaluation matters more than the training trick (folder 16)

# %% Where to go next
# Hugging Face course (free)  |  fast.ai  |  Andrej Karpathy "Neural Networks: Zero to Hero"
# Papers to read once you are comfortable: "Attention Is All You Need", GPT-3, LoRA, RAG.
