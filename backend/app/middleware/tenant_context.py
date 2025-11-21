"""
OMEGA Core v3.0 - Tenant Context Middleware
"""
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from app.config import get_settings

settings = get_settings()


class TenantContextMiddleware(BaseHTTPMiddleware):
    """Middleware to inject tenant context from session/JWT"""
    
    async def dispatch(self, request: Request, call_next):
        # Extract tenant_id from JWT or session
        # For now, use default tenant from config
        # TODO: Extract from JWT token in Authorization header
        tenant_id = settings.default_tenant_id
        
        # Set tenant context
        request.state.tenant_id = tenant_id
        request.state.user_id = None  # TODO: Extract from JWT
        request.state.user_role = None  # TODO: Extract from JWT
        
        response = await call_next(request)
        return response

