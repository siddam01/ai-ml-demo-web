# RentFlow Backend (FastAPI)

## Quick start (no Docker, no local Postgres)

1. Create free DB on [Neon](https://neon.tech).
2. Configure env:

```powershell
copy .env.example .env
# Set DATABASE_URL (Neon) and JWT_SECRET_KEY
```

3. Install, migrate, run:

```powershell
py -m pip install -r requirements.txt
# Local Postgres only (first time):
.\scripts\create-db.ps1
.\scripts\migrate.ps1
py -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Scripts: `.\scripts\create-db.ps1`, `.\scripts\migrate.ps1`, `.\scripts\dev.ps1`

- Swagger: http://127.0.0.1:8000/api/v1/docs

## Troubleshooting

### Browser shows `ERR_CONNECTION_REFUSED`

That means no process is listening on the port.

1. Start the API:

```powershell
py -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

2. If port 8000 is already in use, find and stop it:

```powershell
netstat -ano | findstr ":8000"
taskkill /PID <pid> /F
```

## Tests

Run:

```powershell
py -m pytest -q
```

This runs an in-process ASGI smoke test (no server required).

## Screenshot checklist (for docs)

Capture these after a successful run:

- Swagger UI: `/api/v1/docs`
- `POST /api/v1/auth/register` success response
- `POST /api/v1/auth/login` token response
- Create property/unit/tenant/payment success responses
- `GET /api/v1/reports/pending-dues` response

## Features

- Async FastAPI + SQLAlchemy (PostgreSQL)
- Alembic migrations
- JWT auth (register, login, refresh)
- Properties, units, tenants, payments, reports
- Clean architecture: routes → services → repositories

## Windows

psycopg async needs `WindowsSelectorEventLoopPolicy` — set in `alembic/env.py` and `app/main.py`.

## Docker (optional)

If Docker Desktop is allowed:

```bash
docker compose up --build
docker compose exec api alembic upgrade head
```

Use `DATABASE_URL` with host `db` in `.env` for compose only.

## Deploy

See repo root `DEPLOYMENT.md`.
