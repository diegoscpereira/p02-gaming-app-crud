# 🎮 Game Library — CRUD API + Dashboard

A full-stack CRUD application that lets you search the [RAWG](https://rawg.io) video game database, save games to a personal library, and track your own status, rating, and comments for each one — built to demonstrate backend/data-engineering fundamentals: API design, relational modeling, data validation, and clean service-layer architecture.

![Demo](docs/demo_p02_crud_project.gif)

---

## Badges

![Python](https://img.shields.io/badge/Python-3.12-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-ORM-CC2927)
![Pydantic](https://img.shields.io/badge/Pydantic-v2-E92063?logo=pydantic&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-database-003B57?logo=sqlite&logoColor=white)
![NiceGUI](https://img.shields.io/badge/NiceGUI-frontend-5C2D91)
![uv](https://img.shields.io/badge/uv-package%20manager-DE5FE9)
![License](https://img.shields.io/badge/license-MIT-green)

---

## What this demonstrates

- **REST API design** — a FastAPI backend with proper CRUD verbs, status codes, path vs. query parameters, and auto-generated interactive docs (Swagger/ReDoc).
- **Data validation at every boundary** — Pydantic schemas validate and reshape data at each point it crosses into or out of the system (external API → backend, frontend → backend, backend → database, database → frontend), rather than trusting any single source blindly.
- **ETL-style data cleaning** — real-world API responses are messy (missing fields, inconsistent nesting, mismatched key names). This project handles that with Pydantic field aliases, `mode="before"` validators, and nullability decisions verified against live data rather than assumed.
- **ORM-based persistence** — SQLAlchemy 2.0 typed models (`Mapped[...]`), a proper database-agnostic connection layer, and a clean write cycle (`add` → `commit` → `refresh`).
- **Layered architecture** — routers, services, schemas, and models each have one job, so the codebase stays readable as it grows. See [Architecture](#architecture) below.
- **Configuration & secrets handled correctly** — typed, validated settings via `pydantic-settings`, reading from a `.env` file that is never committed (see `.env.example`).

---

## Tech stack

| Layer | Tool | Why |
|---|---|---|
| Backend framework | **FastAPI** | Type-hint-driven validation, automatic docs, async-ready |
| Data validation | **Pydantic v2** | Schema validation and data cleaning at every system boundary |
| ORM | **SQLAlchemy 2.0** | Typed models, database-agnostic persistence |
| Database | **SQLite** | Zero-setup for local development; swapping to PostgreSQL is a one-line change to the connection URL |
| Config | **pydantic-settings** | Typed, fail-fast environment configuration |
| Frontend | **NiceGUI** | Pure-Python interactive UI, calls the API exactly like any other client |
| HTTP client | **httpx** | Async-friendly requests, used both server-side (RAWG calls) and client-side (frontend → backend) |
| External data source | **[RAWG Video Games API](https://rawg.io/apidocs)** | Free, no-cost tier; 500,000+ game catalog |
| Environment | **uv** | Fast, modern Python dependency management |

---

## Architecture

```
Frontend (NiceGUI)  →  HTTP/JSON  →  Backend (FastAPI)  →  RAWG API
                                            │
                                            ▼
                                   SQLite (via SQLAlchemy)
```

The frontend never touches the database directly — it only ever talks to the backend's REST API, the same way any other client (Swagger, a mobile app, a future integration) would.

```
backend/
├── main.py              # FastAPI app instance, router registration
├── config.py             # Typed settings (pydantic-settings), reads .env once
├── database.py             # SQLAlchemy engine, session factory, Base
├── models.py                 # Library table (SQLAlchemy)
├── schemas.py                  # Pydantic schemas — one per system boundary
├── rawg_client.py                # Thin HTTP client for the RAWG API only
├── services/
│   ├── explore.py                  # Search RAWG, validate + clean results
│   └── library.py                    # All database CRUD operations
└── routers/
    ├── explore.py                      # GET /explore/ — search endpoint
    └── library.py                        # /library/ — full CRUD endpoints

frontend/
└── app.py                # NiceGUI pages: Explore + My Library
```

**Design principle:** each file answers one question.
- `models.py` — how does data live in *my* database?
- `schemas.py` — what does data look like as it *crosses a boundary* (API in/out, RAWG in)?
- `rawg_client.py` — how do I talk to RAWG, and nothing else?
- `services/` — what actually happens (business logic, database operations)?
- `routers/` — how does an HTTP request map to that logic?

### A key design decision: single table, not normalized

`Library` stores both the RAWG snapshot (title, description, rating, platforms, etc.) *and* the user's own data (status, rating, comment) in one table, rather than a normalized `games` + `library` pair joined by a foreign key.

**Trade-off, chosen deliberately:** if a game is deleted and re-added later, its RAWG data is re-fetched rather than reused. For a single-user portfolio project, that's a negligible cost, and it keeps the schema simple. A normalized version — separating "facts about a game" from "a user's relationship to a game" — is a natural, documented v2 refactor if this were to support multiple users.

---

## API endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/explore/?query=...` | Search RAWG for games |
| `POST` | `/library/` | Save a game to your library |
| `GET` | `/library/?skip=&limit=` | List saved games (paginated) |
| `GET` | `/library/{id}` | Get one saved game |
| `PUT` | `/library/{id}` | Update status / rating / comment |
| `DELETE` | `/library/{id}` | Remove a game from your library |

Full interactive documentation is available at `/docs` (Swagger UI) once the backend is running.

---

## Getting started

### 1. Clone and install

```bash
git clone https://github.com/diegoscpereira/p02-python-gaming-app-crud.git
cd p02-python-gaming-app-crud
uv sync
```

### 2. Configure your environment

Copy the example file and add your free RAWG API key ([get one here](https://rawg.io/apidocs) — takes about a minute):

```bash
cp .env.example .env
```

```
RAWG_API_KEY=your_key_here
```

### 3. Run the backend

```bash
uv run uvicorn backend.main:app --reload
```

API docs: [http://localhost:8000/docs](http://localhost:8000/docs)

### 4. Run the frontend (in a second terminal)

```bash
uv run python frontend/app.py
```

App: [http://localhost:8080](http://localhost:8080)

---

## Data source & attribution

Game data provided by the [RAWG Video Games Database API](https://rawg.io). This project uses RAWG's free tier for personal, non-commercial use.

---

## Roadmap / possible next steps

These are deliberately out of scope for v1, to keep the project focused on core CRUD + data-engineering fundamentals:

- [ ] `pytest` + `TestClient` coverage for the library CRUD endpoints
- [ ] Normalize `games` and `library` into separate tables with a foreign key
- [ ] Swap SQLite → PostgreSQL (one-line change to `database.py`) + Docker Compose
- [ ] Deploy (e.g. Cloud Run) with a live demo link
- [ ] Alembic migrations instead of `create_all`

---

## Author

Built by **Diego Pereira** as a portfolio project — [GitHub](https://github.com/diegoscpereira)