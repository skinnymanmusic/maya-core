"""
OMEGA Core v3.0 - Gmail Router
Gmail webhook and watch subscription endpoints
"""
from typing import Dict, Any, Optional
from fastapi import APIRouter, Request, HTTPException, status, Header
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.config import get_settings
from app.services.gmail_webhook import (
    verify_jwt_token,
    process_webhook_message,
)
from app.services.gmail_service import setup_watch as gmail_setup_watch
from app.services.email_processor_v3 import EmailProcessorV3
from app.database import get_db

settings = get_settings()
router = APIRouter(prefix="/api/gmail", tags=["gmail"])
limiter = Limiter(key_func=get_remote_address)

class WatchRequest(BaseModel):
    account_email: str
    topic: str

class WatchResponse(BaseModel):
    status: str
    expiration: Optional[str] = None
    history_id: Optional[str] = None

@router.post("/webhook")
@limiter.limit("100/minute")
async def gmail_webhook(
    request: Request,
    body: Dict[str, Any],
    authorization: Optional[str] = Header(None),
):
    """
    Gmail Pub/Sub webhook endpoint with full JWT verification
    
    Security:
    - Full Google JWT verification (issuer, audience, signature, expiration)
    - SHA256 fingerprinting (replay prevention)
    - Database locking (race condition prevention)
    
    Returns:
    - 200 OK - Message processed
    - 401 Unauthorized - Invalid JWT
    - 400 Bad Request - Invalid message format
    - 409 Conflict - Replay detected or lock failed
    """
    # Get tenant_id from request state (set by middleware)
    tenant_id = getattr(request.state, "tenant_id", settings.default_tenant_id)
    trace_id = getattr(request.state, "trace_id", None)
    
    # Verify JWT token
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid Authorization header"
        )
    
    token = authorization.replace("Bearer ", "")
    is_valid, error_msg = verify_jwt_token(token, tenant_id)
    
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid JWT: {error_msg}"
        )
    
    # Process webhook message
    success, error_msg, parsed_message = process_webhook_message(
        body,
        tenant_id,
        trace_id
    )
    
    if not success:
        if "replay" in error_msg.lower() or "lock" in error_msg.lower():
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=error_msg
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg
        )
    
    # Trigger email processing (async, non-blocking)
    # This would typically be done via a background task
    # For now, we'll just return success
    # TODO: Queue email processing job
    
    return {"status": "success", "message": "Webhook processed"}


@router.post("/watch", response_model=WatchResponse)
@limiter.limit("10/minute")
async def setup_watch(
    request: Request,
    watch_request: WatchRequest,
):
    """
    Set up Gmail watch subscription
    
    Args:
        watch_request: Watch configuration
        
    Returns:
        Watch response with expiration and history_id
    """
    tenant_id = getattr(request.state, "tenant_id", settings.default_tenant_id)
    
    try:
        result = gmail_setup_watch(
            account_email=watch_request.account_email,
            topic=watch_request.topic,
            tenant_id=tenant_id
        )
        
        return WatchResponse(
            status="success",
            expiration=result.get("expiration"),
            history_id=result.get("history_id")
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to setup watch: {str(e)}"
        )

