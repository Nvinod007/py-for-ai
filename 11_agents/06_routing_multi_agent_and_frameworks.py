# Bigger systems: route requests to specialists, then know the frameworks.

import re

try:
    import langgraph  # noqa: F401
    HAS_LANGGRAPH = True
except ImportError:
    HAS_LANGGRAPH = False

# %% Router: pick the right specialist for the request
def classify(request):
    text = request.lower()
    if re.search(r"refund|charge|invoice|payment", text):
        return "billing"
    if re.search(r"password|login|error|crash|bug", text):
        return "technical"
    return "general"


def billing_agent(request):
    return f"[billing] I will check your payment history for: {request}"


def technical_agent(request):
    return f"[technical] Let's troubleshoot: {request}"


def general_agent(request):
    return f"[general] Happy to help with: {request}"


SPECIALISTS = {"billing": billing_agent, "technical": technical_agent, "general": general_agent}


def handle(request):
    route = classify(request)
    return SPECIALISTS[route](request)


for r in ["I was charged twice", "App crashes on login", "What are your hours?"]:
    print(handle(r))

# %% Orchestrator + workers: split a task, run workers, merge results
def researcher(topic):
    return f"facts about {topic}"


def writer(facts):
    return f"Report based on: {facts}"


def orchestrate(topic):
    facts = researcher(topic)
    return writer(facts)


print(orchestrate("renewable energy"))

# %% A state machine is the core idea behind LangGraph-style frameworks
GRAPH = {
    "start": lambda state: ("collect", state),
    "collect": lambda state: ("draft", {**state, "facts": ["a", "b"]}),
    "draft": lambda state: ("review", {**state, "draft": "text with " + ",".join(state["facts"])}),
    "review": lambda state: ("end" if len(state["draft"]) > 10 else "draft", state),
}


def run_graph(state):
    node = "start"
    while node != "end":
        node, state = GRAPH[node](state)
        print("->", node)
    return state


print(run_graph({}))

# %% Frameworks (learn the ideas above first, then pick one)
FRAMEWORKS = {
    "LangGraph": "graphs/state machines for agents, good for complex flows and persistence",
    "OpenAI Agents SDK": "small, simple loop with tools, handoffs, guardrails",
    "Claude Agent SDK": "agent loop with tools and file/shell access",
    "LlamaIndex": "focused on RAG and data connectors",
    "CrewAI / AutoGen": "multi-agent role playing, can be heavy",
    "PydanticAI": "typed agents with validation",
}
for name, note in FRAMEWORKS.items():
    print(f"{name:18} {note}")
print("langgraph installed:", HAS_LANGGRAPH)

# %% Advice
# 1. A single agent with good tools beats a team of agents most of the time.
# 2. Use a workflow (fixed steps) when the path is known; an agent when it truly varies.
# 3. Measure with evals before and after adding complexity.
