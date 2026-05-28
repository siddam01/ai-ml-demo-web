from __future__ import annotations

from datetime import datetime, timedelta, timezone

from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.app_log import AppLog


class LogService:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def cleanup_older_than_days(self, days: int) -> int:
        cutoff = datetime.now(timezone.utc) - timedelta(days=days)
        stmt = delete(AppLog).where(AppLog.created_at < cutoff)
        res = await self.session.execute(stmt)
        await self.session.commit()
        return int(res.rowcount or 0)

