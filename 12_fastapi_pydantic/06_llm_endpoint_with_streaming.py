# An AI endpoint: validated input, an LLM call, and streamed output.
# Without OPENAI_API_KEY it uses a fake model, with a key it calls the real one.
# Run for real:  uv run uvicorn 06_llm_endpoint_with_streaming:app --reload

import os
import threading
import time
from collections.abc import Iterator

import httpx
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from openai import OpenAI
from pydantic import BaseModel, Field

API_KEY = os.environ.get("OPENAI_API_KEY")
MODEL = "gpt-4o-mini"
client = OpenAI(api_key=API_KEY) if API_KEY else None

app = FastAPI(title="LLM service")


# %% Request and response models
class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000)
    system: str = "You are a helpful assistant."


class ChatResponse(BaseModel):
    reply: str
    model: str


# %% The LLM calls (real or fake)
def llm_complete(request: ChatRequest) -> str:
    if client is None:
        return f"(fake model) You said: {request.message}"
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": request.system}, {"role": "user", "content": request.message}],
        timeout=30,
    )
    return response.choices[0].message.content


def llm_stream(request: ChatRequest) -> Iterator[str]:
    if client is None:
        for word in f"(fake model) You said: {request.message}".split():
            time.sleep(0.05)
            yield word + " "
        return
    stream = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "system", "content": request.system}, {"role": "user", "content": request.message}],
        stream=True,
    )
    for chunk in stream:
        if chunk.choices and chunk.choices[0].delta.content:
            yield chunk.choices[0].delta.content


# %% Endpoints
@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest):
    try:
        return ChatResponse(reply=llm_complete(request), model=MODEL if client else "fake")
    except Exception as error:                                     # never leak raw provider errors
        raise HTTPException(status_code=502, detail="the model service failed") from error


@app.post("/chat/stream")
def chat_stream(request: ChatRequest):
    def events():
        for piece in llm_stream(request):
            yield f"data: {piece}\n\n"                              # Server-Sent Events format
        yield "data: [DONE]\n\n"

    return StreamingResponse(events(), media_type="text/event-stream")


@app.get("/health")
def health():
    return {"status": "ok", "llm_configured": client is not None}


# %% Run and call it
def serve(application, port):
    server = uvicorn.Server(uvicorn.Config(application, host="127.0.0.1", port=port, log_level="warning"))
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    while not server.started:
        time.sleep(0.05)
    return server, thread


server, thread = serve(app, 8104)
BASE = "http://127.0.0.1:8104"

print(httpx.get(f"{BASE}/health").json())
print(httpx.post(f"{BASE}/chat", json={"message": "Explain RAG briefly"}, timeout=60).json())
print(httpx.post(f"{BASE}/chat", json={"message": ""}).status_code)       # validation: 422

# %% Read the stream piece by piece
with httpx.stream("POST", f"{BASE}/chat/stream", json={"message": "stream this please"}, timeout=60) as response:
    for line in response.iter_lines():
        if line.startswith("data: ") and line != "data: [DONE]":
            print(line.removeprefix("data: "), end="", flush=True)
print()

# %% Production checklist for AI endpoints
# - Validate input size (cost and abuse control).
# - Timeouts + retries on the model call.
# - Authentication and per-user rate limits.
# - Log latency, tokens, errors (folder 16). Never log secrets.
# - Return friendly errors, not raw provider messages.
# - Keep keys in environment variables.

server.should_exit = True
thread.join(timeout=5)
