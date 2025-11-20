"""
OMEGA Core v3.0 - Archivus Data Models
Long-term memory and pattern storage
"""
from __future__ import annotations
from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel


class ArchivusThread(BaseModel):
    """Archivus thread summary model"""
    id: str
    tenant_id: str
    gmail_thread_id: str
    summary: str
    key_points: Dict[str, Any]
    client_context: Optional[Dict[str, Any]] = None
    venue_context: Optional[Dict[str, Any]] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ArchivusMemory(BaseModel):
    """Archivus memory pattern model"""
    id: str
    tenant_id: str
    memory_type: str  # "client_profile", "venue_profile", "pattern", "configuration"
    key: str
    value: Dict[str, Any]
    confidence: float = 1.0
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ArchivusSystemNote(BaseModel):
    """Archivus system note model"""
    id: str
    tenant_id: str
    category: str  # "guardian_daemon", "safe_mode", "migration", etc.
    summary: str
    details: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True

