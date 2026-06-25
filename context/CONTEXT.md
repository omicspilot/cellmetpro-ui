# CellMetPro UI — Project Context

## What this is

A companion application to **CellMetPro** (https://github.com/omicspilot/CellMetPro), a Python
package for single-cell RNA-seq metabolic analysis. CellMetPro is live on PyPI and provides
a CLI and Python API. This new project makes those capabilities accessible to scientists who are not
comfortable with the command line or Python.

The goal is a **production-quality, open-source, cross-platform application** — not a demo or
internal tool. Every architectural and code decision should reflect that standard.

---

## The developer

**Oumar Ndiaye** — bioinformatics engineer and the author of CellMetPro.

- Comfortable with Python: built CellMetPro end-to-end (COMPASS algorithm, FBA, scRNA-seq analysis pipeline,
  CLI, test suite at 80% coverage, CI/CD with GitHub Actions, published to PyPI)
- Strong JavaScript: knows React and Vue; has shipped JS projects
- Not a fan of Java; avoid unless there is a genuinely compelling reason
- This project is also a **learning journey** — specifically to deepen expertise in:
  - Production Electron app architecture and packaging
  - TypeScript at scale
  - FastAPI for real-world APIs (async, WebSockets, background jobs, auth)
  - Modern React patterns (React Query, Zustand, component libraries)
  - Docker and cross-platform distribution
- Quality bar: the learning context does not lower the bar — every feature ships at production level.
  No shortcuts, no "we'll clean this up later." Code is typed, tested, documented, and CI-gated.

---

## Architecture decision

### Two-piece design

```
┌─────────────────────────────────────────────────────────────┐
│  Piece 1: cellmetpro-server  (Python, pip-installable)      │
│  FastAPI application that wraps cellmetpro operations        │
│  Runs wherever the user wants: local machine, HPC, cloud VM  │
└────────────────────────┬────────────────────────────────────┘
                         │ REST + WebSocket
┌────────────────────────▼────────────────────────────────────┐
│  Piece 2: CellMetPro Desktop  (Electron + React)            │
│  The React frontend works standalone in any browser too      │
│  Electron is a thin shell: process management + native UX   │
└─────────────────────────────────────────────────────────────┘
```

### Two operating modes (same codebase, config-switchable)

**Mode 1 — Local (default for most users)**
- User downloads and double-clicks the desktop app
- Electron checks for `cellmetpro-server` installation, prompts to install if missing
- Electron spawns the Python server as a child process and manages its lifecycle
- User never sees a terminal

**Mode 2 — Remote (for power users and labs)**
- User (or their sysadmin) runs `pip install cellmetpro-server && cellmetpro-server start` on a
  remote machine (HPC cluster, cloud VM, lab workstation with a GPU)
- User opens the desktop app, goes to Settings, enters the server URL and an auth token
- The React frontend connects to the remote server; all computation happens there
- The desktop app is purely a UI client in this mode

### Why this architecture

- Open source and zero hosting costs — users bring their own compute
- Non-technical users get a double-click install experience
- Power users get full flexibility (HPC, Docker, bare metal)
- The React frontend is backend-agnostic: it only talks to a URL, so it works identically inside
  Electron or in a plain browser (for Docker/self-hosted setups)
- The API layer makes CellMetPro accessible to future R clients or third-party tools for free

---

## Monorepo structure

```
cellmetpro-ui/                         # new GitHub repo
├── packages/
│   ├── server/                        # pip-installable Python package
│   │   ├── cellmetpro_server/
│   │   │   ├── main.py                # FastAPI app entrypoint
│   │   │   ├── routers/               # one router per analysis domain
│   │   │   │   ├── compass.py
│   │   │   │   ├── differential.py
│   │   │   │   ├── clustering.py
│   │   │   │   ├── visualization.py
│   │   │   │   └── io.py
│   │   │   ├── jobs.py                # background job management
│   │   │   ├── auth.py                # token auth for remote mode
│   │   │   └── ws.py                  # WebSocket progress streaming
│   │   ├── pyproject.toml
│   │   └── tests/
│   │
│   └── desktop/                       # Electron + React
│       ├── src/                       # React app (also works in browser)
│       │   ├── app/                   # routing, layout
│       │   ├── features/              # one folder per feature domain
│       │   │   ├── upload/
│       │   │   ├── scoring/
│       │   │   ├── differential/
│       │   │   ├── clustering/
│       │   │   ├── visualization/
│       │   │   └── settings/
│       │   ├── api/                   # typed API client (auto-generated from OpenAPI)
│       │   ├── store/                 # Zustand global state
│       │   └── components/            # shared UI components
│       ├── electron/                  # Electron shell
│       │   ├── main.ts                # main process: window, server lifecycle
│       │   ├── preload.ts             # context bridge
│       │   └── server-manager.ts      # spawn / kill Python server
│       ├── package.json
│       └── vite.config.ts
│
├── docker/
│   └── Dockerfile                     # docker run -p 8000:8000 cellmetpro/server
├── .github/
│   └── workflows/
│       ├── ci.yml                     # lint + test on every PR
│       └── release.yml                # build installers + publish on tag
└── README.md
```

---

## Technology stack

### Backend (`packages/server`)

| Concern | Choice | Reason |
|---|---|---|
| Framework | **FastAPI** | Async, WebSocket native, auto OpenAPI docs |
| Task queue | **FastAPI BackgroundTasks** (start), migrate to **ARQ** if needed | Avoids Celery overhead early on |
| Progress streaming | **WebSocket** per job ID | Real-time progress bars in the UI |
| Auth (remote mode) | **Bearer token** (static, user-generated) | Simple, no OAuth overhead for v1 |
| Package versioning | `cellmetpro-server==X.Y` pins `cellmetpro==X.Y` | One server version per cellmetpro version |
| Testing | **pytest** + **httpx** (async test client) | Consistent with CellMetPro |
| Linting | **ruff** + **mypy** | ruff handles both linting and formatting (black-compatible) |

### Frontend (`packages/desktop`)

| Concern | Choice | Reason |
|---|---|---|
| Framework | **React 18 + TypeScript** | Known stack, large ecosystem |
| Build | **Vite** | Fast HMR, small bundles |
| State | **Zustand** | Minimal, TypeScript-first, no boilerplate |
| Server state | **TanStack Query (React Query)** | Caching, background refetch, loading states |
| UI components | **shadcn/ui** (Radix + Tailwind) | Unstyled primitives, full control, accessible |
| Routing | **React Router v6** | File-based routes inside Vite |
| Charts | **Recharts** or **Plotly.js** | Plotly for scientific plots (matches Python side) |
| API client | **Auto-generated from OpenAPI spec** (openapi-ts) | Types always in sync with backend |
| Forms | **React Hook Form + Zod** | Type-safe validation |
| Testing | **Vitest** + **Testing Library** | Fast, Vite-native |

### Electron shell

| Concern | Choice |
|---|---|
| Electron version | Latest stable |
| Bundler | **electron-builder** |
| IPC | Context bridge (no `nodeIntegration`) |
| Server management | `child_process.spawn` with stdout/stderr piped to a log panel |
| Auto-updater | **electron-updater** (GitHub Releases) |
| Distribution | `.dmg` (macOS), `.exe` NSIS installer (Windows), `.AppImage` (Linux) |

---

## Key product decisions

### File handling
- Users upload data files (CSV, h5ad, MTX) via a drag-and-drop zone in the UI
- In local mode: files are written to a temp directory that the server reads from
- In remote mode: files are multipart-uploaded to the server via the API
- Results (plots, CSVs) are downloadable from the UI

### Job model
- Every analysis operation is a **job** with a UUID
- Job states: `pending → running → complete | failed`
- Progress streamed via WebSocket: `{ job_id, step, progress, message }`
- UI shows a live progress panel — no black-box waiting

### Version management
- The server reports which cellmetpro version it is running (`GET /version`)
- The desktop app displays this in the status bar
- Remote mode: user chooses which server (and thus which cellmetpro version) to connect to
- This enables side-by-side comparison between versions in the future

### Auth model (remote mode only)
- Server started with `cellmetpro-server start --token <token>`
- Client sends `Authorization: Bearer <token>` on every request
- Local mode: no auth (localhost only, token ignored)

---

## Quality standards (non-negotiable)

- **TypeScript strict mode** throughout the frontend — no `any`
- **mypy** on the backend with `--strict` or `--ignore-missing-imports` at minimum
- **100% of API routes have tests** (pytest + httpx)
- **CI blocks merges** on failing tests, lint, or type errors
- **No `console.log` or `print` in production code** — structured logging only
- **Semantic versioning** — server and desktop versions are kept in sync
- **Changelog** maintained for every release (Keep a Changelog format)
- **Accessibility**: all interactive UI elements keyboard-navigable, ARIA labels on custom components

---

## Relationship to CellMetPro

- `cellmetpro-server` depends on `cellmetpro` as a library — it never reimplements analysis logic
- When CellMetPro releases a new version, `cellmetpro-server` releases a matching version
- The desktop app is version-agnostic as long as the server API contract is maintained
- Breaking API changes follow semver (major bump)
- CellMetPro itself remains a fully independent CLI/Python package — this project adds a UI layer,
  it does not replace or fork CellMetPro

---

## Open source

- License: **MIT** (consistent with CellMetPro)
- GitHub: new repo under `ndiayeoumar/cellmetpro-ui` (or `omicspilot/cellmetpro-ui`)
- Issues and PRs welcome from day one
- CONTRIBUTING.md, CODE_OF_CONDUCT.md, and issue templates from the start
