# A complete CRUD API: Create, Read, Update, Delete, using pydantic models.
# Run for real:  uv run uvicorn 04_crud_api_with_models:app --reload   (then open /docs)

import threading
import time
from typing import Optional

import httpx
import uvicorn
from fastapi import FastAPI, HTTPException, Query, status
from pydantic import BaseModel, Field

app = FastAPI(title="Todo API")


# %% Models: what comes in, what goes out
class TodoCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    priority: int = Field(default=3, ge=1, le=5)


class TodoUpdate(BaseModel):
    title: Optional[str] = Field(default=None, min_length=1, max_length=100)
    priority: Optional[int] = Field(default=None, ge=1, le=5)
    done: Optional[bool] = None


class Todo(BaseModel):
    id: int
    title: str
    priority: int
    done: bool = False


DB: dict[int, Todo] = {}
next_id = {"value": 1}


# %% Endpoints
@app.post("/todos", response_model=Todo, status_code=status.HTTP_201_CREATED)
def create_todo(payload: TodoCreate):
    todo = Todo(id=next_id["value"], **payload.model_dump())
    DB[todo.id] = todo
    next_id["value"] += 1
    return todo


@app.get("/todos", response_model=list[Todo])
def list_todos(done: Optional[bool] = None, limit: int = Query(10, ge=1, le=100)):
    items = [t for t in DB.values() if done is None or t.done == done]
    return items[:limit]


@app.get("/todos/{todo_id}", response_model=Todo)
def get_todo(todo_id: int):
    if todo_id not in DB:
        raise HTTPException(status_code=404, detail=f"todo {todo_id} not found")
    return DB[todo_id]


@app.patch("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, changes: TodoUpdate):
    if todo_id not in DB:
        raise HTTPException(status_code=404, detail=f"todo {todo_id} not found")
    updated = DB[todo_id].model_copy(update=changes.model_dump(exclude_unset=True))
    DB[todo_id] = updated
    return updated


@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int):
    if DB.pop(todo_id, None) is None:
        raise HTTPException(status_code=404, detail=f"todo {todo_id} not found")


# %% Run the server in the background
def serve(application, port):
    server = uvicorn.Server(uvicorn.Config(application, host="127.0.0.1", port=port, log_level="warning"))
    thread = threading.Thread(target=server.run, daemon=True)
    thread.start()
    while not server.started:
        time.sleep(0.05)
    return server, thread


server, thread = serve(app, 8102)
BASE = "http://127.0.0.1:8102"

# %% Create
r = httpx.post(f"{BASE}/todos", json={"title": "Learn FastAPI", "priority": 1})
print(r.status_code, r.json())
httpx.post(f"{BASE}/todos", json={"title": "Build RAG"})

# %% Read
print(httpx.get(f"{BASE}/todos").json())
print(httpx.get(f"{BASE}/todos/1").json())
print(httpx.get(f"{BASE}/todos/99").status_code, httpx.get(f"{BASE}/todos/99").json())

# %% Update
print(httpx.patch(f"{BASE}/todos/1", json={"done": True}).json())
print(httpx.get(f"{BASE}/todos", params={"done": True}).json())

# %% Validation protects the API
bad = httpx.post(f"{BASE}/todos", json={"title": "", "priority": 9})
print(bad.status_code, [e["loc"][-1] for e in bad.json()["detail"]])

# %% Delete
print(httpx.delete(f"{BASE}/todos/2").status_code)
print(httpx.get(f"{BASE}/todos").json())

# %% HTTP verbs and codes to remember
# GET read | POST create | PUT replace | PATCH change part | DELETE remove
# 200 OK | 201 Created | 204 No Content | 400 Bad request | 401 Not logged in
# 403 Forbidden | 404 Not found | 409 Conflict | 422 Invalid data | 500 Server error

server.should_exit = True
thread.join(timeout=5)
