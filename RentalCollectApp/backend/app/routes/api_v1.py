from __future__ import annotations

from fastapi import APIRouter

from app.routes.auth import router as auth_router
from app.routes.payments import router as payments_router
from app.routes.properties import router as properties_router
from app.routes.reports import router as reports_router
from app.routes.tenants import router as tenants_router


router = APIRouter()

router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(properties_router, prefix="/properties", tags=["properties"])
router.include_router(tenants_router, prefix="/tenants", tags=["tenants"])
router.include_router(payments_router, prefix="/payments", tags=["payments"])
router.include_router(reports_router, prefix="/reports", tags=["reports"])

