"""
OMEGA Core v3.0 - Client Data Models
"""
from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class ClientBase(BaseModel):
    """Base client model"""
    name: str
    email: EmailStr
    phone: Optional[str] = None
    company: Optional[str] = None
    notes: Optional[str] = None


class ClientCreate(ClientBase):
    """Client creation model"""
    pass


class ClientUpdate(BaseModel):
    """Client update model (all fields optional)"""
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    company: Optional[str] = None
    notes: Optional[str] = None


class Client(ClientBase):
    """Full client model with ID and metadata"""
    id: str
    tenant_id: str
    email_hash: str
    last_contact_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ClientResponse(BaseModel):
    """Client response model for API (decrypted)"""
    id: str
    tenant_id: str
    name: str
    email_hash: str
    last_contact_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

