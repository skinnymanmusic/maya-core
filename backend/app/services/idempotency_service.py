"""
OMEGA Core v3.0 - Idempotency Service
Global idempotency layer and processor locks
"""
import uuid
from typing import Optional, Tuple
from datetime import datetime, timezone
from app.database import get_cursor
from app.services.audit_service import get_audit_service
from app.config import get_settings

settings = get_settings()


class IdempotencyService:
    """Idempotency checks and processor locks"""
    
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.audit = get_audit_service(tenant_id)
    
    def is_processed(self, gmail_message_id: str) -> bool:
        """
        Check if message has already been processed
        
        Args:
            gmail_message_id: Gmail message ID
            
        Returns:
            True if already processed, False otherwise
        """
        try:
            with get_cursor(tenant_id=self.tenant_id) as cur:
                cur.execute(
                    "SELECT 1 FROM processed_messages WHERE gmail_message_id = %s AND tenant_id = %s LIMIT 1",
                    (gmail_message_id, self.tenant_id)
                )
                return cur.fetchone() is not None
        except Exception:
            # Fail-open: if check fails, allow processing
            return False
    
    def mark_processed(self, gmail_message_id: str, trace_id: Optional[str] = None) -> None:
        """
        Mark message as processed
        
        Args:
            gmail_message_id: Gmail message ID
            trace_id: Request trace ID
        """
        try:
            with get_cursor(tenant_id=self.tenant_id) as cur:
                cur.execute(
                    """
                    INSERT INTO processed_messages (id, tenant_id, gmail_message_id, processed_at, created_at)
                    VALUES (%s, %s, %s, %s, %s)
                    ON CONFLICT (gmail_message_id) DO NOTHING
                    """,
                    (
                        str(uuid.uuid4()),
                        self.tenant_id,
                        gmail_message_id,
                        datetime.now(timezone.utc),
                        datetime.now(timezone.utc),
                    )
                )
            
            self.audit.log_event(
                action="idempotency.marked_processed",
                resource_type="email",
                resource_id=gmail_message_id,
                trace_id=trace_id
            )
        except Exception as e:
            # Fail-open: idempotency marking failure doesn't block processing
            self.audit.log_event(
                action="idempotency.mark.error",
                resource_type="email",
                metadata={"error": str(e), "gmail_message_id": gmail_message_id},
                trace_id=trace_id
            )
    
    def acquire_processor_lock(self, gmail_message_id: str) -> Tuple[bool, Optional[str]]:
        """
        Acquire processor lock on gmail_message_id
        
        Args:
            gmail_message_id: Gmail message ID
            
        Returns:
            Tuple of (lock_acquired, error_message)
        """
        try:
            # Hash message ID to get lock key
            lock_key = hash(gmail_message_id) & 0x7FFFFFFF  # Ensure positive integer
            
            with get_cursor(tenant_id=self.tenant_id) as cur:
                cur.execute("SELECT pg_try_advisory_lock(%s)", (lock_key,))
                acquired = cur.fetchone()[0]
                
                if not acquired:
                    return False, "Lock already exists (idempotency)"
                
                return True, None
        except Exception as e:
            return False, f"Lock acquisition failed: {str(e)}"
    
    def release_processor_lock(self, gmail_message_id: str) -> None:
        """
        Release processor lock
        
        Args:
            gmail_message_id: Gmail message ID
        """
        try:
            lock_key = hash(gmail_message_id) & 0x7FFFFFFF
            with get_cursor(tenant_id=self.tenant_id) as cur:
                cur.execute("SELECT pg_advisory_unlock(%s)", (lock_key,))
        except Exception:
            # Fail-open: lock release failure is logged but doesn't crash
            pass


def get_idempotency_service(tenant_id: Optional[str] = None) -> IdempotencyService:
    """Get idempotency service instance"""
    tenant_id = tenant_id or settings.default_tenant_id
    return IdempotencyService(tenant_id=tenant_id)

