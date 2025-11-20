"""
OMEGA Core v3.0 - User Data Models
"""
from __future__ import annotations
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Base user model"""
    email: EmailStr
    full_name: Optional[str] = None
    role: str = "user"  # "admin" | "user"


class UserCreate(UserBase):
    """User creation model"""
    password: str


class User(UserBase):
    """Full user model with ID and metadata"""
    id: str
    tenant_id: str
    email_hash: str
    active: bool = True
    locked_until: Optional[datetime] = None
    failed_login_attempts: int = 0
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserResponse(BaseModel):
    """User response model for API (no sensitive data)"""
    id: str
    tenant_id: str
    email: EmailStr
    full_name: Optional[str] = None
    role: str
    active: bool
    last_login: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

