# py-for-ai

Hands-on Python for AI / FDE work. Go folder by folder, file by file, in numeric order.

## Setup

```bash
uv sync                 # install deps from pyproject.toml
uv run python 01_numpy/01_array_basics.py   # run any lesson (use real filenames)
```

Lessons use `# %%` cells, so you can run them cell by cell in Cursor/VS Code. Run from the project root or from inside a lesson folder.

## Roadmap (in order)

| Folder | Topic |
|---|---|
| `00_oops` | Classes, self, 4 pillars, dunder methods, abstraction |
| `01_numpy` | Arrays, indexing, math, broadcasting, linear algebra |
| `02_pandas` | DataFrames, cleaning, groupby, merge, time series |
| `03_matplotlib` | Plots, subplots, styling |
| `04_seaborn` | Statistical visualization |
| `05_python_essentials` | File I/O, exceptions, generators, decorators, typing, logging, async |
| `06_git_and_terminal` | Terminal, git basics, branches/PRs, undo (`.md`) |
| `07_http_and_apis` | requests, auth, pagination, retries, httpx |
| `08_sql` | SQLite, joins, CTEs, window functions. **Run `01` first** (creates `data/output/shop.db`) |
| `09_llm_apis` | OpenAI/Anthropic calls, structured output, tools, streaming |
| `10_rag` | Embeddings, chunking, vector search, RAG, evaluation |
| `11_agents` | Agent loop, tools, memory, planning, guardrails |
| `12_fastapi_pydantic` | Pydantic, FastAPI CRUD, middleware, LLM endpoint |
| `13_docker_and_cloud` | Docker, Compose, deployment (`.md` + example app) |
| `14_machine_learning` | scikit-learn: regression, classification, pipelines, clustering |
| `15_deep_learning` | PyTorch, autograd, attention, tiny GPT |
| `16_evals_and_observability` | Eval datasets, LLM-as-judge, tracing, monitoring |

## Data

`data/` holds sample CSVs and a FAQ doc used by the lessons. Generated files go to `data/output/`.

## API keys

LLM lessons work offline with fake fallbacks. For real calls, set keys in your shell (names are in `.env.example`):

```bash
export OPENAI_API_KEY=...
export ANTHROPIC_API_KEY=...
```

Never commit real keys.

## Notes

- Docker/cloud examples in `13_docker_and_cloud` were not executed during authoring.
- All `.py` lessons in 05–16 were run headless and pass.
