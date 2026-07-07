# CellMetPro Server

FastAPI server for the [CellMetPro](https://pypi.org/project/cellmetpro/) desktop application. Handles file I/O, background job tracking, and WebSocket progress streaming. Intended to run either as an embedded process spawned by the Electron shell (local mode) or as a standalone remote server.

---


## For Developers
### Prerequisites

- Python ≥ 3.10
- [uv](https://docs.astral.sh/uv/getting-started/installation/) — manages the virtual environment and runs all Python commands
- [pre-commit](https://pre-commit.com/#install) — installed once globally (`pipx install pre-commit` or `brew install pre-commit`)

---

### First-time setup

Run this once after cloning, and again any time `pyproject.toml` changes:

```bash
cd packages/server
make dev
```

This installs all dev dependencies (mypy, pytest, ruff, httpx…) into `.venv` and registers the git hooks.

> If `make` is not available, run the two commands manually:
> ```bash
> uv sync --extra dev
> pre-commit install
> ```

---

### Daily development workflow

#### Before committing — quality pass

The pre-commit hooks (mypy, ruff, eslint, prettier) run automatically on `git commit`. To run the Python quality pass manually before that — and auto-fix what can be fixed — add this alias to your shell profile (`.zshrc` / `.bashrc`):

```bash
alias uv_clean_code="uv sync --extra dev && uv run mypy . && uv run ruff check --fix . && uv run ruff format ."
```

Or use the equivalent Makefile target (does the same thing, skipping the sync step):

```bash
make check
```

Run either from `packages/server/`.

#### Running tests

```bash
make test
# or
uv run pytest tests
```

#### Starting the server

```bash
make serve
# or
uv run cellmetpro-server
```

The server starts on `http://127.0.0.1:8000` by default. Interactive API docs are available at `/docs`.

---

### Project layout

```
packages/server/
├── cellmetpro_server/
│   ├── main.py          # FastAPI app, router registration
│   ├── config.py        # Settings via pydantic-settings
│   ├── jobs.py          # Job model, JobStore, in-memory state
│   └── routers/
│       ├── system.py    # GET /health, GET /version
│       ├── io.py        # File upload / download / delete
│       ├── jobs.py      # Job list and status endpoints
│       └── ws.py        # WebSocket progress streaming
├── tests/
├── pyproject.toml       # Dependencies, ruff, mypy, pytest config
├── Makefile
└── uv.lock
```

---

### Environment variables

Settings are read from the environment (or a `.env` file) via `pydantic-settings`. All are optional.

| Variable    | Default       | Description                        |
|-------------|---------------|------------------------------------|
| `HOST`      | `127.0.0.1`   | Bind address                       |
| `PORT`      | `8000`        | Bind port                          |
| `LOG_LEVEL` | `info`        | Uvicorn log level                  |
| `RELOAD`    | `false`       | Enable auto-reload (dev only)      |
