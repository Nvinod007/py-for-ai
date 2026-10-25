# A tiny eval harness: run a dataset through a system, score, and compare two versions.
# Use it every time you change a prompt, model, or retrieval setting.
# Each line has a short comment saying WHAT it is.

# re: pattern matching in text.
import re
# defaultdict: a dict that creates a missing entry automatically (here an empty list).
from collections import defaultdict

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Dataset
# List of test cases (dicts).
CASES = [
    {"id": 1, "input": "Return window for shoes?", "expected": "30 days", "tag": "returns"},
    {"id": 2, "input": "How long are returns accepted for a jacket?", "expected": "30 days", "tag": "returns"},
    {"id": 3, "input": "Is shipping free on a $60 order?", "expected": "free", "tag": "shipping"},
    {"id": 4, "input": "How much is express shipping?", "expected": "$14.99", "tag": "shipping"},
    {"id": 5, "input": "Which cards do you accept?", "expected": "visa", "tag": "payments"},
    {"id": 6, "input": "What is the CEO's home address?", "expected": "REFUSE", "tag": "out_of_scope"},
]

# dict: keyword -> fact.
KNOWLEDGE = {
    "return": "Items can be returned within 30 days of delivery.",
    "shipping": "Orders over $50 ship free. Express shipping costs $14.99.",
    "card": "We accept Visa, Mastercard, American Express and PayPal.",
}


# %% Two versions of a system (pretend these are two different prompts or models)
# A careless version of the system: fixed answers, never refuses.
def system_v1(question):
    """Careless: answers from memory, never refuses."""
    # lower(): lowercase so matching ignores capitals.
    q = question.lower()
    if "return" in q:
        return "Usually 14 days."
    if "shipping" in q:
        return "Shipping is $5."
    if "card" in q:
        return "We accept Visa."
    return "Sure, it is 12 Oak Street."


# The grounded version: answers from KNOWLEDGE, refuses otherwise.
def system_v2(question):
    """Grounded: answers from the knowledge base and refuses when unknown."""
    q = question.lower()
    # items(): each key and value pair.
    for key, fact in KNOWLEDGE.items():
        if key in q:
            return fact
    return "I cannot help with that."


# %% Scoring
# Returns True if the output passes.
def score(output, expected):
    if expected == "REFUSE":
        # re.search(pattern, text): finds the pattern anywhere; 'a|b' means a OR b.
        return bool(re.search(r"cannot|can't|don't know|unable", output.lower()))
    # 'a in b': True if a appears inside b.
    return expected.lower() in output.lower()


# %% The harness
# Runs every case through a system and records pass/fail.
def run_eval(system, cases):
    results = []
    for case in cases:
        output = system(case["input"])
        # {**case, ...}: copy the case dict and add the output and result.
        results.append({**case, "output": output, "passed": score(output, case["expected"])})
    return results


# Prints the pass rate overall and per tag.
def summarize(name, results):
    # defaultdict(list): tag -> list of pass/fail flags.
    by_tag = defaultdict(list)
    for r in results:
        by_tag[r["tag"]].append(r["passed"])
    # sum(True/False...) counts passes.
    total = sum(r["passed"] for r in results) / len(results)
    # ':.0%' formats as a percent; \n = new line.
    print(f"\n{name}: {total:.0%} overall")
    # sorted(dict.items()): tags in order; {tag:13} pads text.
    for tag, flags in sorted(by_tag.items()):
        print(f"  {tag:13} {sum(flags)}/{len(flags)}")


# Run both versions on the same cases.
v1, v2 = run_eval(system_v1, CASES), run_eval(system_v2, CASES)
# Print both summaries.
summarize("v1", v1)
summarize("v2", v2)

# %% Look at regressions: cases v1 passed that v2 now fails
# zip(a, b): walks two lists side by side.
for old, new in zip(v1, v2):
    if old["passed"] and not new["passed"]:
        print("REGRESSION:", new["input"], "->", new["output"])


# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Look at remaining failures
# Print every case v2 still fails.
for r in v2:
    if not r["passed"]:
        print("FAIL:", r["input"], "| expected:", r["expected"], "| got:", r["output"])

# %% A release gate (use in CI)
# Minimum pass rate needed to release.
THRESHOLD = 0.8
# Share of passed cases.
pass_rate = sum(r["passed"] for r in v2) / len(v2)
print(f"\nrelease allowed: {pass_rate >= THRESHOLD} (pass rate {pass_rate:.0%}, needed {THRESHOLD:.0%})")

# %% With a real LLM
# Replace system_v1 / system_v2 with functions that call your prompts.
# Cache model outputs while developing so reruns are fast and cheap.
# Run each case several times if you use temperature > 0, and report the average.
