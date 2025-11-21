"""
OMEGA Core v3.0 - Security Middleware
"""
import uuid
import re
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response


def redact_tokens(data: dict) -> dict:
    """Redact tokens and sensitive data from metadata"""
    redacted = data.copy()
    sensitive_keys = [
        "token", "password", "secret", "key", "api_key",
        "access_token", "refresh_token", "authorization"
    ]
    
    for key in list(redacted.keys()):
        key_lower = key.lower()
        if any(sensitive in key_lower for sensitive in sensitive_keys):
            redacted[key] = "[REDACTED]"
        elif isinstance(redacted[key], dict):
            redacted[key] = redact_tokens(redacted[key])
        elif isinstance(redacted[key], str) and len(redacted[key]) > 50:
            # Redact long strings that might be tokens
            if re.search(r'[A-Za-z0-9_-]{32,}', redacted[key]):
                redacted[key] = "[REDACTED]"
    
    return redacted


class SecurityMiddleware(BaseHTTPMiddleware):
    """Security middleware for request tracing and headers"""
    
    async def dispatch(self, request: Request, call_next):
        # Generate trace ID
        trace_id = str(uuid.uuid4())
        request.state.trace_id = trace_id
        
        # Add security headers
        response: Response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        response.headers["X-Trace-ID"] = trace_id
        
        return response

