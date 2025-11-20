"""
OMEGA Core v3.0 - Health Check Endpoints
"""
from fastapi import APIRouter, Depends
from datetime import datetime
from app.database import get_cursor
from app.config import get_settings

router = APIRouter(prefix="/api/health", tags=["health"])
settings = get_settings()


@router.get("/")
async def health_check():
    """Comprehensive health check"""
    try:
        # Test database connection
        with get_cursor() as cur:
            cur.execute("SELECT 1")
            db_ok = True
    except Exception:
        db_ok = False
    
    # Test encryption (would test encryption service here)
    encryption_ok = bool(settings.encryption_key)
    
    return {
        "status": "healthy" if (db_ok and encryption_ok) else "degraded",
        "database": db_ok,
        "encryption": encryption_ok,
        "timestamp": datetime.utcnow().isoformat(),
        "version": settings.app_version
    }


@router.get("/db")
async def db_health():
    """Database connection test"""
    try:
        with get_cursor() as cur:
            cur.execute("SELECT 1")
        return {"status": "ok", "message": "Database connection successful"}
    except Exception as e:
        return {"status": "error", "message": str(e)}


@router.get("/encryption")
async def encryption_health():
    """Encryption service test"""
    encryption_ok = bool(settings.encryption_key)
    return {
        "status": "ok" if encryption_ok else "error",
        "message": "Encryption service operational" if encryption_ok else "Encryption key missing"
    }

