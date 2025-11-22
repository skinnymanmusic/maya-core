"""
OMEGA Core v3.0 - Configuration Module
Canonical settings loader - always import from here
"""
from functools import lru_cache
from .settings import Settings


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


# Export settings instance for convenience
settings = get_settings()
