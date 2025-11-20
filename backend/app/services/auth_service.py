"""
OMEGA Core v3.0 - Authentication Service
JWT-based authentication with brute force protection
"""
from __future__ import annotations
import jwt
import hashlib
from datetime import datetime, timedelta, timezone
from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
from app.config import get_settings
from app.database import get_cursor
from app.services.audit_service import get_audit_service
from app.utils.password_policy import PasswordPolicyService, validate_password
from app.models.user import User as UserModel
from app.encryption import decrypt

settings = get_settings()
security = HTTPBearer()


class TokenPair(BaseModel):
    """JWT token pair response"""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


def hash_email(email: str) -> str:
    """Compute SHA256 hash of email for lookup"""
    return hashlib.sha256(email.lower().strip().encode()).hexdigest()


def authenticate_user(email: str, password: str) -> Optional[UserModel]:
    """
    Authenticate user with email and password
    
    Args:
        email: User email
        password: User password
        
    Returns:
        User object if authenticated, None otherwise
    """
    password_service = PasswordPolicyService()
    email_hash = hash_email(email)
    
    try:
        # Get user from database (using users table, not users_v4)
        with get_cursor(tenant_id=None) as cur:
            cur.execute(
                """
                SELECT id, tenant_id, email, email_hash, full_name, role, 
                       password_hash, active, locked_until, failed_login_attempts,
                       last_login, created_at, updated_at
                FROM users
                WHERE email_hash = %s
                LIMIT 1
                """,
                (email_hash,),
            )
            row = cur.fetchone()
            
            if not row:
                return None
            
            # Check if account is locked
            if row[8] and row[8] > datetime.now(timezone.utc):
                # Account is locked
                audit = get_audit_service(None)
                audit.log_event(
                    action="auth.login.locked",
                    resource_type="user",
                    metadata={"email_hash": email_hash, "locked_until": row[8].isoformat()},
                    tenant_id=None,
                )
                return None
            
            # Verify password
            if not password_service.verify_password(password, row[6]):  # password_hash
                # Increment failed attempts
                failed_attempts = (row[9] or 0) + 1
                locked_until = None
                
                if failed_attempts >= 5:
                    # Lock account for 15 minutes
                    locked_until = datetime.now(timezone.utc) + timedelta(minutes=15)
                
                cur.execute(
                    """
                    UPDATE users
                    SET failed_login_attempts = %s,
                        locked_until = %s,
                        updated_at = NOW()
                    WHERE id = %s
                    """,
                    (failed_attempts, locked_until, row[0]),
                )
                cur.connection.commit()
                
                audit = get_audit_service(None)
                audit.log_event(
                    action="auth.login.failed",
                    resource_type="user",
                    metadata={"email_hash": email_hash, "failed_attempts": failed_attempts},
                    tenant_id=None,
                )
                return None
            
            # Successful login - reset failed attempts and update last_login
            cur.execute(
                """
                UPDATE users
                SET failed_login_attempts = 0,
                    locked_until = NULL,
                    last_login = NOW(),
                    updated_at = NOW()
                WHERE id = %s
                """,
                (row[0],),
            )
            cur.connection.commit()
            
            # Return User object (decrypt email and full_name)
            return UserModel(
                id=str(row[0]),
                tenant_id=str(row[1]),
                email=decrypt(row[2]) if row[2] else "",  # Decrypted email
                email_hash=row[3],
                full_name=decrypt(row[4]) if row[4] else None,  # Decrypted full_name
                role=row[5],
                active=row[7],
                locked_until=row[8],
                failed_login_attempts=row[9] or 0,
                last_login=row[10],
                created_at=row[11],
                updated_at=row[12],
            )
    except Exception as e:
        # Fail-open: return None on error
        audit = get_audit_service(None)
        audit.log_event(
            action="auth.login.error",
            resource_type="user",
            metadata={"error": str(e), "email_hash": email_hash},
            tenant_id=None,
        )
        return None


def create_token_pair(user: UserModel) -> TokenPair:
    """
    Create JWT token pair for user
    
    Args:
        user: User object
        
    Returns:
        TokenPair with access_token and refresh_token
    """
    now = datetime.now(timezone.utc)
    
    # Access token payload
    access_payload = {
        "sub": str(user.id),
        "email": user.email,
        "tenant_id": user.tenant_id,
        "role": user.role,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(minutes=settings.jwt_access_token_expire_minutes)).timestamp()),
        "type": "access",
    }
    
    # Refresh token payload
    refresh_payload = {
        "sub": str(user.id),
        "email": user.email,
        "tenant_id": user.tenant_id,
        "iat": int(now.timestamp()),
        "exp": int((now + timedelta(days=settings.jwt_refresh_token_expire_days)).timestamp()),
        "type": "refresh",
    }
    
    # Generate tokens
    access_token = jwt.encode(access_payload, settings.jwt_secret_key, algorithm="HS256")
    refresh_token = jwt.encode(refresh_payload, settings.jwt_secret_key, algorithm="HS256")
    
    return TokenPair(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
    )


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> UserModel:
    """
    Get current user from JWT token (dependency)
    
    Args:
        credentials: HTTP Bearer token credentials
        
    Returns:
        User object
        
    Raises:
        HTTPException: If token is invalid or user not found
    """
    token = credentials.credentials
    
    try:
        # Decode token
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=["HS256"])
        
        # Validate token type
        if payload.get("type") != "access":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token type",
            )
        
        # Get user from database
        user_id = payload.get("sub")
        email_hash = hash_email(payload.get("email", ""))
        
        with get_cursor(tenant_id=None) as cur:
            cur.execute(
                """
                SELECT id, tenant_id, email, email_hash, full_name, role,
                       active, locked_until, failed_login_attempts,
                       last_login, created_at, updated_at
                FROM users
                WHERE id = %s AND email_hash = %s AND active = TRUE
                LIMIT 1
                """,
                (user_id, email_hash),
            )
            row = cur.fetchone()
            
            if not row:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="User not found or inactive",
                )
            
            return UserModel(
                id=str(row[0]),
                tenant_id=str(row[1]),
                email=decrypt(row[2]) if row[2] else "",  # Decrypted
                email_hash=row[3],
                full_name=decrypt(row[4]) if row[4] else None,  # Decrypted
                role=row[5],
                active=row[6],
                locked_until=row[7],
                failed_login_attempts=row[8] or 0,
                last_login=row[9],
                created_at=row[10],
                updated_at=row[11],
            )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication error: {str(e)}",
        )


def get_current_admin_user(
    current_user: UserModel = Depends(get_current_user),
) -> UserModel:
    """
    Get current admin user (dependency)
    
    Args:
        current_user: Current user from get_current_user
        
    Returns:
        User object (must be admin)
        
    Raises:
        HTTPException: If user is not admin
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user


# Export User model for convenience
User = UserModel

