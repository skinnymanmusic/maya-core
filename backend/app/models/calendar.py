"""
OMEGA Core v3.0 - Calendar Event Data Models
"""
from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CalendarEventBase(BaseModel):
    """Base calendar event model"""
    title: str
    start_time: datetime
    end_time: datetime
    location: Optional[str] = None
    description: Optional[str] = None
    client_id: Optional[str] = None


class CalendarEventCreate(CalendarEventBase):
    """Calendar event creation model"""
    pass


class CalendarEvent(CalendarEventBase):
    """Full calendar event model with ID and metadata"""
    id: str
    tenant_id: str
    google_event_id: Optional[str] = None
    color_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class CalendarEventResponse(BaseModel):
    """Calendar event response model for API"""
    id: str
    tenant_id: str
    title: str
    start_time: datetime
    end_time: datetime
    location: Optional[str] = None
    description: Optional[str] = None
    client_id: Optional[str] = None
    google_event_id: Optional[str] = None
    color_id: Optional[int] = None
    created_at: str  # ISO string
    updated_at: str  # ISO string

