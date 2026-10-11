# Warehouse Management System

[![CI](https://github.com/akincenk/warehouse-management-system/actions/workflows/ci.yml/badge.svg)](https://github.com/akincenk/warehouse-management-system/actions/workflows/ci.yml)

A small inventory app: a FastAPI + SQLAlchemy REST API with JWT authentication and role-based access, plus a minimal React login/dashboard client.

## What it does

- Users register (always as `staff`) and log in with the OAuth2 password flow to get a short-lived JWT.
- Authenticated users can create, list, view and update products (name + quantity).
- Only `admin` and `manager` users can delete products.
- Only `admin` users can list users and change a user's role (`admin`, `manager`, `staff`).
- The first admin is created from the command line (`create_admin.py`), not through the public API.

## Stack

- **Backend:** Python 3.11+, FastAPI, SQLAlchemy 2, Pydantic 2, PyJWT, bcrypt. SQLite by default (any SQLAlchemy URL via `DATABASE_URL`).
- **Frontend:** React 18 (Create React App), React Router, Axios.
- **Tooling:** pytest, ruff, GitHub Actions.

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
| GET / POST | `/products/` | any user |
| GET / PATCH | `/products/{id}` | any user |
| DELETE | `/products/{id}` | admin, manager |
| GET | `/users/` | admin |
| PATCH | `/users/{id}/role` | admin, body `{"role": "manager"}` |

## Tests

```bash
cd backend
pip install -r requirements-dev.txt
ruff check . && pytest
```

Tests use a temporary SQLite database and cover registration, hashing, login, expired/forged tokens, role checks, product CRUD, validation, CORS and the admin CLI. CI runs them on Python 3.11 and 3.12.

## Security notes

- Passwords are hashed with bcrypt (passwords over 72 bytes are rejected instead of silently truncated).
- Tokens are HS256 JWTs with an expiry; the signing key only comes from the environment.
- Public registration cannot choose a role.
- CORS is restricted to configured origins and does not allow credentials (the token travels in the `Authorization` header).

## Limitations / next steps

- Tables are created with `create_all` on startup; there are no Alembic migrations.
- No refresh tokens or token revocation; the frontend stores the token in `localStorage`.
- Products only have a name and a quantity: no locations, SKUs, stock movements or audit history.
- The React client is a bare login page and a read-only dashboard, has no tests, and is not built in CI.

## License

MIT, see [LICENSE](LICENSE).
