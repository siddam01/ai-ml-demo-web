# RentFlow Backend (FastAPI)

Production-ready FastAPI backend for a rental collection mobile app.

## Features

- Async FastAPI + async SQLAlchemy (PostgreSQL)
- Alembic migrations
- Pydantic v2 schemas + validation
- JWT auth (access + refresh), password hashing
- Clean architecture: routes → services → repositories
- Centralized exception handling, CORS + logging middleware

## Quickstart (Docker)

1. Copy env file:

```bash
cp .env.example .env
```

2. Start services:

```bash
docker compose up --build
```

3. Run migrations:

```bash
docker compose exec api alembic upgrade head
```

Open Swagger at `http://localhost:8000/docs`.

## Local (without Docker)

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
alembic upgrade head
uvicorn app.main:app --reload
```

## Auth Notes

- Register an owner via `POST /api/v1/auth/register`
- Login via `POST /api/v1/auth/login` to get tokens
- Use `Authorization: Bearer <access_token>` for protected routes
