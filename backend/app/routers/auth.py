"""
OMEGA Core v3.0 - Authentication Router
JWT-based authentication endpoints
"""
from __future__ import annotations

import secrets
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel

from app.services.auth_service import (
    TokenPair,
    authenticate_user,
    create_token_pair,
    get_current_user,
    User,
)
from app.services.sso_service import get_sso_service
from app.services.tenant_resolution_service import get_tenant_resolution_service

router = APIRouter(prefix="/api/auth", tags=["auth"])

# v4.0 SSO Models
class SSOStartResponse(BaseModel):
    """Response for SSO start endpoint"""
    auth_url: str
    state: str


class SSOCallbackRequest(BaseModel):
    """Request for SSO callback endpoint"""
    code: str
    state: Optional[str] = None


@router.post("/login", response_model=TokenPair)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    """
    Login endpoint - authenticate user and return JWT tokens
    
    Args:
        form_data: OAuth2 password form (username=email, password)
        
    Returns:
        TokenPair with access_token and refresh_token
        
    Raises:
        HTTPException: If credentials are invalid
    """
    user = authenticate_user(
        email=form_data.username,
        password=form_data.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
        )
    
    return create_token_pair(user)


@router.post("/refresh", response_model=TokenPair)
async def refresh_token(
    refresh_token: str,
):
    """
    Refresh token endpoint
    
    TODO: In a full implementation, decode and validate refresh token, then re-issue pair.
    For now, this is not implemented.
    
    Args:
        refresh_token: Refresh token string
        
    Raises:
        HTTPException: Not implemented
    """
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED,
        detail="Refresh token flow not implemented yet",
    )


@router.get("/me", response_model=User)
async def get_me(current_user: User = Depends(get_current_user)):
    """
    Get current user information from JWT token
    
    Args:
        current_user: Current user from JWT token
        
    Returns:
        User object
    """
    return current_user


# ============================================================
# v4.0 SSO Endpoints (Google OIDC)
# ============================================================

@router.get("/google/start", response_model=SSOStartResponse)
@router.post("/google/start", response_model=SSOStartResponse)
async def google_sso_start():
    """
    Start Google OIDC authentication flow
    
    Returns:
        Authorization URL and state token
    """
    sso = get_sso_service()
    
    # Generate CSRF state token
    state = secrets.token_urlsafe(32)
    
    try:
        auth_url = sso.get_google_auth_url(state)
        return SSOStartResponse(auth_url=auth_url, state=state)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Google SSO not configured: {str(e)}"
        )


@router.get("/google/callback")
@router.post("/google/callback")
async def google_sso_callback(
    code: Optional[str] = None,
    state: Optional[str] = None,
    error: Optional[str] = None,
    request: Request = None,
):
    """
    Handle Google OIDC callback
    
    Args:
        code: Authorization code from Google
        state: CSRF state token
        error: Error from Google (if any)
        request: FastAPI request object
        
    Returns:
        Redirect to frontend with session token
    """
    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Google OAuth error: {error}"
        )
    
    # Get code from query params if not in body
    if not code and request:
        code = request.query_params.get("code")
        state = request.query_params.get("state")
    
    if not code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing authorization code"
        )
    
    sso = get_sso_service()
    
    try:
        # Exchange code for user info
        user_data = await sso.exchange_google_code(code)
        
        # Phase 3: Tenant resolution and session creation
        resolution_service = get_tenant_resolution_service()
        resolution = resolution_service.resolve_tenant_for_user(
            provider=user_data["provider"],
            sub=user_data["sub"],
            email=user_data["email"],
            name=user_data["name"],
            domain=user_data.get("domain"),
        )
        
        # Create session if single tenant
        session_id = None
        if resolution.get("tenant_id"):
            from uuid import UUID
            session_id = resolution_service.create_session(
                user_id=UUID(resolution["user_id"]),
                tenant_id=UUID(resolution["tenant_id"]),
                metadata={"provider": "GOOGLE", "ip": request.client.host if request else None},
            )
        
        return {
            "status": "success",
            "provider": "GOOGLE",
            "user": user_data,
            "resolution": resolution,
            "session_id": str(session_id) if session_id else None,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to authenticate with Google: {str(e)}"
        )


# ============================================================
# v4.0 SSO Endpoints (Microsoft OIDC)
# ============================================================

@router.get("/microsoft/start", response_model=SSOStartResponse)
@router.post("/microsoft/start", response_model=SSOStartResponse)
async def microsoft_sso_start():
    """
    Start Microsoft OIDC authentication flow
    
    Returns:
        Authorization URL and state token
    """
    sso = get_sso_service()
    
    # Generate CSRF state token
    state = secrets.token_urlsafe(32)
    
    try:
        auth_url = sso.get_microsoft_auth_url(state)
        return SSOStartResponse(auth_url=auth_url, state=state)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Microsoft SSO not configured: {str(e)}"
        )


@router.get("/microsoft/callback")
@router.post("/microsoft/callback")
async def microsoft_sso_callback(
    code: Optional[str] = None,
    state: Optional[str] = None,
    error: Optional[str] = None,
    request: Request = None,
):
    """
    Handle Microsoft OIDC callback
    
    Args:
        code: Authorization code from Microsoft
        state: CSRF state token
        error: Error from Microsoft (if any)
        request: FastAPI request object
        
    Returns:
        Redirect to frontend with session token
    """
    if error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Microsoft OAuth error: {error}"
        )
    
    # Get code from query params if not in body
    if not code and request:
        code = request.query_params.get("code")
        state = request.query_params.get("state")
    
    if not code:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing authorization code"
        )
    
    sso = get_sso_service()
    
    try:
        # Exchange code for user info
        user_data = await sso.exchange_microsoft_code(code)
        
        # Phase 3: Tenant resolution and session creation
        resolution_service = get_tenant_resolution_service()
        resolution = resolution_service.resolve_tenant_for_user(
            provider=user_data["provider"],
            sub=user_data["sub"],
            email=user_data["email"],
            name=user_data["name"],
            domain=user_data.get("domain"),
        )
        
        # Create session if single tenant
        session_id = None
        if resolution.get("tenant_id"):
            from uuid import UUID
            session_id = resolution_service.create_session(
                user_id=UUID(resolution["user_id"]),
                tenant_id=UUID(resolution["tenant_id"]),
                metadata={"provider": "MICROSOFT", "ip": request.client.host if request else None},
            )
        
        return {
            "status": "success",
            "provider": "MICROSOFT",
            "user": user_data,
            "resolution": resolution,
            "session_id": str(session_id) if session_id else None,
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to authenticate with Microsoft: {str(e)}"
        )

