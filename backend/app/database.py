"""
OMEGA Core v3.0 - Database Connection Management
"""
import os
import psycopg2
from psycopg2 import pool, sql
from psycopg2.extras import RealDictCursor
from contextlib import contextmanager
from typing import Optional, Generator
from app.config import get_settings

settings = get_settings()

# Connection pool (thread-safe)
_connection_pool: Optional[pool.ThreadedConnectionPool] = None


def init_db_pool():
    """Initialize database connection pool"""
    global _connection_pool
    if _connection_pool is None:
        _connection_pool = pool.ThreadedConnectionPool(
            minconn=2,
            maxconn=30,
            dsn=settings.database_url,
            cursor_factory=RealDictCursor
        )
    return _connection_pool


def get_db_pool():
    """Get database connection pool (initializes if needed)"""
    global _connection_pool
    if _connection_pool is None:
        init_db_pool()
    return _connection_pool


@contextmanager
def get_cursor(tenant_id: Optional[str] = None) -> Generator[RealDictCursor, None, None]:
    """
    Get database cursor with tenant context.
    
    Args:
        tenant_id: Optional tenant ID for RLS context
        
    Yields:
        RealDictCursor: Database cursor
    """
    pool = get_db_pool()
    conn = pool.getconn()
    try:
        # Set tenant context for RLS
        if tenant_id:
            with conn.cursor() as cur:
                cur.execute("SET LOCAL app.current_tenant_id = %s", (tenant_id,))
        
        cursor = conn.cursor()
        yield cursor
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        pool.putconn(conn)


def get_db():
    """Get database connection (legacy compatibility)"""
    return get_db_pool().getconn()


def close_db_pool():
    """Close all database connections"""
    global _connection_pool
    if _connection_pool:
        _connection_pool.closeall()
        _connection_pool = None


# Async session support (for routers that use AsyncSession)
try:
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
    from sqlalchemy.orm import declarative_base
    
    _async_engine = None
    _async_session_maker = None
    
    def init_async_db():
        """Initialize async database engine"""
        global _async_engine, _async_session_maker
        if _async_engine is None:
            # Convert postgresql:// to postgresql+asyncpg://
            async_url = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")
            _async_engine = create_async_engine(async_url, echo=False)
            _async_session_maker = async_sessionmaker(_async_engine, class_=AsyncSession, expire_on_commit=False)
        return _async_session_maker
    
    async def get_async_session() -> AsyncSession:
        """Get async database session (dependency)"""
        global _async_session_maker
        if _async_session_maker is None:
            init_async_db()
        async with _async_session_maker() as session:
            yield session
    
except ImportError:
    # Fallback if asyncpg not available
    async def get_async_session():
        """Fallback async session (not implemented)"""
        raise NotImplementedError("Async database sessions require asyncpg. Install with: pip install asyncpg")

