"""
Bookings Router
API endpoints for managing bookings
"""
from fastapi import APIRouter, Request, HTTPException, Query
from typing import Optional, List
from pydantic import BaseModel
from app.database import get_cursor
from app.services.audit_service import get_audit_service
from app.config import get_settings
from app.routers.auth import get_current_user

settings = get_settings()
router = APIRouter(prefix="/api/bookings", tags=["bookings"])


class BookingResponse(BaseModel):
    booking_id: str
    tenant_id: str
    client_email: Optional[str]
    service_description: Optional[str]
    event_date: Optional[str]
    event_location: Optional[str]
    payment_status: str
    payment_amount: Optional[float]
    stripe_payment_link_id: Optional[str]
    created_at: str
    updated_at: str


@router.get("/", response_model=List[BookingResponse])
async def list_bookings(
    request: Request,
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
    payment_status: Optional[str] = Query(None, description="Filter by payment status")
):
    """
    List bookings for the current tenant
    """
    # Get current user (authenticated)
    user = await get_current_user(request)
    tenant_id = user.get("tenant_id") or settings.default_tenant_id
    
    # Build query
    query = """
        SELECT 
            booking_id, tenant_id, client_email, service_description,
            event_date, event_location, payment_status, payment_amount,
            stripe_payment_link_id, created_at, updated_at
        FROM bookings
        WHERE tenant_id = %s
    """
    params = [tenant_id]
    
    if payment_status:
        query += " AND payment_status = %s"
        params.append(payment_status)
    
    query += " ORDER BY created_at DESC LIMIT %s OFFSET %s"
    params.extend([limit, offset])
    
    # Execute query
    with get_cursor(tenant_id=tenant_id) as cursor:
        cursor.execute(query, params)
        rows = cursor.fetchall()
        
        bookings = []
        for row in rows:
            bookings.append({
                "booking_id": row["booking_id"],
                "tenant_id": str(row["tenant_id"]),
                "client_email": row["client_email"],
                "service_description": row["service_description"],
                "event_date": row["event_date"].isoformat() if row["event_date"] else None,
                "event_location": row["event_location"],
                "payment_status": row["payment_status"],
                "payment_amount": float(row["payment_amount"]) if row["payment_amount"] else None,
                "stripe_payment_link_id": row["stripe_payment_link_id"],
                "created_at": row["created_at"].isoformat() if row["created_at"] else "",
                "updated_at": row["updated_at"].isoformat() if row["updated_at"] else "",
            })
    
    # Log audit event
    audit = get_audit_service(tenant_id)
    audit.log_event(
        action="bookings.listed",
        resource_type="booking",
        metadata={"count": len(bookings), "filters": {"payment_status": payment_status}},
        trace_id=getattr(request.state, "trace_id", None)
    )
    
    return bookings


@router.get("/{booking_id}", response_model=BookingResponse)
async def get_booking(
    request: Request,
    booking_id: str
):
    """
    Get a specific booking by ID
    """
    # Get current user
    user = await get_current_user(request)
    tenant_id = user.get("tenant_id") or settings.default_tenant_id
    
    # Query booking
    with get_cursor(tenant_id=tenant_id) as cursor:
        cursor.execute("""
            SELECT 
                booking_id, tenant_id, client_email, service_description,
                event_date, event_location, payment_status, payment_amount,
                stripe_payment_link_id, created_at, updated_at
            FROM bookings
            WHERE booking_id = %s AND tenant_id = %s
        """, (booking_id, tenant_id))
        row = cursor.fetchone()
        
        if not row:
            raise HTTPException(status_code=404, detail="Booking not found")
        
        booking = {
            "booking_id": row["booking_id"],
            "tenant_id": str(row["tenant_id"]),
            "client_email": row["client_email"],
            "service_description": row["service_description"],
            "event_date": row["event_date"].isoformat() if row["event_date"] else None,
            "event_location": row["event_location"],
            "payment_status": row["payment_status"],
            "payment_amount": float(row["payment_amount"]) if row["payment_amount"] else None,
            "stripe_payment_link_id": row["stripe_payment_link_id"],
            "created_at": row["created_at"].isoformat() if row["created_at"] else "",
            "updated_at": row["updated_at"].isoformat() if row["updated_at"] else "",
        }
    
    # Log audit event
    audit = get_audit_service(tenant_id)
    audit.log_event(
        action="booking.retrieved",
        resource_type="booking",
        resource_id=booking_id,
        trace_id=getattr(request.state, "trace_id", None)
    )
    
    return booking

