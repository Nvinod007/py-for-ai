# Bigger systems: route requests to specialists, then know the frameworks.
# Each line has a short comment saying WHAT it is.

# re: pattern matching in text.
import re

# try/except ImportError: use langgraph if installed, otherwise carry on.
try:
    # Tries to import the optional langgraph package; '# noqa' tells linters to ignore it.
    import langgraph  # noqa: F401
    HAS_LANGGRAPH = True
except ImportError:
    HAS_LANGGRAPH = False

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Router: pick the right specialist for the request
# Router: picks a category from keywords. .lower() makes lowercase; 'a|b' in a pattern means a OR b; re.search finds it anywhere.
def classify(request):
    text = request.lower()
    if re.search(r"refund|charge|invoice|payment", text):
        return "billing"
    if re.search(r"password|login|error|crash|bug", text):
        return "technical"
    return "general"


# A specialist 'agent': here just a function that returns a text reply.
def billing_agent(request):
    return f"[billing] I will check your payment history for: {request}"


def technical_agent(request):
    return f"[technical] Let's troubleshoot: {request}"


def general_agent(request):
    return f"[general] Happy to help with: {request}"


# dict: category name -> function, so we can pick one by name.
SPECIALISTS = {"billing": billing_agent, "technical": technical_agent, "general": general_agent}


# Route first, then call the matching specialist.
def handle(request):
    route = classify(request)
    return SPECIALISTS[route](request)


# for loop: runs the code once per request in the list.
for r in ["I was charged twice", "App crashes on login", "What are your hours?"]:
    print(handle(r))

# %% Orchestrator + workers: split a task, run workers, merge results
# Worker 1: pretends to gather facts.
def researcher(topic):
    return f"facts about {topic}"


def writer(facts):
    return f"Report based on: {facts}"


# Orchestrator: calls workers in order and passes results along.
def orchestrate(topic):
    facts = researcher(topic)
    return writer(facts)


print(orchestrate("renewable energy"))


# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% A state machine is the core idea behind LangGraph-style frameworks
# dict: node name -> function that returns (next node name, updated state).
GRAPH = {
    "start": lambda state: ("collect", state),
    "collect": lambda state: ("draft", {**state, "facts": ["a", "b"]}),
    "draft": lambda state: ("review", {**state, "draft": "text with " + ",".join(state["facts"])}),
    "review": lambda state: ("end" if len(state["draft"]) > 10 else "draft", state),
}


# Keeps running nodes until it reaches 'end'; state is a dict passed along.
def run_graph(state):
    node = "start"
    while node != "end":
        # Look up the node's function, call it, get the next node and new state.
        node, state = GRAPH[node](state)
        print("->", node)
    return state


print(run_graph({}))

# %% Frameworks (learn the ideas above first, then pick one)
# dict: framework name -> one-line description.
FRAMEWORKS = {
    "LangGraph": "graphs/state machines for agents, good for complex flows and persistence",
    "OpenAI Agents SDK": "small, simple loop with tools, handoffs, guardrails",
    "Claude Agent SDK": "agent loop with tools and file/shell access",
    "LlamaIndex": "focused on RAG and data connectors",
    "CrewAI / AutoGen": "multi-agent role playing, can be heavy",
    "PydanticAI": "typed agents with validation",
}
for name, note in FRAMEWORKS.items():
    # {name:18} pads the text to 18 characters so columns line up.
    print(f"{name:18} {note}")
print("langgraph installed:", HAS_LANGGRAPH)

# %% Advice
# 1. A single agent with good tools beats a team of agents most of the time.
# 2. Use a workflow (fixed steps) when the path is known; an agent when it truly varies.
# 3. Measure with evals before and after adding complexity.
