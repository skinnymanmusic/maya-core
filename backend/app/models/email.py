"""
OMEGA Core v3.0 - Email Data Models
"""
from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class EmailBase(BaseModel):
    """Base email model"""
    gmail_message_id: str
    gmail_thread_id: str
    account_email: str
    sender_email: str
    sender_name: str
    subject: str
    body: str
    received_at: datetime


class EmailCreate(EmailBase):
    """Email creation model"""
    pass


class Email(EmailBase):
    """Full email model with ID and metadata"""
    id: str
    tenant_id: str
    processed: bool = False
    processed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class EmailResponse(BaseModel):
    """Email response model for API"""
    id: str
    tenant_id: str
    gmail_message_id: str
    gmail_thread_id: str
    account_email: str
    sender_email: str
    sender_name: str
    subject: str
    body: str
    received_at: datetime
    processed: bool
    processed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

