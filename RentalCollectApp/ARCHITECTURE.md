# Architecture

## MVP stack (free tier, no Docker on dev PC)

| Layer | Technology |
|-------|------------|
| Mobile | Flutter (Android) |
| API | FastAPI, prefix `/api/v1` |
| Database | PostgreSQL (Neon / Supabase free tier) |
| Auth (MVP) | JWT register / login / refresh |
| Auth (later) | Mobile OTP |
| Hosting | Render free web service |
| Local dev | Python + uvicorn; cloud DB URL in `.env` |

## Domain model

Owner → Property → Unit → Tenant → Payment

UUID keys, timestamps, soft delete on core entities.

## Backend layout

```
backend/app/
  routes/        → HTTP
  services/      → business logic
  repositories/  → data access
  models/        → SQLAlchemy
  schemas/       → Pydantic v2
```

## Feature status

| Feature | Status |
|---------|--------|
| Properties & units | Done |
| Tenants | Done |
| Payments | Done |
| Reports (dues, collection) | Done (MVP) |
| WhatsApp reminders | Planned |
| PDF receipts | Planned |

See `API_SPEC.md` and `DEPLOYMENT.md`.
