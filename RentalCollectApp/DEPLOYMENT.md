# Deployment (MVP — no Docker required)

Use this when Docker Desktop is blocked on corporate machines.

## Stack

| Layer | Service |
|-------|---------|
| Database | [Neon](https://neon.tech) or [Supabase](https://supabase.com) (free PostgreSQL) |
| API (production) | [Render](https://render.com) free web service |
| Local API | Python 3.12+ + uvicorn |

## 1. Database (Neon)

1. Create a Neon project.
2. Copy the connection string.
3. Set in `backend/.env`:

```env
DATABASE_URL=postgresql+psycopg://USER:PASSWORD@ep-xxxx.region.aws.neon.tech/neondb?sslmode=require
JWT_SECRET_KEY=<long-random-string>
```

Do **not** use host `db` outside Docker Compose.

## 2. Local development (Windows)

### Option A — Local PostgreSQL (if port 5432 is available)

```powershell
cd backend
copy .env.example .env
# DATABASE_URL=postgresql+psycopg://postgres:postgres@localhost:5432/rentflow

.\scripts\create-db.ps1
.\scripts\migrate.ps1
```

### Option B — Neon (no local Postgres)

```powershell
cd backend
copy .env.example .env
# Edit .env with Neon DATABASE_URL

py -m pip install -r requirements.txt
py -m alembic upgrade head
py -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Or: `.\scripts\migrate.ps1` then `.\scripts\dev.ps1`

- Swagger: http://127.0.0.1:8000/api/v1/docs
- Health: http://127.0.0.1:8000/api/v1/health

### Windows note

Alembic and psycopg async use `WindowsSelectorEventLoopPolicy` (configured in `alembic/env.py` and `app/main.py`).

## 3. Swagger smoke test

1. `POST /api/v1/auth/register`
2. `POST /api/v1/auth/login` (username = mobile)
3. Authorize → create property → unit → tenant → payment
4. `GET /api/v1/reports/pending-dues?as_of=2026-05-28`

### Screenshot checklist (for reporting / documentation)

- Swagger page: `http://127.0.0.1:8000/api/v1/docs`
- Successful responses for:
  - Register
  - Login (token pair)
  - Create property + unit
  - Create tenant
  - Create payment
  - Pending dues report

## 4. Render deploy

1. Web Service → GitHub repo.
2. Root directory: `RentalCollectApp/backend`
3. Build: `pip install -r requirements.txt`
4. Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Env: `DATABASE_URL`, `JWT_SECRET_KEY`, `CORS_ORIGINS`, `ENV=production`
6. Run `alembic upgrade head` once against Neon (from your PC).

## 5. Flutter base URL

| Target | URL |
|--------|-----|
| Android emulator | `http://10.0.2.2:8000/api/v1` |
| Physical device | `http://<PC-LAN-IP>:8000/api/v1` |
| Production | `https://<app>.onrender.com/api/v1` |

## Docker (optional)

Only if IT allows Docker Desktop: `docker compose up --build` in `backend/`.
