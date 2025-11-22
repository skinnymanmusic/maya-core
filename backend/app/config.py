"""
OMEGA Core v3.0 - Configuration Management

DEPRECATED: This file is kept for backward compatibility.
Use `from app.config import get_settings` instead.
"""
# Import from the new canonical location
from app.config import get_settings, settings, Settings

__all__ = ['get_settings', 'settings', 'Settings']

