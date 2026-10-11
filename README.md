# Warehouse Management System

[![CI](https://github.com/akincenk/warehouse-management-system/actions/workflows/ci.yml/badge.svg)](https://github.com/akincenk/warehouse-management-system/actions/workflows/ci.yml)

A small inventory app: a FastAPI + SQLAlchemy REST API with JWT authentication and role-based access, plus a minimal React login/dashboard client.

## What it does

- Users register (always as `staff`) and log in with the OAuth2 password flow to get a short-lived JWT.
- Products have a name and a quantity. There are three roles:

  | Role | Products | Users |
  | --- | --- | --- |
  | `staff` | list, view | - |
  | `manager` | list, view, create, update, delete | - |
  | `admin` | list, view, create, update, delete | list, change role |
- The first admin is created from the command line (`create_admin.py`), not through the public API.

## Stack

- **Backend:** Python 3.11+, FastAPI, SQLAlchemy 2, Pydantic 2, PyJWT, bcrypt. SQLite by default (any SQLAlchemy URL via `DATABASE_URL`).
- **Frontend:** React 18 (Create React App), React Router, Axios.
- **Tooling:** pytest, ruff, pip-audit, Docker, GitHub Actions, Dependabot.

```
backend/
  main.py            app, CORS, router wiring
  database.py        engine/session from DATABASE_URL
  models.py          User, Product
  schemas.py         Pydantic request/response models
  auth/security.py   bcrypt hashing, JWT issue/verify, role checks
  auth/auth_routes.py  /auth/register, /auth/login, /auth/me
  routes/            /products, /users
  create_admin.py    CLI to create or promote an admin
  tests/
frontend/
  src/components/    Login, Dashboard
```

## Quickstart

### Backend

```bash
cd backend
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env   # then set JWT_SECRET
export $(grep -v '^#' .env | xargs)
python create_admin.py admin        # prompts for a password (8+ chars)
uvicorn main:app --reload
```

Generate a secret with `python -c "import secrets; print(secrets.token_urlsafe(48))"`. The app refuses to start without a `JWT_SECRET` of at least 32 characters.

### Backend with Docker

```bash
export JWT_SECRET="$(python3 -c 'import secrets; print(secrets.token_urlsafe(48))')"
docker build -t warehouse-api backend
docker run --rm -it -e JWT_SECRET -v warehouse-data:/data warehouse-api python create_admin.py admin
docker run --rm -p 8000:8000 -e JWT_SECRET -v warehouse-data:/data warehouse-api
```

The image runs as a non-root user and keeps the SQLite file in the `/data` volume.

Interactive API docs: http://127.0.0.1:8000/docs (use the **Authorize** button with your username/password).

### Frontend

Requires Node 18+.

```bash
cd frontend
npm install
npm start            # http://localhost:3000
```

The client calls `http://localhost:8000` by default; override with `REACT_APP_API_URL`. The backend allows the origins listed in `CORS_ORIGINS` (default `http://localhost:3000`).

## Configuration

| Variable | Default | Purpose |
| --- | --- | --- |
| `JWT_SECRET` | none (required) | HMAC key for signing tokens |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | `30` | Token lifetime |
| `DATABASE_URL` | `sqlite:///./warehouse.db` | SQLAlchemy URL |
| `CORS_ORIGINS` | `http://localhost:3000` | Comma-separated allowed origins |

## API overview

| Method | Path | Access |
| --- | --- | --- |
| POST | `/auth/register` | public (creates `staff`) |
| POST | `/auth/login` | public, form fields `username`, `password` |
| GET | `/auth/me` | any user |
| GET | `/products/`, `/products/{id}` | any user |
| POST | `/products/` | admin, manager |
| PATCH / DELETE | `/products/{id}` | admin, manager |
| GET | `/users/` | admin |
| PATCH | `/users/{id}/role` | admin, body `{"role": "manager"}` |

## Tests

```bash
cd backend
pip install -r requirements-dev.txt
ruff check . && pytest
```

Tests use a temporary SQLite database and cover registration, hashing, login, expired/forged tokens and tokens missing `exp`/`sub`, login timing equalization, the role matrix above, product CRUD, validation, CORS and the admin CLI. CI runs them on Python 3.11 and 3.12, runs `pip-audit` against the pinned requirements and builds the Docker image.

## Design decisions

- **Roles as a column, checked by a dependency.** `require_role(...)` is a FastAPI dependency, so each route states its permission in its signature.
- **No public path to elevated roles.** Registration always creates `staff`; the first admin comes from `create_admin.py`, after which admins promote users via the API.
- **Header bearer tokens, not cookies.** Avoids CSRF and lets CORS run without credentials.
- **SQLite by default.** Zero setup for a demo; `DATABASE_URL` accepts any SQLAlchemy URL.

## Security

- Passwords are hashed with bcrypt (passwords over 72 bytes are rejected instead of silently truncated).
- Login for an unknown username still runs one bcrypt check against a dummy hash, so response time does not reveal which usernames exist.
- Tokens are HS256 JWTs; `exp` and `sub` are required claims. The signing key only comes from the environment (32+ chars or the app refuses to start).
- Public registration cannot choose a role.
- CORS is restricted to configured origins and does not allow credentials (the token travels in the `Authorization` header).
- The Docker image runs as a non-root user; runtime and dev dependencies are separate, pinned files.
- No rate limiting on `/auth/login` yet (see below).

## Limitations / next steps

- Tables are created with `create_all` on startup; there are no Alembic migrations.
- No refresh tokens, token revocation or login rate limiting; the frontend stores the token in `localStorage`.
- Products only have a name and a quantity: no locations, SKUs, stock movements or audit history.
- The React client is a bare login page and a read-only dashboard, has no tests, and is not built in CI.

## License

MIT, see [LICENSE](LICENSE).
