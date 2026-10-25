# Streaming: show words as they are generated, so users do not stare at a blank screen.
# Each line has a short comment saying WHAT it is.

import os
import time

from openai import OpenAI

# os.environ.get(NAME): reads a setting from your terminal; gives None if it is not set.
API_KEY = os.environ.get("OPENAI_API_KEY")
# MODEL = the name of the AI model to use.
MODEL = "gpt-4o-mini"
# OpenAI(api_key=...): creates the object that talks to the API; None if there is no key so the file still runs.
client = OpenAI(api_key=API_KEY) if API_KEY else None

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% A generator that behaves like a stream
# fake_stream: a generator = a function that hands out pieces one at a time.
def fake_stream(text):
    # split(): cut the text into a list of words.
    for word in text.split():
        # time.sleep(seconds): pause, to mimic waiting for the AI.
        time.sleep(0.05)
        # yield: hand out one piece now and continue later (unlike return, which ends).
        yield word + " "

# %% Consume a stream
# for piece in stream: takes pieces as they arrive.
answer = ""
for piece in fake_stream("Streaming sends small pieces as soon as they are ready."):
    # end="": do not add a new line; flush=True: show it on screen right away.
    print(piece, end="", flush=True)
    answer += piece
# strip(): remove spaces at both ends.
print("\nfull text:", answer.strip())

# %% Real streaming
if client:
    # create(...): sends the conversation to the AI; stream=True = get the answer in small pieces instead of all at once.
    stream = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": "Explain pandas in two sentences."}],
        stream=True,
    )
    full = ""
    for chunk in stream:
        # chunk.choices[0].delta.content: the new few words in this piece (None if empty).
        delta = chunk.choices[0].delta.content if chunk.choices else None
        if delta:
            print(delta, end="", flush=True)
            full += delta
    print()

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Measure what users feel
# measure: times how long a stream takes; perf_counter() is a precise clock.
def measure(stream):
    start = time.perf_counter()
    first = None
    count = 0
    # _ = a throwaway name, we only count the pieces.
    for _ in stream:
        count += 1
        if first is None:
            first = time.perf_counter() - start
    total = time.perf_counter() - start
    return first, total, count


# f"{x:.2f}": show a number with 2 decimals.
first, total, count = measure(fake_stream("one two three four five six seven eight"))
print(f"time to first token {first:.2f}s, total {total:.2f}s, pieces {count}")

# %% Web apps send streams with Server-Sent Events (see folder 12, 06_llm_endpoint)
# SSE (Server-Sent Events): a web format where each piece is sent as a 'data: ...' line followed by a blank line.
def sse(chunks):
    for chunk in chunks:
        yield f"data: {chunk}\n\n"
    yield "data: [DONE]\n\n"


# "".join(list): glue the pieces together into one text.
print("".join(sse(["Hel", "lo"])))

# %% Tips
# - Stream for chat UIs. Do not stream when you need to parse complete JSON.
# - Handle cancellation: stop reading when the user leaves.
# - Tool calls also stream in pieces, collect them before running.
