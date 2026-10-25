# Three kinds of memory an agent can have.
# Each line has a short comment saying WHAT it is.

# json: read/write JSON text.
import json
# tempfile: makes temporary files/folders that are cleaned up by the OS.
import tempfile
# dataclass: auto-writes __init__ and printing for a class that just holds data; field(...) customizes one field.
from dataclasses import dataclass, field
# Path: an object for file paths with handy read/write methods.
from pathlib import Path

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% 1. Short-term: the message list for this conversation
# A list of dicts: each message has a 'role' (who spoke) and 'content' (text).
messages = [
    {"role": "user", "content": "I need a flight to Paris next week."},
    {"role": "assistant", "content": "Which day do you want to leave?"},
    {"role": "user", "content": "Tuesday."},
]
# len(list): number of items.
print(len(messages), "messages in short-term memory")

# %% 2. Working state: structured facts for the current task (better than re-reading chat)
# @dataclass: decorator turning the class below into a simple data holder.
@dataclass
# class: a blueprint for objects. 'str | None' means text or nothing yet.
class TripState:
    destination: str | None = None
    day: str | None = None
    budget: float | None = None
    # field(default_factory=list): gives each object its OWN empty list (never share a mutable default).
    steps_done: list[str] = field(default_factory=list)

    # Method (function inside a class): lists the facts still unset. getattr(obj, 'name') reads an attribute by its name text.
    def missing(self):
        return [name for name in ("destination", "day", "budget") if getattr(self, name) is None]


# Create an object; unspecified fields use their defaults.
state = TripState(destination="Paris", day="Tuesday")
print(state.missing())
state.budget = 800
# append: add an item to the list.
state.steps_done.append("collected requirements")
print(state, state.missing())

# %% 3. Long-term: facts that survive between conversations
# A small class that saves facts to a JSON file so they survive restarts.
class MemoryStore:
    # __init__: runs automatically when the object is created; self is the object itself.
    def __init__(self, path):
        self.path = Path(path)
        # path.exists() checks the file exists; read_text() reads it; json.loads turns the text into a list.
        self.facts = json.loads(self.path.read_text()) if self.path.exists() else []

    # Saves one fact; list(tags) copies tags into a list.
    def remember(self, text, tags=()):
        self.facts.append({"text": text, "tags": list(tags)})
        # write_text(text) saves text to the file; json.dumps(..., indent=2) makes pretty JSON.
        self.path.write_text(json.dumps(self.facts, indent=2))

    # Finds stored facts that share words with the query; limit = max results.
    def recall(self, query, limit=3):
        # set: unique items; .lower().split() makes lowercase words.
        words = set(query.lower().split())
        # 'words & set(...)' = words in common; len() counts them, so score = overlap.
        scored = [(len(words & set(f["text"].lower().split())), f["text"]) for f in self.facts]
        # sorted(..., reverse=True): biggest score first; [:limit] keeps the top few; score > 0 drops non-matches.
        return [text for score, text in sorted(scored, reverse=True)[:limit] if score > 0]


# tempfile.mkdtemp(): makes a temp folder; Path / 'x' joins path parts.
store = MemoryStore(Path(tempfile.mkdtemp()) / "memory.json")
store.remember("User prefers window seats", tags=["travel"])
store.remember("User is vegetarian", tags=["food"])
store.remember("User lives in Pune", tags=["profile"])
print(store.recall("book a window seat please"))
print(store.recall("restaurant for a vegetarian dinner"))

# %% Put recalled memory into the prompt
# Builds the instruction text sent to the model, including recalled memories.
def build_system_prompt(user_message):
    memories = store.recall(user_message)
    # '\n'.join(list): joins items into lines; 'or' gives a fallback if the list is empty.
    memory_text = "\n".join(f"- {m}" for m in memories) or "- (nothing relevant)"
    return f"You are a travel assistant.\nWhat you know about this user:\n{memory_text}"


print(build_system_prompt("Find me a seat on the flight"))


# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Upgrade: use embeddings (folder 10) instead of word overlap, store in a vector DB.

# %% Memory pitfalls
# - Remembering wrong or old facts (add timestamps, allow the user to correct or delete).
# - Storing private data without consent (be explicit about what you store).
# - Stuffing everything into the prompt (retrieve only what is relevant).
