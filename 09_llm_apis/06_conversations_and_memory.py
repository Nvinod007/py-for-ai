# The API has NO memory. Every call you must resend the whole conversation.
# "Memory" is just you managing that list of messages.

import json
import os

from openai import OpenAI

API_KEY = os.environ.get("OPENAI_API_KEY")
MODEL = "gpt-4o-mini"
client = OpenAI(api_key=API_KEY) if API_KEY else None


def llm(messages):
    if client:
        return client.chat.completions.create(model=MODEL, messages=messages).choices[0].message.content
    last_user = [m for m in messages if m["role"] == "user"][-1]["content"]
    return f"(fake reply to: {last_user})"


# %% A chat is a growing list
history = [{"role": "system", "content": "You are a friendly tutor."}]


def chat(user_text):
    history.append({"role": "user", "content": user_text})
    reply = llm(history)
    history.append({"role": "assistant", "content": reply})
    return reply


print(chat("My name is Asha."))
print(chat("What is my name?"))
print(len(history), "messages sent next time")

# %% The model forgets anything you do not send
print(llm([{"role": "user", "content": "What is my name?"}]))

# %% Windows have a size limit (context window), costs grow with every turn
def rough_tokens(messages):
    return sum(len(m["content"]) for m in messages) // 4


print("approx tokens in history:", rough_tokens(history))

# %% Strategy 1: keep only the last N messages (always keep the system prompt)
def sliding_window(messages, keep=6):
    system, rest = messages[:1], messages[1:]
    return system + rest[-keep:]


long_chat = [{"role": "system", "content": "tutor"}] + [
    {"role": "user" if i % 2 == 0 else "assistant", "content": f"message {i}"} for i in range(20)
]
print(len(sliding_window(long_chat, keep=6)))

# %% Strategy 2: summarize old messages into one
def summarize_old(messages, keep=4):
    system, rest = messages[:1], messages[1:]
    if len(rest) <= keep:
        return messages
    old, recent = rest[:-keep], rest[-keep:]
    summary = llm([{"role": "user", "content": "Summarize this chat in 2 sentences:\n" + "\n".join(m["content"] for m in old)}])
    return system + [{"role": "system", "content": f"Summary of earlier chat: {summary}"}] + recent


print(len(summarize_old(long_chat)))

# %% Strategy 3: store facts outside the chat (long-term memory)
facts = {}


def remember(key, value):
    facts[key] = value


def build_messages(user_text):
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
saved = json.dumps(history)
print(len(json.loads(saved)))
