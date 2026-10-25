# Models can only read so much, and search works best on small focused pieces.
# Chunking = cutting documents into pieces before embedding them.
# Each line has a short comment saying WHAT it is.

import re
from pathlib import Path

# Path(...).exists(): True if the folder exists; picks whichever data folder is found.
DATA = Path("data") if Path("data").exists() else Path("../data")
# read_text(): read the whole file as one string.
text = (DATA / "05_company_faq.md").read_text()
# len(text): number of characters; split(): cut into words so len counts words.
print(len(text), "characters,", len(text.split()), "words")

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Strategy 1: fixed size with overlap
# chunk_fixed: cuts text into pieces of `size` characters; overlap = how many characters repeat between neighbours so ideas aren't lost at the edge.
def chunk_fixed(text, size=300, overlap=50):
    # chunks = list of pieces; start = where the next piece begins.
    chunks, start = [], 0
    while start < len(text):
        # text[a:b]: slice of characters from a up to (not including) b; append adds to the list.
        chunks.append(text[start : start + size])
        # Move forward by size minus overlap.
        start += size - overlap
    return chunks


fixed = chunk_fixed(text)
print(len(fixed), "chunks")
# repr(): shows the text with quotes and \n visible; [:80] = first 80 characters.
print(repr(fixed[1][:80]), "...")                    # note it can cut a sentence in half

# %% Strategy 2: split on structure (headings, paragraphs)
# chunk_by_heading: one chunk per '## ' section of the markdown file.
def chunk_by_heading(markdown):
    # re.split(pattern, text): cut text at each match; (?=## ) = cut before a line starting '## ' but keep it.
    parts = re.split(r"\n(?=## )", markdown)
    chunks = []
    for part in parts:
        # strip(): remove spaces/newlines at both ends.
        part = part.strip()
        # startswith(): True if the text begins with that.
        if part.startswith("## "):
            # partition("\n"): split at the first newline into (title, separator, body); _ ignores the separator.
            title, _, body = part.partition("\n")
            # removeprefix('## '): cut that start off the text.
            chunks.append({"title": title.removeprefix("## ").strip(), "text": body.strip()})
    return chunks


by_heading = chunk_by_heading(text)
# List comprehension: collect every chunk's title.
print(len(by_heading), [c["title"] for c in by_heading])

# %% Strategy 3: sentence-aware chunks up to a size
# chunk_sentences: groups whole sentences until a chunk reaches max_chars.
def chunk_sentences(text, max_chars=250):
    # (?<=[.!?])\s+ = split at whitespace that follows . ! or ?.
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    # chunks = finished pieces; current = the piece being built.
    chunks, current = [], ""
    for sentence in sentences:
        # If adding this sentence would be too long, save the current piece and start a new one.
        if current and len(current) + len(sentence) > max_chars:
            chunks.append(current.strip())
            current = ""
        # Add the sentence (plus a space) to the current piece.
        current += sentence + " "
    # Save the last piece if it has any text.
    if current.strip():
        chunks.append(current.strip())
    return chunks


# Chunk the first two sections together.
sent = chunk_sentences(by_heading[0]["text"] + " " + by_heading[1]["text"])
print(len(sent))
for c in sent:
    print("-", c[:90], "...")

# %% Always keep metadata: you need it to cite sources
# records: list of dictionaries, each chunk with its metadata (id, source file, section).
records = []
for section in by_heading:
    # enumerate(list): gives a counter i and each item.
    for i, piece in enumerate(chunk_sentences(section["text"])):
        records.append(
            # f"...{x}...": text with values filled in.
            {"id": f"{section['title']}-{i}", "text": piece, "source": "05_company_faq.md", "section": section["title"]}
        )
print(len(records), records[0])

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% How to pick chunk size
# Too small -> loses context ("It costs $4.99" - what costs?)
# Too big   -> mixes topics, wastes tokens, retrieval gets blurry
# Start with 200-500 words (or one section), overlap 10-20%, then test (folder 10 / 06 and folder 16).
# Add the section title into the chunk text so every piece knows what it is about.
# List comprehension: put the section title in front of each chunk text.
with_title = [f"{r['section']}: {r['text']}" for r in records]
print(with_title[0])
