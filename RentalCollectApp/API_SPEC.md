# API Specification (v1)

Base: `/api/v1`  
Auth header: `Authorization: Bearer <access_token>`

## Health

| Method | Path | Auth |
|--------|------|------|
| GET | `/health` | No |

## Auth

| Method | Path | Body |
|--------|------|------|
| POST | `/auth/register` | JSON: `name`, `mobile`, `password` |
| POST | `/auth/login` | Form: `username` (= mobile), `password` |
| POST | `/auth/refresh` | JSON: `refresh_token` |

## Properties

| Method | Path |
|--------|------|
| GET | `/properties` |
| POST | `/properties` |
| PATCH | `/properties/{property_id}` |
| DELETE | `/properties/{property_id}` |
| GET | `/properties/{property_id}/units` |
| POST | `/properties/{property_id}/units` |

## Tenants

| Method | Path | Notes |
|--------|------|-------|
| GET | `/tenants?unit_id={uuid}` | Required query |
| POST | `/tenants` | |
| PATCH | `/tenants/{tenant_id}` | |
| DELETE | `/tenants/{tenant_id}` | |

## Payments

| Method | Path | Notes |
|--------|------|-------|
| GET | `/payments?tenant_id={uuid}` | |
| POST | `/payments` | |

## Reports

| Method | Path | Query |
|--------|------|-------|
| GET | `/reports/collection-summary` | `from_date`, `to_date` |
| GET | `/reports/pending-dues` | `as_of` |

Swagger: `/api/v1/docs`
