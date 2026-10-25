# A tiny eval harness: run a dataset through a system, score, and compare two versions.
# Use it every time you change a prompt, model, or retrieval setting.

import re
from collections import defaultdict

# %% Dataset
CASES = [
    {"id": 1, "input": "Return window for shoes?", "expected": "30 days", "tag": "returns"},
    {"id": 2, "input": "How long are returns accepted for a jacket?", "expected": "30 days", "tag": "returns"},
    {"id": 3, "input": "Is shipping free on a $60 order?", "expected": "free", "tag": "shipping"},
    {"id": 4, "input": "How much is express shipping?", "expected": "$14.99", "tag": "shipping"},
    {"id": 5, "input": "Which cards do you accept?", "expected": "visa", "tag": "payments"},
    {"id": 6, "input": "What is the CEO's home address?", "expected": "REFUSE", "tag": "out_of_scope"},
]

KNOWLEDGE = {
    "return": "Items can be returned within 30 days of delivery.",
    "shipping": "Orders over $50 ship free. Express shipping costs $14.99.",
    "card": "We accept Visa, Mastercard, American Express and PayPal.",
}


# %% Two versions of a system (pretend these are two different prompts or models)
def system_v1(question):
    """Careless: answers from memory, never refuses."""
    q = question.lower()
    if "return" in q:
        return "Usually 14 days."
    if "shipping" in q:
        return "Shipping is $5."
    if "card" in q:
        return "We accept Visa."
    return "Sure, it is 12 Oak Street."


def system_v2(question):
    """Grounded: answers from the knowledge base and refuses when unknown."""
    q = question.lower()
    for key, fact in KNOWLEDGE.items():
        if key in q:
            return fact
    return "I cannot help with that."


# %% Scoring
def score(output, expected):
    if expected == "REFUSE":
        return bool(re.search(r"cannot|can't|don't know|unable", output.lower()))
    return expected.lower() in output.lower()


# %% The harness
def run_eval(system, cases):
    results = []
    for case in cases:
        output = system(case["input"])
        results.append({**case, "output": output, "passed": score(output, case["expected"])})
    return results


def summarize(name, results):
    by_tag = defaultdict(list)
    for r in results:
        by_tag[r["tag"]].append(r["passed"])
    total = sum(r["passed"] for r in results) / len(results)
    print(f"\n{name}: {total:.0%} overall")
    for tag, flags in sorted(by_tag.items()):
        print(f"  {tag:13} {sum(flags)}/{len(flags)}")


v1, v2 = run_eval(system_v1, CASES), run_eval(system_v2, CASES)
summarize("v1", v1)
summarize("v2", v2)

# %% Look at regressions: cases v1 passed that v2 now fails
for old, new in zip(v1, v2):
    if old["passed"] and not new["passed"]:
        print("REGRESSION:", new["input"], "->", new["output"])

# %% Look at remaining failures
for r in v2:
    if not r["passed"]:
        print("FAIL:", r["input"], "| expected:", r["expected"], "| got:", r["output"])

# %% A release gate (use in CI)
THRESHOLD = 0.8
pass_rate = sum(r["passed"] for r in v2) / len(v2)
print(f"\nrelease allowed: {pass_rate >= THRESHOLD} (pass rate {pass_rate:.0%}, needed {THRESHOLD:.0%})")

# %% With a real LLM
# Replace system_v1 / system_v2 with functions that call your prompts.
# Cache model outputs while developing so reruns are fast and cheap.
# Run each case several times if you use temperature > 0, and report the average.
