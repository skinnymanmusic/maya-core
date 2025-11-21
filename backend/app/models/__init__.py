"""
OMEGA Core v3.0 - Data Models
Pydantic models for type safety and validation
"""
from app.models.email import Email, EmailCreate, EmailResponse
from app.models.client import Client, ClientCreate, ClientUpdate, ClientResponse
from app.models.calendar import CalendarEvent, CalendarEventCreate, CalendarEventResponse
from app.models.user import User, UserCreate, UserResponse
from app.models.archivus import ArchivusThread, ArchivusMemory, ArchivusSystemNote

__all__ = [
    "Email",
    "EmailCreate",
    "EmailResponse",
    "Client",
    "ClientCreate",
    "ClientUpdate",
    "ClientResponse",
    "CalendarEvent",
    "CalendarEventCreate",
    "CalendarEventResponse",
    "User",
    "UserCreate",
    "UserResponse",
    "ArchivusThread",
    "ArchivusMemory",
    "ArchivusSystemNote",
]

