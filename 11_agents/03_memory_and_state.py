# Three kinds of memory an agent can have.

import json
import tempfile
from dataclasses import dataclass, field
from pathlib import Path

# %% 1. Short-term: the message list for this conversation
messages = [
    {"role": "user", "content": "I need a flight to Paris next week."},
    {"role": "assistant", "content": "Which day do you want to leave?"},
    {"role": "user", "content": "Tuesday."},
]
print(len(messages), "messages in short-term memory")

# %% 2. Working state: structured facts for the current task (better than re-reading chat)
@dataclass
class TripState:
    destination: str | None = None
    day: str | None = None
    budget: float | None = None
    steps_done: list[str] = field(default_factory=list)

    def missing(self):
        return [name for name in ("destination", "day", "budget") if getattr(self, name) is None]


state = TripState(destination="Paris", day="Tuesday")
print(state.missing())
state.budget = 800
state.steps_done.append("collected requirements")
print(state, state.missing())

# %% 3. Long-term: facts that survive between conversations
class MemoryStore:
    def __init__(self, path):
        self.path = Path(path)
        self.facts = json.loads(self.path.read_text()) if self.path.exists() else []

    def remember(self, text, tags=()):
        self.facts.append({"text": text, "tags": list(tags)})
        self.path.write_text(json.dumps(self.facts, indent=2))

    def recall(self, query, limit=3):
        words = set(query.lower().split())
        scored = [(len(words & set(f["text"].lower().split())), f["text"]) for f in self.facts]
        return [text for score, text in sorted(scored, reverse=True)[:limit] if score > 0]


store = MemoryStore(Path(tempfile.mkdtemp()) / "memory.json")
store.remember("User prefers window seats", tags=["travel"])
store.remember("User is vegetarian", tags=["food"])
store.remember("User lives in Pune", tags=["profile"])
print(store.recall("book a window seat please"))
print(store.recall("restaurant for a vegetarian dinner"))

# %% Put recalled memory into the prompt
def build_system_prompt(user_message):
    memories = store.recall(user_message)
    memory_text = "\n".join(f"- {m}" for m in memories) or "- (nothing relevant)"
    return f"You are a travel assistant.\nWhat you know about this user:\n{memory_text}"


print(build_system_prompt("Find me a seat on the flight"))

# %% Upgrade: use embeddings (folder 10) instead of word overlap, store in a vector DB.

# %% Memory pitfalls
# - Remembering wrong or old facts (add timestamps, allow the user to correct or delete).
# - Storing private data without consent (be explicit about what you store).
# - Stuffing everything into the prompt (retrieve only what is relevant).
