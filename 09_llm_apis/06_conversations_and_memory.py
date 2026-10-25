# The API has NO memory. Every call you must resend the whole conversation.
# "Memory" is just you managing that list of messages.
# Each line has a short comment saying WHAT it is.

import json
import os

from openai import OpenAI

# os.environ.get(NAME): reads a setting from your terminal; gives None if it is not set.
API_KEY = os.environ.get("OPENAI_API_KEY")
# MODEL = the name of the AI model to use.
MODEL = "gpt-4o-mini"
# OpenAI(api_key=...): creates the object that talks to the API; None if there is no key so the file still runs.
client = OpenAI(api_key=API_KEY) if API_KEY else None


# llm(messages): asks the real AI if there is a key, otherwise returns a fake reply.
def llm(messages):
    if client:
        # create(model, messages): sends the conversation to the AI; .choices[0].message.content is the answer text.
        return client.chat.completions.create(model=MODEL, messages=messages).choices[0].message.content
    # List comprehension: pick the user messages; [-1] takes the last one.
    last_user = [m for m in messages if m["role"] == "user"][-1]["content"]
    return f"(fake reply to: {last_user})"

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% A chat is a growing list
# history: the list of all messages so far; the API remembers nothing, so we keep it.
history = [{"role": "system", "content": "You are a friendly tutor."}]


# chat(user_text): add your message, ask the AI, add its reply, return it.
def chat(user_text):
    # append: add an item to the end of the list.
    history.append({"role": "user", "content": user_text})
    reply = llm(history)
    history.append({"role": "assistant", "content": reply})
    return reply


print(chat("My name is Asha."))
print(chat("What is my name?"))
# len(): how many items.
print(len(history), "messages sent next time")

# %% The model forgets anything you do not send
print(llm([{"role": "user", "content": "What is my name?"}]))

# %% Windows have a size limit (context window), costs grow with every turn
# rough_tokens: guesses token count; sum() adds the text lengths, // 4 = about 4 characters per token.
def rough_tokens(messages):
    return sum(len(m["content"]) for m in messages) // 4


print("approx tokens in history:", rough_tokens(history))

# %% Strategy 1: keep only the last N messages (always keep the system prompt)
# sliding_window: keeps the system message plus only the last `keep` messages.
def sliding_window(messages, keep=6):
    # messages[:1] = first item; messages[1:] = everything after it.
    system, rest = messages[:1], messages[1:]
    # rest[-keep:] = the last `keep` items; + joins lists.
    return system + rest[-keep:]


# A fake long chat: i % 2 == 0 alternates user/assistant; range(20) makes 20 messages.
long_chat = [{"role": "system", "content": "tutor"}] + [
    {"role": "user" if i % 2 == 0 else "assistant", "content": f"message {i}"} for i in range(20)
]
print(len(sliding_window(long_chat, keep=6)))

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Strategy 2: summarize old messages into one
# summarize_old: asks the AI to shorten old messages into one summary and keeps recent ones.
def summarize_old(messages, keep=4):
    system, rest = messages[:1], messages[1:]
    if len(rest) <= keep:
        return messages
    # rest[:-keep] = all but the last `keep`; rest[-keep:] = the last `keep`.
    old, recent = rest[:-keep], rest[-keep:]
    # "\n".join(...): glue the old messages into one text, one per line.
    summary = llm([{"role": "user", "content": "Summarize this chat in 2 sentences:\n" + "\n".join(m["content"] for m in old)}])
    return system + [{"role": "system", "content": f"Summary of earlier chat: {summary}"}] + recent


print(len(summarize_old(long_chat)))

# %% Strategy 3: store facts outside the chat (long-term memory)
# facts: a dictionary (key -> value) kept outside the chat as long-term memory.
facts = {}


# remember: store one fact.
def remember(key, value):
    facts[key] = value


# build_messages: puts the stored facts into the system prompt.
def build_messages(user_text):
    # facts.items(): gives each key and value; f"- {k}: {v}" makes a bullet line.
    memory = "\n".join(f"- {k}: {v}" for k, v in facts.items())
    return [
        {"role": "system", "content": f"You are a tutor.\nKnown about the user:\n{memory}"},
        {"role": "user", "content": user_text},
    ]


remember("name", "Asha")
remember("goal", "become a forward deployed engineer")
print(build_messages("What should I study next?")[0]["content"])

# %% Where long-term memory really lives
# A database table, or a vector store (folder 10) that you search for relevant memories.

# %% Save and load a conversation
# json.dumps: turn the list into JSON text (to save in a file).
saved = json.dumps(history)
# json.loads: turn JSON text back into a Python list.
print(len(json.loads(saved)))
