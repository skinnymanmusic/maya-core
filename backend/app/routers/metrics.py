"""
OMEGA Core v3.0 - System Metrics Router
Admin-only API for system metrics and dashboard data
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
from typing import Any, Dict

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.services.auth_service import get_current_admin_user, User

router = APIRouter(prefix="/api/metrics", tags=["metrics"])

class MetricsResponse(BaseModel):
    generated_at: str
    emails_processed_24h: int
    retry_queue_pending: int
    unsafe_threads: int
    repair_failures_24h: int
    vee_drafts_by_status: Dict[str, int] | None = None

@router.get("/", response_model=MetricsResponse)
async def get_metrics(
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_admin_user),
):
    """
    System metrics for dashboard.
    Aggregated across tenants for now.
    """
    now = datetime.now(timezone.utc)
    d24 = now - timedelta(hours=24)
    
    async def scalar(q: str, params: dict[str, Any] | None = None) -> int:
        res = await db.execute(text(q), params or {})
        return int(res.scalar() or 0)
    
    emails_24h = await scalar(
        """
        SELECT COUNT(*)::int
        FROM audit_log
        WHERE action = 'email.processed'
          AND created_at >= :since
        """,
        {"since": d24},
    )
    
    retry_pending = await scalar(
        """
        SELECT COUNT(*)::int
        FROM email_retry_queue
        WHERE status = 'pending'
        """
    )
    
    unsafe_count = await scalar(
        """
        SELECT COUNT(*)::int
        FROM unsafe_threads
        """
    )
    
    repairs_24h = await scalar(
        """
        SELECT COUNT(*)::int
        FROM repair_log
        WHERE success = FALSE
          AND created_at >= :since
        """,
        {"since": d24},
    )
    
    # Optional: Vee drafts by status
    vee_drafts = None
    try:
        vee_q = text(
            """
            SELECT status, COUNT(*)::int AS c
            FROM vee_drafts
            GROUP BY status
            """
        )
        vee_res = await db.execute(vee_q)
        vee_rows = vee_res.fetchall()
        if vee_rows:
            vee_drafts = {row[0]: int(row[1]) for row in vee_rows}
    except Exception:
        # Table might not exist yet
        pass
    
    return MetricsResponse(
        generated_at=now.isoformat(),
        emails_processed_24h=emails_24h,
        retry_queue_pending=retry_pending,
        unsafe_threads=unsafe_count,
        repair_failures_24h=repairs_24h,
        vee_drafts_by_status=vee_drafts,
    )

