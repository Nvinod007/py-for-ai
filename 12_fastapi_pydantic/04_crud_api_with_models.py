# A complete CRUD API: Create, Read, Update, Delete, using pydantic models.
# Run for real:  uv run uvicorn 04_crud_api_with_models:app --reload   (then open /docs)
# Each line has a short comment saying WHAT it is.

# threading: run code in the background.
import threading
# time: sleep() pauses the program.
import time
# Optional[X]: X or None.
from typing import Optional

# httpx: sends web requests from Python.
import httpx
# uvicorn: runs the FastAPI app as a server.
import uvicorn
# FastAPI: creates the app; HTTPException: send an error reply; Query: rules for query parameters; status: named HTTP codes.
from fastapi import FastAPI, HTTPException, Query, status
# BaseModel: data shape; Field: rules for a field.
from pydantic import BaseModel, Field

# Create the app; title shows in /docs.
app = FastAPI(title="Todo API")


# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Models: what comes in, what goes out
# Shape of data a client sends to create a todo; min_length/max_length = text size, ge/le = number range.
class TodoCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    priority: int = Field(default=3, ge=1, le=5)


# All fields optional (default None) so a client can change just some.
class TodoUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=100)
    priority: Optional[int] = Field(default=None, ge=1, le=5)
    done: Optional[bool] = None


# Shape of what the API returns.
class Todo(BaseModel):
    id: int
    title: str
    priority: int
    done: bool = False


# Fake in-memory database: id -> Todo (lost when the program stops).
DB: dict[int, Todo] = {}
# Counter for new ids (a dict so functions can change it).
next_id = {"value": 1}


# %% Endpoints
# @app.post: handles POST (create). response_model=Todo shapes the reply; status_code=201 means Created.
@app.post("/todos", response_model=Todo, status_code=status.HTTP_201_CREATED)
# payload: TodoCreate means the JSON body is checked against that model.
def create_todo(payload: TodoCreate):
    # model_dump(): model -> dict; ** unpacks it into named arguments.
    todo = Todo(id=next_id["value"], **payload.model_dump())
    DB[todo.id] = todo
    next_id["value"] += 1
    return todo


# @app.get: list todos; response_model=list[Todo] means a list of Todo.
@app.get("/todos", response_model=list[Todo])
# Query(10, ge=1, le=100): query parameter 'limit', default 10, allowed 1-100.
def list_todos(done: Optional[bool] = None, limit: int = Query(10, ge=1, le=100)):
    # List comprehension: keep todos that match the optional 'done' filter.
    items = [t for t in DB.values() if done is None or t.done == done]
    return items[:limit]


# {todo_id} in the path is passed to the function (converted to int).
@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    if todo_id not in DB:
        # raise HTTPException(status_code, detail): stops and sends this error reply (404 = not found).
        raise HTTPException(status_code=404, detail=f"todo {todo_id} not found")
    return DB[todo_id]


# @app.patch: handles PATCH (change part of an item).
@app.patch("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, changes: TodoUpdate):
    if todo_id not in DB:
        raise HTTPException(status_code=404, detail=f"todo {todo_id} not found")
    # exclude_unset=True: only the fields the client actually sent; model_copy(update=...) makes a changed copy.
    updated = DB[todo_id].model_copy(update=changes.model_dump(exclude_unset=True))
    DB[todo_id] = updated
    return updated


# @app.delete: handles DELETE; 204 means success with no body.
@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int):
    # dict.pop(key, None): removes the item and returns it, or None if missing.
    if DB.pop(todo_id, None) is None:
        raise HTTPException(status_code=404, detail=f"todo {todo_id} not found")


# %% Run the server in the background
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


server, thread = serve(app, 8102)
BASE = "http://127.0.0.1:8102"

# %% Create
# httpx.post(url, json={...}): send a POST with a JSON body.
r = httpx.post(f"{BASE}/todos", json={"title": "Learn FastAPI", "priority": 1})
print(r.status_code, r.json())
httpx.post(f"{BASE}/todos", json={"title": "Build RAG"})

# %% Read
# httpx.get(url): GET request; .json() reads the reply as data.
print(httpx.get(f"{BASE}/todos").json())
print(httpx.get(f"{BASE}/todos/1").json())
print(httpx.get(f"{BASE}/todos/99").status_code, httpx.get(f"{BASE}/todos/99").json())

# %% Update
# httpx.patch(url, json=...): send a PATCH request.
print(httpx.patch(f"{BASE}/todos/1", json={"done": True}).json())
print(httpx.get(f"{BASE}/todos", params={"done": True}).json())

# %% Validation protects the API
# Invalid body: expect 422 and the names of the bad fields.
bad = httpx.post(f"{BASE}/todos", json={"title": "", "priority": 9})
print(bad.status_code, [e["loc"][-1] for e in bad.json()["detail"]])

# %% Delete
# httpx.delete(url): send a DELETE request.
print(httpx.delete(f"{BASE}/todos/2").status_code)
print(httpx.get(f"{BASE}/todos").json())


# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% HTTP verbs and codes to remember
# GET read | POST create | PUT replace | PATCH change part | DELETE remove
# 200 OK | 201 Created | 204 No Content | 400 Bad request | 401 Not logged in
# 403 Forbidden | 404 Not found | 409 Conflict | 422 Invalid data | 500 Server error

# Stop the server and wait up to 5 seconds.
server.should_exit = True
thread.join(timeout=5)
