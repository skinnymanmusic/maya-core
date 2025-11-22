"""
OMEGA Core v3.0 - Calendar Router
Calendar CRUD endpoints with auto-blocking and conflict detection
"""
from typing import Optional, List
from datetime import datetime
from fastapi import APIRouter, Request, Query, HTTPException, status, Path
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.config import get_settings
from app.services.calendar_service_v3 import CalendarServiceV3

settings = get_settings()
router = APIRouter(prefix="/api/calendar", tags=["calendar"])
limiter = Limiter(key_func=get_remote_address)

# Request/Response Models
class CreateEventRequest(BaseModel):
    title: str
    start_time: str  # ISO format
    end_time: str  # ISO format
    location: Optional[str] = None
    description: Optional[str] = None
    client_id: Optional[str] = None

class AutoBlockRequest(BaseModel):
    event_date: str  # ISO format
    event_type: str
    client_name: str
    duration_hours: float
    location: Optional[str] = None
    venue: Optional[str] = None
    context: Optional[str] = None
    client_id: Optional[str] = None

class CalendarEventResponse(BaseModel):
    id: str
    title: str
    start_time: str
    end_time: str
    location: Optional[str] = None
    description: Optional[str] = None
    client_id: Optional[str] = None
    google_event_id: Optional[str] = None
    tenant_id: str
    created_at: str
    updated_at: str

class CalendarEventListResponse(BaseModel):
    status: str
    count: int
    events: List[CalendarEventResponse]

class AvailabilityResponse(BaseModel):
    available: bool
    has_conflict: bool
    conflict_count: int
    conflicts: List[dict]

def to_iso_string(dt: Optional[datetime]) -> str:
    """Convert datetime to ISO string, handling None"""
    if dt is None:
        return ""
    if isinstance(dt, str):
        return dt
    return dt.isoformat()

@router.get("/events", response_model=CalendarEventListResponse)
@limiter.limit("100/minute")
async def list_events(
    request: Request,
    start_date: Optional[str] = Query(None),
    end_date: Optional[str] = Query(None),
    limit: int = Query(100, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    """
    List calendar events with optional date range
    
    Query Parameters:
    - start_date: ISO format date (optional)
    - end_date: ISO format date (optional)
    - limit: Max results (default: 100, max: 1000)
    - offset: Pagination offset (default: 0)
    """
    tenant_id = getattr(request.state, "tenant_id", settings.default_tenant_id)
    trace_id = getattr(request.state, "trace_id", None)
    
    try:
        # Parse dates if provided
        start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00')) if start_date else None
        end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00')) if end_date else None
        
        calendar_service = CalendarServiceV3(tenant_id=tenant_id)
        events = calendar_service.list_events(
            start_date=start_dt,
            end_date=end_dt,
            limit=limit,
            offset=offset
        )
        
        event_responses = [
            CalendarEventResponse(
                id=str(row.get("id", "")),
                title=row.get("title", ""),
                start_time=to_iso_string(row.get("start_time")),
                end_time=to_iso_string(row.get("end_time")),
                location=row.get("location"),
                description=row.get("description"),
                client_id=str(row.get("client_id", "")) if row.get("client_id") else None,
                google_event_id=row.get("google_event_id"),
                tenant_id=str(row.get("tenant_id", "")),
                created_at=to_iso_string(row.get("created_at")),
                updated_at=to_iso_string(row.get("updated_at")),
            )
            for row in events
        ]
        
        return CalendarEventListResponse(
            status="success",
            count=len(event_responses),
            events=event_responses
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list events: {str(e)}"
        )


@router.post("/events")
@limiter.limit("50/minute")
async def create_event(
    request: Request,
    event_request: CreateEventRequest,
):
    """
    Create calendar event
    
    Request Body:
    - title: Event title
    - start_time: ISO format datetime
    - end_time: ISO format datetime
    - location: Optional location
    - description: Optional description
    - client_id: Optional client ID (UUID)
    """
    tenant_id = getattr(request.state, "tenant_id", settings.default_tenant_id)
    trace_id = getattr(request.state, "trace_id", None)
    
    try:
        start_dt = datetime.fromisoformat(event_request.start_time.replace('Z', '+00:00'))
        end_dt = datetime.fromisoformat(event_request.end_time.replace('Z', '+00:00'))
        
        calendar_service = CalendarServiceV3(tenant_id=tenant_id)
        result = calendar_service.create_event(
            title=event_request.title,
            start_time=start_dt,
            end_time=end_dt,
            location=event_request.location,
            description=event_request.description,
            client_id=event_request.client_id,
            trace_id=trace_id
        )
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Calendar operation blocked (Safe Mode)"
            )
        
        return {
            "status": "success",
            "event_id": result.get("id"),
            "google_event_id": result.get("google_event_id"),
            "tenant_id": tenant_id,
            "created_at": to_iso_string(result.get("created_at")),
            "updated_at": to_iso_string(result.get("updated_at")),
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid date format: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create event: {str(e)}"
        )


@router.post("/block")
@limiter.limit("50/minute")
async def auto_block(
    request: Request,
    block_request: AutoBlockRequest,
):
    """
    Auto-block time for confirmed booking
    
    Special Behavior:
    - Title format: "SME Booking — {Client Name}"
    - Color: 4 (red)
    - Includes venue, time, context in description
    - Respects tenant timezone
    - Checks for conflicts before creating
    """
    tenant_id = getattr(request.state, "tenant_id", settings.default_tenant_id)
    trace_id = getattr(request.state, "trace_id", None)
    
    try:
        event_dt = datetime.fromisoformat(block_request.event_date.replace('Z', '+00:00'))
        from datetime import timedelta
        end_dt = event_dt + timedelta(hours=block_request.duration_hours)
        
        calendar_service = CalendarServiceV3(tenant_id=tenant_id)
        result = calendar_service.auto_block_for_confirmed_gig(
            event_date=event_dt,
            event_type=block_request.event_type,
            client_name=block_request.client_name,
            duration_hours=block_request.duration_hours,
            location=block_request.location or block_request.venue,
            venue=block_request.venue,
            context=block_request.context or "Auto-blocked from email acceptance",
            client_id=block_request.client_id,
            trace_id=trace_id
        )
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Calendar operation blocked (Safe Mode)"
            )
        
        return {
            "status": "success",
            "event_id": result.get("id"),
            "google_event_id": result.get("google_event_id"),
            "tenant_id": tenant_id,
            "created_at": to_iso_string(result.get("created_at")),
            "updated_at": to_iso_string(result.get("updated_at")),
            "message": "Calendar block created"
        }
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid date format: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create block: {str(e)}"
        )


@router.get("/availability", response_model=AvailabilityResponse)
@limiter.limit("100/minute")
async def check_availability(
    request: Request,
    start_time: str = Query(..., description="ISO format datetime"),
    end_time: str = Query(..., description="ISO format datetime"),
):
    """
    Check calendar availability for time window
    
    Query Parameters:
    - start_time: ISO format datetime (required)
    - end_time: ISO format datetime (required)
    """
    tenant_id = getattr(request.state, "tenant_id", settings.default_tenant_id)
    trace_id = getattr(request.state, "trace_id", None)
    
    try:
        start_dt = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        end_dt = datetime.fromisoformat(end_time.replace('Z', '+00:00'))
        
        calendar_service = CalendarServiceV3(tenant_id=tenant_id)
        conflicts = calendar_service.check_availability(
            start_time=start_dt,
            end_time=end_dt,
            trace_id=trace_id
        )
        
        has_conflict = len(conflicts) > 0
        
        return AvailabilityResponse(
            available=not has_conflict,
            has_conflict=has_conflict,
            conflict_count=len(conflicts),
            conflicts=conflicts
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid date format: {str(e)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to check availability: {str(e)}"
        )


@router.delete("/event/{event_id}")
@limiter.limit("50/minute")
async def delete_event(
    request: Request,
    event_id: str = Path(..., description="Event ID (UUID)"),
):
    """
    Delete calendar event
    
    Path Parameters:
    - event_id: Event ID (UUID)
    """
    tenant_id = getattr(request.state, "tenant_id", settings.default_tenant_id)
    trace_id = getattr(request.state, "trace_id", None)
    
    try:
        calendar_service = CalendarServiceV3(tenant_id=tenant_id)
        success = calendar_service.delete_event(
            event_id=event_id,
            trace_id=trace_id
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )
        
        return {
            "status": "success",
            "message": "Event deleted"
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete event: {str(e)}"
        )

