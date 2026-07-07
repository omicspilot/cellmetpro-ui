# CellMetPro UI — Implementation Roadmap

This file is the single source of truth for the full implementation plan.
Each step is tackled linearly. Check off items as they are completed.

---

## Phase 0 — Monorepo & Tooling Foundation

> Everything else sits on this. Get it right first.

- [x] **0.1** — Monorepo structure with `pnpm` workspaces
- [x] **0.2** — Python environment: `uv`, `pyproject.toml`, `ruff` / `mypy`
- [x] **0.3** — Node/TS environment: `pnpm`, `tsconfig`, `eslint` / `prettier`
- [x] **0.4** — Git hygiene: `.gitignore`, `commitlint`, conventional commits
- [x] **0.5** — Pre-commit hooks (Python + JS in one repo)

---

## Phase 1 — FastAPI Server (`packages/server`)

> Python home ground, but with real-world production patterns.

- [x] **1.1** — FastAPI app skeleton, project layout, Uvicorn
- [x] **1.2** — Health check + `GET /version` endpoint
- [x] **1.3** — File I/O router: multipart upload, temp directory management
- [x] **1.4** — Background jobs system (`BackgroundTasks` → job UUID state model)
- [x] **1.5** — WebSocket progress streaming (`ws.py`)
- [~] **1.6** — COMPASS / scoring router (wraps `cellmetpro`)
- [ ] **1.7** — Differential, clustering, visualization routers
- [ ] **1.8** — Auth middleware: Bearer token (remote mode only)
- [ ] **1.9** — Error handling, structured logging, CORS
- [ ] **1.10** — pytest + httpx test suite (100% route coverage target)
- [ ] **1.11** — OpenAPI spec export (feeds the frontend type generator)

---

## Phase 2 — React Frontend (`packages/desktop/src`)

> Known stack, but with production-grade architecture patterns.

- [ ] **2.1** — Vite + React + TypeScript scaffold
- [ ] **2.2** — Tailwind CSS + shadcn/ui setup
- [ ] **2.3** — React Router v6: root layout, route definitions
- [ ] **2.4** — Zustand store: connection state, active job state
- [ ] **2.5** — Auto-generated API client from OpenAPI spec (`openapi-ts`)
- [ ] **2.6** — TanStack Query: data fetching layer, query/mutation patterns
- [ ] **2.7** — Feature: File upload (drag-and-drop, multipart POST)
- [ ] **2.8** — Feature: Job progress panel (WebSocket consumer, live progress bar)
- [ ] **2.9** — Feature: Scoring / COMPASS form (React Hook Form + Zod validation)
- [ ] **2.10** — Feature: Differential expression view
- [ ] **2.11** — Feature: Clustering view
- [ ] **2.12** — Feature: Visualization (Plotly.js integration)
- [ ] **2.13** — Feature: Settings page (server URL, auth token, mode switch)
- [ ] **2.14** — Accessibility audit (keyboard navigation, ARIA labels)
- [ ] **2.15** — Vitest + Testing Library test suite

---

## Phase 3 — Electron Shell (`packages/desktop/electron`)

> The new frontier: IPC, native OS integration, process management.

- [ ] **3.1** — Electron main process: `BrowserWindow`, security hardening
- [ ] **3.2** — Context bridge / preload: IPC surface design
- [ ] **3.3** — Server manager: spawn Python server, pipe logs, kill on quit
- [ ] **3.4** — Local mode vs remote mode switching
- [ ] **3.5** — Native dialogs: file open, save, system notifications
- [ ] **3.6** — Auto-updater (`electron-updater` + GitHub Releases)
- [ ] **3.7** — electron-builder config: `.dmg` (macOS), `.exe` NSIS (Windows), `.AppImage` (Linux)

---

## Phase 4 — Integration & End-to-End

> Wire all three pieces together and harden the seams.

- [ ] **4.1** — Local mode full flow: Electron spawns server → React connects
- [ ] **4.2** — Remote mode full flow: React → auth token → remote server
- [ ] **4.3** — Error states: server unreachable, version mismatch, auth failure
- [ ] **4.4** — E2E testing strategy (Playwright + Electron driver)

---

## Phase 5 — CI/CD, Docker & Release

> Ship it like a real open-source product.

- [ ] **5.1** — GitHub Actions `ci.yml`: lint + test on every PR
- [ ] **5.2** — GitHub Actions `release.yml`: build installers + publish on tag
- [ ] **5.3** — Docker: `cellmetpro/server` image (for self-hosted / Docker mode)
- [ ] **5.4** — Community files: `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`, issue templates
- [ ] **5.5** — Changelog (`CHANGELOG.md`, Keep a Changelog format) + semantic versioning strategy

---

## Legend

| Symbol | Meaning |
|--------|---------|
| `[ ]`  | Not started |
| `[~]`  | In progress |
| `[x]`  | Done |
