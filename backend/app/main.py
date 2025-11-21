"""
OMEGA Core v3.0 - FastAPI Application Entry Point
"""
import time
import uuid
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.config import get_settings
from app.middleware.security import SecurityMiddleware
from app.middleware.tenant_context import TenantContextMiddleware
from app.routers import gmail, calendar, health, auth, clients, agents, metrics, unsafe_threads, stripe, sms, bookings
from app.database import init_db_pool, close_db_pool

settings = get_settings()

# Rate limiter
limiter = Limiter(key_func=get_remote_address)

# FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    debug=settings.debug,
    docs_url="/docs" if settings.debug else None,
    redoc_url="/redoc" if settings.debug else None,
)

# Add rate limiter
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    init_db_pool()
    yield
    # Shutdown
    close_db_pool()


app.router.lifespan_context = lifespan

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://maya-ai-production.up.railway.app",
        "https://maya-ai-staging.up.railway.app",
        "http://localhost:3000",
        "http://localhost:8000",
    ] if not settings.debug else ["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
    allow_headers=["*"],
)

# Security middleware
app.add_middleware(SecurityMiddleware)

# Tenant context middleware
app.add_middleware(TenantContextMiddleware)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler with audit logging"""
    trace_id = getattr(request.state, "trace_id", str(uuid.uuid4()))
    error_message = str(exc) if settings.debug else "Internal server error"
    
    # Log error (would use audit service here)
    print(f"[ERROR] {trace_id}: {error_message}")
    
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": error_message,
            "trace_id": trace_id,
            "timestamp": time.time(),
        }
    )

# Include routers
app.include_router(health.router)
app.include_router(auth.router)
app.include_router(gmail.router)
app.include_router(calendar.router)
app.include_router(clients.router)
app.include_router(agents.router)
app.include_router(metrics.router)
app.include_router(unsafe_threads.router)
app.include_router(stripe.router)
app.include_router(sms.router)
app.include_router(bookings.router)

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "service": settings.app_name,
        "version": settings.app_version,
        "status": "operational"
    }

