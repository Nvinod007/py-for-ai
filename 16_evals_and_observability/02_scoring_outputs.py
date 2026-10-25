# Code-based scorers: cheap, fast, and reliable where they apply.

import json
import re
from collections import Counter

from pydantic import BaseModel, ValidationError


# %% Exact and normalized match
def normalize(text):
    return re.sub(r"[^a-z0-9 ]", "", text.lower()).strip()


def exact_match(output, expected):
    return normalize(output) == normalize(expected)


print(exact_match("Paris.", "paris"), exact_match("It is Paris", "paris"))


# %% Contains (more forgiving)
def contains(output, expected):
    return normalize(expected) in normalize(output)


print(contains("The capital is Paris, France.", "paris"))


# %% Token overlap F1 (partial credit for text answers)
def token_f1(output, expected):
    a, b = normalize(output).split(), normalize(expected).split()
    common = Counter(a) & Counter(b)
    same = sum(common.values())
    if same == 0:
        return 0.0
    precision, recall = same / len(a), same / len(b)
    return 2 * precision * recall / (precision + recall)


print(round(token_f1("returns are allowed within 30 days", "30 days"), 2))
print(round(token_f1("no idea", "30 days"), 2))


# %% Numbers with tolerance
def number_close(output, expected, tolerance=0.01):
    found = re.findall(r"-?\d+(?:\.\d+)?", output.replace(",", ""))
    return bool(found) and abs(float(found[-1]) - expected) <= tolerance * abs(expected)


print(number_close("The total is $1,200.50", 1200), number_close("about 900", 1200))


# %% Valid JSON that matches a schema
class Answer(BaseModel):
    category: str
    urgency: int


def valid_schema(output):
    try:
        Answer.model_validate(json.loads(output))
        return True
    except (json.JSONDecodeError, ValidationError):
        return False


print(valid_schema('{"category": "billing", "urgency": 3}'), valid_schema('{"category": "billing"}'), valid_schema("sorry"))


# %% Rule checks: citations, length, banned content, refusals
def has_citation(output):
    return bool(re.search(r"\[\d+\]", output))


def within_length(output, max_words=60):
    return len(output.split()) <= max_words


def refused(output):
    return bool(re.search(r"\b(can't|cannot|unable|don't know|not able)\b", output.lower()))


def leaks_secret(output):
    return bool(re.search(r"sk-[A-Za-z0-9]{10,}|system prompt:", output, re.IGNORECASE))


print(has_citation("Returns take 30 days [1]."), within_length("short"), refused("I cannot help with that"), leaks_secret("ok"))

# %% Classification metrics when the task is a label
y_true = ["billing", "tech", "billing", "shipping", "tech", "billing"]
y_pred = ["billing", "tech", "shipping", "shipping", "billing", "billing"]
accuracy = sum(t == p for t, p in zip(y_true, y_pred)) / len(y_true)
print("accuracy", round(accuracy, 2))
for label in sorted(set(y_true)):
    tp = sum(t == p == label for t, p in zip(y_true, y_pred))
    fp = sum(p == label and t != label for t, p in zip(y_true, y_pred))
    fn = sum(t == label and p != label for t, p in zip(y_true, y_pred))
    print(f"{label:9} precision={tp / (tp + fp) if tp + fp else 0:.2f} recall={tp / (tp + fn) if tp + fn else 0:.2f}")

# %% Choose the scorer to match the task
# Fact lookup       -> contains / exact
# Extraction        -> schema + field-by-field equality
# Classification    -> accuracy, precision, recall per class
# Summaries, chat   -> rules + LLM judge + human sample
# RAG               -> retrieval hit rate (folder 10) + faithfulness + refusal when unknown
