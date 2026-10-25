# RAG = Retrieval Augmented Generation.
#   1. Retrieve the most relevant chunks for the question.
#   2. Put them in the prompt.
#   3. Ask the model to answer ONLY from them (and cite).
# This is how you make an LLM use your documents without training it.
# Each line has a short comment saying WHAT it is.

import os
import re
import zlib
from pathlib import Path

import numpy as np
from openai import OpenAI

# Path(...).exists(): True if the folder exists; picks whichever data folder is found.
DATA = Path("data") if Path("data").exists() else Path("../data")
# os.environ.get(NAME): reads a setting from the terminal; None if missing.
API_KEY = os.environ.get("OPENAI_API_KEY")
# OpenAI(api_key=...): creates the API client; None if no key so the file still runs.
client = OpenAI(api_key=API_KEY) if API_KEY else None
# MODEL = the name of the AI model to use.
MODEL = "gpt-4o-mini"
# DIM: how many numbers each vector has.
DIM = 512
# STOP: 'stop words' = very common words we ignore because they carry little meaning.
STOP = {"the", "a", "an", "of", "to", "and", "is", "are", "in", "on", "for", "or", "do", "i", "my", "can", "you", "it", "we", "how", "what", "does"}


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

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Step 1: index the documents
# load_sections: reads the FAQ and returns one {section, text} per '## ' heading.
def load_sections():
    # read_text(): read the file as one string.
    text = (DATA / "05_company_faq.md").read_text()
    sections = []
    # re.split: cut before each '## ' heading.
    for part in re.split(r"\n(?=## )", text):
        if part.startswith("## "):
            # partition("\n"): split at the first newline into title and body; removeprefix removes '## '.
            title, _, body = part.partition("\n")
            sections.append({"section": title.removeprefix("## ").strip(), "text": body.strip()})
    return sections


# matrix: one row (vector) per chunk; the title is included so it helps matching.
chunks = load_sections()
matrix = np.array([embed(f"{c['section']} {c['text']}") for c in chunks])
print(len(chunks), "chunks indexed")

# %% Step 2: retrieve
# retrieve(question, k): finds the k most similar chunks.
def retrieve(question, k=2):
    # matrix @ vector: similarity of the question to every chunk at once.
    scores = matrix @ embed(question)
    # argsort: positions sorted by score (small to big); [::-1] reverses; [:k] keeps k.
    top = np.argsort(scores)[::-1][:k]
    # {**chunk, "score": x}: copy the chunk's fields and add a score.
    return [{**chunks[i], "score": float(scores[i])} for i in top]


# Show each hit's score and section.
for hit in retrieve("Can I return shoes after three weeks?"):
    print(f"{hit['score']:.2f} {hit['section']}")

# %% Step 3: build the prompt
# build_prompt: puts the retrieved chunks and the question into chat messages.
def build_prompt(question, hits):
    # enumerate(hits): numbers each chunk so the AI can cite [1], [2]; "\n\n".join(...) glues them with blank lines.
    context = "\n\n".join(f"[{i + 1}] ({h['section']}) {h['text']}" for i, h in enumerate(hits))
    return [
        {
            # role system: the rules for the AI (answer only from context, cite, admit when unknown).
            "role": "system",
            "content": (
                "You answer customer questions using ONLY the numbered context.\n"
                "Cite sources like [1]. If the context does not contain the answer, say "
                "'I don't know based on the documents.'"
            ),
        },
        # role user: the context and the question.
        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {question}"},
    ]


# Retrieve chunks, then build the prompt messages; [400] shows the first 400 characters.
question = "How long does standard shipping take and what does it cost?"
messages = build_prompt(question, retrieve(question))
print(messages[1]["content"][:400])

# %% Step 4: generate
# answer(question, k): the full RAG flow: retrieve, build prompt, ask the AI.
def answer(question, k=2):
    hits = retrieve(question, k)
    messages = build_prompt(question, hits)
    if client:
        # create(...): sends messages to the AI; temperature=0 = most predictable answer; choices[0].message.content = the answer text.
        text = client.chat.completions.create(model=MODEL, messages=messages, temperature=0).choices[0].message.content
    else:
        text = "(no API key: the model would answer from the context above)"
    # Return the answer and the names of the sections used (sources).
    return {"answer": text, "sources": [h["section"] for h in hits]}


print(answer(question))

# %% Questions that are NOT in the documents (should say "I don't know")
print(answer("Do you sell gift wrapping for birthdays?"))

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Why RAG instead of fine-tuning?
# RAG:         fresh data, cites sources, cheap to update, easy to delete data
# Fine-tuning: changes style/behavior, bad for adding facts

# %% Common RAG failures
# 1. Wrong chunk retrieved      -> better chunking, hybrid search, reranking
# 2. Right chunk, bad answer    -> better prompt, bigger model
# 3. Question not in documents  -> force "I don't know"
# 4. Stale data                 -> re-index on change
# 5. Prompt injection in docs   -> treat documents as data, never as instructions
