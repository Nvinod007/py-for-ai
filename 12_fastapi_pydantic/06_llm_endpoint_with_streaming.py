# An AI endpoint: validated input, an LLM call, and streamed output.
# Without OPENAI_API_KEY it uses a fake model, with a key it calls the real one.
# Run for real:  uv run uvicorn 06_llm_endpoint_with_streaming:app --reload
# Each line has a short comment saying WHAT it is.

# os: os.environ reads environment variables.
import os
# threading: run code in the background.
import threading
# time: sleep() pauses.
import time
# Iterator: type label for something that gives items one at a time.
from collections.abc import Iterator

# httpx: sends web requests from Python.
import httpx
# uvicorn: runs the FastAPI app.
import uvicorn
# FastAPI: creates the app; HTTPException: error reply.
from fastapi import FastAPI, HTTPException
# StreamingResponse: sends a reply in pieces as they are ready.
from fastapi.responses import StreamingResponse
# OpenAI: client class for talking to OpenAI's models.
from openai import OpenAI
# BaseModel: data shape; Field: field rules.
from pydantic import BaseModel, Field

# os.environ.get(NAME) reads the key from the environment (None if unset).
API_KEY = os.environ.get("OPENAI_API_KEY")
# Which model to call.
MODEL = "gpt-4o-mini"
# Real client only if a key exists, otherwise None (use the fake model).
client = OpenAI(api_key=API_KEY) if API_KEY else None

# Create the app.
app = FastAPI(title="LLM service")


# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Request and response models
# Input shape; min_length/max_length limit the text size.
class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    system: str = "You are a helpful assistant."


# Output shape.
class ChatResponse(BaseModel):
    reply: str
    model: str


# %% The LLM calls (real or fake)
# Returns the whole reply at once (real or fake).
def llm_complete(request: ChatRequest) -> str:
    if client is None:
        return f"(fake model) You said: {request.message}"
    # chat.completions.create(...): ask the model; messages = chat history (system = rules, user = question); timeout = give up after 30 s.
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": request.system}, {"role": "user", "content": request.message}],
        timeout=30,
    )
    # The reply text from the first choice.
    return response.choices[0].message.content


# A generator: 'yield' hands out one piece at a time instead of returning once.
def llm_stream(request: ChatRequest) -> Iterator[str]:
    if client is None:
        # split(): breaks text into words; sleep fakes thinking time.
        for word in f"(fake model) You said: {request.message}".split():
            time.sleep(0.05)
            yield word + " "
        return
    # stream=True: the model sends the reply in small chunks as it writes.
    stream = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": request.system}, {"role": "user", "content": request.message}],
        stream=True,
    )
    # Each chunk holds a small piece of text (delta.content).
    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


# %% Endpoints
# @app.post: POST endpoint; response_model=ChatResponse shapes the reply.
@app.post("/chat", response_model=ChatResponse)
# request: ChatRequest means the JSON body is validated against that model.
def chat(request: ChatRequest):
    try:
        return ChatResponse(reply=llm_complete(request), model=MODEL if client else "fake")
    # Catch any error so raw provider details are not leaked.
    except Exception as error:                                     # never leak raw provider errors
        # 502 = bad gateway (the upstream model failed); 'from error' keeps the original cause.
        raise HTTPException(status_code=502, detail="the model service failed") from error


# POST endpoint that streams its reply.
@app.post("/chat/stream")
def chat_stream(request: ChatRequest):
    # A generator producing Server-Sent Events: lines starting with 'data:' then a blank line.
    def events():
        for piece in llm_stream(request):
            yield f"data: {piece}\n\n"                              # Server-Sent Events format
        yield "data: [DONE]\n\n"

    # StreamingResponse(generator, media_type): sends each yielded piece as it arrives.
    return StreamingResponse(events(), media_type="text/event-stream")


# @app.get: GET endpoint to check the service is alive.
@app.get("/health")
def health():
    return {"status": "ok", "llm_configured": client is not None}


# %% Run and call it
# Starts the web server in a background thread so this script can also call it.
def serve(application, port):
    # uvicorn.Server/Config: uvicorn is the program that runs a FastAPI app; host/port = address, log_level='warning' = quiet.
    server = uvicorn.Server(uvicorn.Config(application, host="127.0.0.1", port=port, log_level="warning"))
    # Thread: runs server.run in the background; daemon=True means it dies when the script ends.
    thread = threading.Thread(target=server.run, daemon=True)
    # start(): begins running the thread.
    thread.start()
    # Wait (sleeping 0.05s each time) until the server is ready.
    while not server.started:
        time.sleep(0.05)
    return server, thread


server, thread = serve(app, 8104)
BASE = "http://127.0.0.1:8104"

# httpx.get(url).json(): GET request, read JSON reply; json=... sends a body; timeout = seconds to wait.
print(httpx.get(f"{BASE}/health").json())
print(httpx.post(f"{BASE}/chat", json={"message": "Explain RAG briefly"}, timeout=60).json())
print(httpx.post(f"{BASE}/chat", json={"message": ""}).status_code)       # validation: 422


# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Read the stream piece by piece
# httpx.stream(...): keeps the connection open and reads the reply as it arrives.
with httpx.stream("POST", f"{BASE}/chat/stream", json={"message": "stream this please"}, timeout=60) as response:
    # iter_lines(): yields the reply one line at a time.
    for line in response.iter_lines():
        if line.startswith("data: ") and line != "data: [DONE]":
            # removeprefix(x): cuts x off the start; end='' no newline; flush=True shows it immediately.
            print(line.removeprefix("data: "), end="", flush=True)
print()

# %% Production checklist for AI endpoints
# - Validate input size (cost and abuse control).
# - Timeouts + retries on the model call.
# - Authentication and per-user rate limits.
# - Log latency, tokens, errors (folder 16). Never log secrets.
# - Return friendly errors, not raw provider messages.
# - Keep keys in environment variables.

# Stop the server and wait up to 5 seconds.
server.should_exit = True
thread.join(timeout=5)
