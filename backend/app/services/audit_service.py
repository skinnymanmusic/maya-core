"""
OMEGA Core v3.0 - Audit Logging Service
Comprehensive audit trail with automatic token redaction and guardian integration
"""
import uuid
from datetime import datetime, timezone
from typing import Optional, Dict, Any
from app.database import get_cursor
from app.middleware.security import redact_tokens
from app.config import get_settings

settings = get_settings()

# Guardian manager cache (per tenant, to avoid circular imports)
_guardian_managers: Dict[str, Any] = {}


def _get_guardian_manager(tenant_id: str):
    """Lazy-load guardian manager to avoid circular imports"""
    global _guardian_managers
    if tenant_id not in _guardian_managers:
        try:
            from app.guardians.guardian_manager import get_guardian_manager
            _guardian_managers[tenant_id] = get_guardian_manager(tenant_id)
        except Exception:
            # Fail-open: if guardians not available, continue without them
            _guardian_managers[tenant_id] = None
    return _guardian_managers.get(tenant_id)


class AuditService:
    """Comprehensive audit logging service"""
    
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
    
    def log_event(
        self,
        action: str,
        resource_type: str,
        resource_id: Optional[str] = None,
        user_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None,
        trace_id: Optional[str] = None,
    ) -> str:
        """
        Log an audit event to the database
        
        Args:
            action: Action name (e.g., "email.processed", "calendar.event.created")
            resource_type: Resource type (e.g., "email", "calendar", "client")
            resource_id: Resource ID (UUID string)
            user_id: User ID (UUID string)
            metadata: Additional metadata (automatically redacted)
            ip_address: Client IP address
            user_agent: Client user agent
            trace_id: Request trace ID
            
        Returns:
            Audit log entry ID
        """
        log_id = str(uuid.uuid4())
        metadata_redacted = redact_tokens(metadata or {})
        
        try:
            with get_cursor(tenant_id=self.tenant_id) as cur:
                cur.execute(
                    """
                    INSERT INTO audit_log (
                        id, tenant_id, action, resource_type, resource_id,
                        user_id, metadata, ip_address, user_agent, trace_id, created_at
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
                    )
                    """,
                    (
                        log_id,
                        self.tenant_id,
                        action,
                        resource_type,
                        resource_id,
                        user_id,
                        metadata_redacted,
                        ip_address,
                        user_agent,
                        trace_id,
                        datetime.now(timezone.utc),
                    )
                )
            
            # Emit to guardian manager (non-blocking, fail-open)
            try:
                guardian_mgr = _get_guardian_manager(self.tenant_id)
                if guardian_mgr:
                    guardian_mgr.receive_event({
                        "action": action,
                        "resource_type": resource_type,
                        "resource_id": resource_id,
                        "metadata": metadata_redacted,
                        "trace_id": trace_id,
                        "level": "INFO",
                        "service": resource_type,
                    })
            except Exception:
                # Fail-open: guardian emission failures don't affect audit logging
                pass
            
            return log_id
        except Exception as e:
            # Fail-open: log errors but don't crash
            print(f"[AUDIT ERROR] Failed to log event {action}: {e}")
            return log_id
    
    def log_safety_event(
        self,
        action: str,
        context: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Log a safety event (for Aegis integration)
        
        Args:
            action: Safety action (e.g., "anomaly.detected", "rate_limit.spike")
            context: Context description
            metadata: Additional metadata
            
        Returns:
            Audit log entry ID
        """
        return self.log_event(
            action=action,
            resource_type="safety",
            metadata={
                "context": context,
                **(metadata or {})
            }
        )


def get_audit_service(tenant_id: Optional[str] = None) -> AuditService:
    """Get audit service instance"""
    tenant_id = tenant_id or settings.default_tenant_id
    return AuditService(tenant_id=tenant_id)

