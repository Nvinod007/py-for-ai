# Models can only read so much, and search works best on small focused pieces.
# Chunking = cutting documents into pieces before embedding them.

import re
from pathlib import Path

DATA = Path("data") if Path("data").exists() else Path("../data")
text = (DATA / "05_company_faq.md").read_text()
print(len(text), "characters,", len(text.split()), "words")

# %% Strategy 1: fixed size with overlap
def chunk_fixed(text, size=300, overlap=50):
    chunks, start = [], 0
    while start < len(text):
        chunks.append(text[start : start + size])
        start += size - overlap
    return chunks


fixed = chunk_fixed(text)
print(len(fixed), "chunks")
print(repr(fixed[1][:80]), "...")                    # note it can cut a sentence in half

# %% Strategy 2: split on structure (headings, paragraphs)
def chunk_by_heading(markdown):
    parts = re.split(r"\n(?=## )", markdown)
    chunks = []
    for part in parts:
        part = part.strip()
        if part.startswith("## "):
            title, _, body = part.partition("\n")
            chunks.append({"title": title.removeprefix("## ").strip(), "text": body.strip()})
    return chunks


by_heading = chunk_by_heading(text)
print(len(by_heading), [c["title"] for c in by_heading])

# %% Strategy 3: sentence-aware chunks up to a size
def chunk_sentences(text, max_chars=250):
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    chunks, current = [], ""
    for sentence in sentences:
        if current and len(current) + len(sentence) > max_chars:
            chunks.append(current.strip())
            current = ""
        current += sentence + " "
    if current.strip():
        chunks.append(current.strip())
    return chunks


sent = chunk_sentences(by_heading[0]["text"] + " " + by_heading[1]["text"])
print(len(sent))
for c in sent:
    print("-", c[:90], "...")

# %% Always keep metadata: you need it to cite sources
records = []
for section in by_heading:
    for i, piece in enumerate(chunk_sentences(section["text"])):
        records.append(
            {"id": f"{section['title']}-{i}", "text": piece, "source": "05_company_faq.md", "section": section["title"]}
        )
print(len(records), records[0])

# %% How to pick chunk size
# Too small -> loses context ("It costs $4.99" - what costs?)
# Too big   -> mixes topics, wastes tokens, retrieval gets blurry
# Start with 200-500 words (or one section), overlap 10-20%, then test (folder 10 / 06 and folder 16).
# Add the section title into the chunk text so every piece knows what it is about.
with_title = [f"{r['section']}: {r['text']}" for r in records]
print(with_title[0])
