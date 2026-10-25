# RAG = Retrieval Augmented Generation.
#   1. Retrieve the most relevant chunks for the question.
#   2. Put them in the prompt.
#   3. Ask the model to answer ONLY from them (and cite).
# This is how you make an LLM use your documents without training it.

import os
import re
import zlib
from pathlib import Path

import numpy as np
from openai import OpenAI

DATA = Path("data") if Path("data").exists() else Path("../data")
API_KEY = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=API_KEY) if API_KEY else None
MODEL = "gpt-4o-mini"
DIM = 512
STOP = {"the", "a", "an", "of", "to", "and", "is", "are", "in", "on", "for", "or", "do", "i", "my", "can", "you", "it", "we", "how", "what", "does"}


def embed(text):
    vector = np.zeros(DIM)
    for word in re.findall(r"[a-z0-9]+", text.lower()):
        if word not in STOP:
            vector[zlib.crc32(word.encode()) % DIM] += 1
    norm = np.linalg.norm(vector)
    return vector / norm if norm else vector


# %% Step 1: index the documents
def load_sections():
    text = (DATA / "05_company_faq.md").read_text()
    sections = []
    for part in re.split(r"\n(?=## )", text):
        if part.startswith("## "):
            title, _, body = part.partition("\n")
            sections.append({"section": title.removeprefix("## ").strip(), "text": body.strip()})
    return sections


chunks = load_sections()
matrix = np.array([embed(f"{c['section']} {c['text']}") for c in chunks])
print(len(chunks), "chunks indexed")


# %% Step 2: retrieve
def retrieve(question, k=2):
    scores = matrix @ embed(question)
    top = np.argsort(scores)[::-1][:k]
    return [{**chunks[i], "score": float(scores[i])} for i in top]


for hit in retrieve("Can I return shoes after three weeks?"):
    print(f"{hit['score']:.2f} {hit['section']}")


# %% Step 3: build the prompt
def build_prompt(question, hits):
    context = "\n\n".join(f"[{i + 1}] ({h['section']}) {h['text']}" for i, h in enumerate(hits))
    return [
        {
            "role": "system",
            "content": (
                "You answer customer questions using ONLY the numbered context.\n"
                "Cite sources like [1]. If the context does not contain the answer, say "
                "'I don't know based on the documents.'"
            ),
        },
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
    ]


question = "How long does standard shipping take and what does it cost?"
messages = build_prompt(question, retrieve(question))
print(messages[1]["content"][:400])


# %% Step 4: generate
def answer(question, k=2):
    hits = retrieve(question, k)
    messages = build_prompt(question, hits)
    if client:
        text = client.chat.completions.create(model=MODEL, messages=messages, temperature=0).choices[0].message.content
    else:
        text = "(no API key: the model would answer from the context above)"
    return {"answer": text, "sources": [h["section"] for h in hits]}


print(answer(question))

# %% Questions that are NOT in the documents (should say "I don't know")
print(answer("Do you sell gift wrapping for birthdays?"))

# %% Why RAG instead of fine-tuning?
# RAG:         fresh data, cites sources, cheap to update, easy to delete data
# Fine-tuning: changes style/behavior, bad for adding facts

# %% Common RAG failures
# 1. Wrong chunk retrieved      -> better chunking, hybrid search, reranking
# 2. Right chunk, bad answer    -> better prompt, bigger model
# 3. Question not in documents  -> force "I don't know"
# 4. Stale data                 -> re-index on change
# 5. Prompt injection in docs   -> treat documents as data, never as instructions
