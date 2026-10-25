# In practice you rarely train from scratch. You reuse pretrained models.
# This file explains the options. The Hugging Face parts run only if `transformers` is installed:
#     uv add transformers
# (it downloads models from the internet on first use)

import torch
from torch import nn

try:
    from transformers import pipeline
    HAS_TRANSFORMERS = True
except ImportError:
    HAS_TRANSFORMERS = False

print("transformers installed:", HAS_TRANSFORMERS)

# %% Ways to use a pretrained model (easiest first)
# 1. Call a hosted API (folder 09)                      no GPU, pay per use
# 2. Run an open model with a pipeline                   free, needs RAM/GPU
# 3. Fine-tune a small model on your labelled data       better for narrow tasks
# 4. Train from scratch                                  almost never

# %% Hugging Face pipelines: one line per task
if HAS_TRANSFORMERS:
    classifier = pipeline("sentiment-analysis")
    print(classifier(["I love this course", "This is confusing"]))
    embedder = pipeline("feature-extraction", model="sentence-transformers/all-MiniLM-L6-v2")
    print(len(embedder("hello world")[0][0]), "dimensional embedding")

# %% Transfer learning with torch only: freeze a "pretrained" body and train a new head
torch.manual_seed(0)
body = nn.Sequential(nn.Linear(10, 32), nn.ReLU(), nn.Linear(32, 16), nn.ReLU())     # pretend it is pretrained
head = nn.Linear(16, 2)                                                                # new task: 2 classes

for parameter in body.parameters():
    parameter.requires_grad = False                    # frozen: weights will not change

model = nn.Sequential(body, head)
trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
total = sum(p.numel() for p in model.parameters())
print(f"training {trainable} of {total} parameters")

X = torch.randn(200, 10)
y = (X[:, 0] + X[:, 1] > 0).long()
optimizer = torch.optim.Adam(head.parameters(), lr=0.05)
for _ in range(200):
    loss = nn.functional.cross_entropy(model(X), y)
    optimizer.zero_grad()
    loss.backward()
    optimizer.step()
print("train accuracy:", (model(X).argmax(1) == y).float().mean().item())

# %% Fine-tuning large language models
# Full fine-tuning: update every weight (needs lots of GPU memory).
# LoRA / QLoRA: train small adapter matrices only (cheap, popular, `peft` library).
# Before fine-tuning, try: better prompts, few-shot examples, RAG (folder 10).
# Fine-tune when you need a consistent style/format or a small fast model for one task.

# %% Evaluation matters more than the training trick (folder 16)

# %% Where to go next
# Hugging Face course (free)  |  fast.ai  |  Andrej Karpathy "Neural Networks: Zero to Hero"
# Papers to read once you are comfortable: "Attention Is All You Need", GPT-3, LoRA, RAG.
