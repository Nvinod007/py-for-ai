# Code-based scorers: cheap, fast, and reliable where they apply.
# Each line has a short comment saying WHAT it is.

# json: convert JSON text to dicts/lists.
import json
# re: regular expressions, a mini-language for matching text patterns.
import re
# Counter: counts how often each item appears.
from collections import Counter

# BaseModel: defines a data shape that is checked; ValidationError: raised when data doesn't fit.
from pydantic import BaseModel, ValidationError


# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Exact and normalized match
# re.sub(pattern, '', text): deletes everything except a-z, 0-9 and space; lower() = lowercase; strip() = trim spaces.
def normalize(text):
    return re.sub(r"[^a-z0-9 ]", "", text.lower()).strip()


# True only if both normalized texts are identical.
def exact_match(output, expected):
    return normalize(output) == normalize(expected)


# Punctuation and capitals are ignored, but extra words still fail.
print(exact_match("Paris.", "paris"), exact_match("It is Paris", "paris"))


# %% Contains (more forgiving)
# 'a in b': True if text a appears inside b.
def contains(output, expected):
    return normalize(expected) in normalize(output)


print(contains("The capital is Paris, France.", "paris"))


# %% Token overlap F1 (partial credit for text answers)
# F1 = score from 0 to 1 for word overlap; gives partial credit.
def token_f1(output, expected):
    # split(): breaks text into a list of words.
    a, b = normalize(output).split(), normalize(expected).split()
    # Counter(a) & Counter(b): words found in both, with counts.
    common = Counter(a) & Counter(b)
    # sum(common.values()): how many words overlap.
    same = sum(common.values())
    if same == 0:
        return 0.0
    # precision = overlap share of our answer; recall = overlap share of the expected; F1 = their balance.
    precision, recall = same / len(a), same / len(b)
    return 2 * precision * recall / (precision + recall)


# round(x, 2): 2 decimals.
print(round(token_f1("returns are allowed within 30 days", "30 days"), 2))
print(round(token_f1("no idea", "30 days"), 2))


# %% Numbers with tolerance
# Checks the last number in the text is close to the expected one (tolerance = allowed relative error).
def number_close(output, expected, tolerance=0.01):
    # re.findall(pattern, text): all matches as a list; replace(',', '') removes thousands commas.
    found = re.findall(r"-?\d+(?:\.\d+)?", output.replace(",", ""))
    # bool(): True if the list isn't empty; abs() = size ignoring the sign.
    return bool(found) and abs(float(found[-1]) - expected) <= tolerance * abs(expected)


# Close enough, then too far.
print(number_close("The total is $1,200.50", 1200), number_close("about 900", 1200))


# %% Valid JSON that matches a schema
# BaseModel: describes the JSON shape we expect (fields and types).
class Answer(BaseModel):
    category: str
    urgency: int


# True if the text is valid JSON that fits the Answer shape.
def valid_schema(output):
    # try/except: catch errors instead of crashing.
    try:
        # json.loads(text): JSON text -> dict; model_validate(dict): check the dict fits the model.
        Answer.model_validate(json.loads(output))
        return True
    # Either invalid JSON or wrong shape counts as failure.
    except (json.JSONDecodeError, ValidationError):
        return False


# Good JSON, missing field, not JSON at all.
print(valid_schema('{"category": "billing", "urgency": 3}'), valid_schema('{"category": "billing"}'), valid_schema("sorry"))


# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Rule checks: citations, length, banned content, refusals
# re.search(r'\[\d+\]', text): looks for a marker like [1].
def has_citation(output):
    return bool(re.search(r"\[\d+\]", output))


# True if the word count is at most max_words.
def within_length(output, max_words=60):
    return len(output.split()) <= max_words


# \b marks word edges; looks for phrases like 'cannot' or 'unable'.
def refused(output):
    return bool(re.search(r"\b(can't|cannot|unable|don't know|not able)\b", output.lower()))


# 'a|b' means a OR b; re.IGNORECASE ignores capitals; spots API keys starting with sk-.
def leaks_secret(output):
    return bool(re.search(r"sk-[A-Za-z0-9]{10,}|system prompt:", output, re.IGNORECASE))


# Try the four rule checks.
print(has_citation("Returns take 30 days [1]."), within_length("short"), refused("I cannot help with that"), leaks_secret("ok"))

# %% Classification metrics when the task is a label
# True labels.
y_true = ["billing", "tech", "billing", "shipping", "tech", "billing"]
# The model's predicted labels.
y_pred = ["billing", "tech", "shipping", "shipping", "billing", "billing"]
# zip(a, b): pairs items together; sum(True/False...) counts the matches.
accuracy = sum(t == p for t, p in zip(y_true, y_pred)) / len(y_true)
print("accuracy", round(accuracy, 2))
# sorted(set(...)): each unique label in order.
for label in sorted(set(y_true)):
    # tp (true positives): predicted this label and it was right.
    tp = sum(t == p == label for t, p in zip(y_true, y_pred))
    # fp (false positives): predicted this label wrongly.
    fp = sum(p == label and t != label for t, p in zip(y_true, y_pred))
    # fn (false negatives): missed this label.
    fn = sum(t == label and p != label for t, p in zip(y_true, y_pred))
    # precision = tp/(tp+fp); recall = tp/(tp+fn); 'x if cond else 0' avoids dividing by zero.
    print(f"{label:9} precision={tp / (tp + fp) if tp + fp else 0:.2f} recall={tp / (tp + fn) if tp + fn else 0:.2f}")

# %% Choose the scorer to match the task
# Fact lookup       -> contains / exact
# Extraction        -> schema + field-by-field equality
# Classification    -> accuracy, precision, recall per class
# Summaries, chat   -> rules + LLM judge + human sample
# RAG               -> retrieval hit rate (folder 10) + faithfulness + refusal when unknown
