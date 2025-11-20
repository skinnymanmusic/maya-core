"""
OMEGA Core v3.0 - Unsafe Threads Router
Admin-only API for viewing and managing unsafe threads tagged by Sentra Safety AI
"""
from __future__ import annotations

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.services.auth_service import get_current_admin_user, User

router = APIRouter(prefix="/api/unsafe-threads", tags=["unsafe-threads"])

class UnsafeThread(BaseModel):
    id: str
    thread_id: str
    reason: str
    violation_type: str
    severity: str
    metadata: dict | None = None
    created_at: str

class UnsafeThreadList(BaseModel):
    items: List[UnsafeThread]
    total: int
    limit: int
    offset: int

@router.get("/", response_model=UnsafeThreadList)
async def list_unsafe_threads(
    limit: int = Query(50, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    severity: str | None = Query(None),
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_admin_user),
):
    """
    Admin-only listing of unsafe threads tagged by Sentra.
    No UI yet; this powers a future frontend.
    """
    filters = []
    params: dict = {"limit": limit, "offset": offset}
    
    if severity:
        filters.append("severity = :severity")
        params["severity"] = severity
    
    where_clause = ""
    if filters:
        where_clause = "WHERE " + " AND ".join(filters)
    
    query = text(
        f"""
        SELECT id::text,
               thread_id,
               reason,
               violation_type,
               severity,
               metadata,
               created_at::text
        FROM unsafe_threads
        {where_clause}
        ORDER BY created_at DESC
        LIMIT :limit OFFSET :offset
        """
    )
    
    count_query = text(
        f"""
        SELECT COUNT(*)::int
        FROM unsafe_threads
        {where_clause}
        """
    )
    
    res = await db.execute(query, params)
    rows = res.mappings().all()
    
    count_res = await db.execute(count_query, params)
    total = int(count_res.scalar() or 0)
    
    items = [
        UnsafeThread(
            id=row["id"],
            thread_id=row["thread_id"],
            reason=row["reason"],
            violation_type=row["violation_type"],
            severity=row["severity"],
            metadata=row["metadata"],
            created_at=row["created_at"],
        )
        for row in rows
    ]
    
    return UnsafeThreadList(
        items=items,
        total=total,
        limit=limit,
        offset=offset,
    )

@router.delete("/{thread_id}", status_code=status.HTTP_204_NO_CONTENT)
async def clear_unsafe_thread(
    thread_id: str,
    db: AsyncSession = Depends(get_async_session),
    current_user: User = Depends(get_current_admin_user),
):
    """
    Admin-only: remove an unsafe thread tag (e.g., after human review).
    """
    q = text(
        """
        DELETE FROM unsafe_threads
        WHERE thread_id = :thread_id
        """
    )
    
    res = await db.execute(q, {"thread_id": thread_id})
    
    if res.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unsafe thread not found",
        )
    
    await db.commit()

