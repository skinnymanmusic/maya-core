"""
OMEGA Core v3.0 - Retry Queue Service
Retry queue management for failed email processing
"""
import uuid
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta, timezone
from app.database import get_cursor
from app.services.audit_service import get_audit_service
from app.config import get_settings

settings = get_settings()


class RetryQueueService:
    """Retry queue management"""
    
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.audit = get_audit_service(tenant_id)
    
    def enqueue_retry(
        self,
        email_id: str,
        gmail_message_id: str,
        account_email: str,
        error_message: Optional[str] = None,
        max_retries: int = 3,
        trace_id: Optional[str] = None
    ) -> Optional[str]:
        """
        Enqueue email for retry
        
        Args:
            email_id: Email ID (UUID string)
            gmail_message_id: Gmail message ID
            account_email: Account email
            error_message: Error message
            max_retries: Maximum retry attempts
            trace_id: Request trace ID
            
        Returns:
            Retry queue item ID or None
        """
        try:
            retry_id = str(uuid.uuid4())
            scheduled_at = datetime.now(timezone.utc) + timedelta(minutes=2)  # Initial delay: 2 minutes
            
            with get_cursor(tenant_id=self.tenant_id) as cur:
                cur.execute(
                    """
                    INSERT INTO email_retry_queue (
                        id, tenant_id, email_id, gmail_message_id, account_email,
                        retry_count, max_retries, status, error_message, scheduled_at, created_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        retry_id,
                        self.tenant_id,
                        email_id,
                        gmail_message_id,
                        account_email,
                        0,
                        max_retries,
                        'pending',
                        error_message[:1024] if error_message else None,
                        scheduled_at,
                        datetime.now(timezone.utc),
                    )
                )
            
            self.audit.log_event(
                action="retry_queue.enqueued",
                resource_type="email_retry_queue",
                resource_id=retry_id,
                metadata={
                    "email_id": email_id,
                    "gmail_message_id": gmail_message_id,
                    "error_message": error_message,
                },
                trace_id=trace_id
            )
            
            return retry_id
        except Exception as e:
            self.audit.log_event(
                action="retry_queue.enqueue.error",
                resource_type="email_retry_queue",
                metadata={"error": str(e), "email_id": email_id},
                trace_id=trace_id
            )
            return None
    
    def get_pending_items(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get pending retry items
        
        Args:
            limit: Maximum number of items to return
            
        Returns:
            List of pending retry items
        """
        try:
            with get_cursor(tenant_id=self.tenant_id) as cur:
                cur.execute(
                    """
                    SELECT id::text, email_id::text, gmail_message_id, account_email,
                           retry_count, max_retries, error_message, scheduled_at
                    FROM email_retry_queue
                    WHERE tenant_id = %s
                      AND status = 'pending'
                      AND scheduled_at <= now()
                    ORDER BY scheduled_at ASC
                    LIMIT %s
                    """,
                    (self.tenant_id, limit)
                )
                rows = cur.fetchall()
                return [
                    {
                        "id": row[0],
                        "email_id": row[1],
                        "gmail_message_id": row[2],
                        "account_email": row[3],
                        "retry_count": row[4],
                        "max_retries": row[5],
                        "error_message": row[6],
                        "scheduled_at": row[7],
                    }
                    for row in rows
                ]
        except Exception:
            return []
    
    def mark_completed(self, retry_id: str, trace_id: Optional[str] = None) -> bool:
        """Mark retry item as completed"""
        try:
            with get_cursor(tenant_id=self.tenant_id) as cur:
                cur.execute(
                    """
                    UPDATE email_retry_queue
                    SET status = 'completed',
                        completed_at = now(),
                        updated_at = now()
                    WHERE id = %s AND tenant_id = %s
                    """,
                    (retry_id, self.tenant_id)
                )
                return cur.rowcount > 0
        except Exception:
            return False
    
    def mark_failed(self, retry_id: str, error_message: str, trace_id: Optional[str] = None) -> bool:
        """Mark retry item as failed"""
        try:
            with get_cursor(tenant_id=self.tenant_id) as cur:
                cur.execute(
                    """
                    UPDATE email_retry_queue
                    SET status = 'failed',
                        error_message = %s,
                        updated_at = now()
                    WHERE id = %s AND tenant_id = %s
                    """,
                    (error_message[:1024], retry_id, self.tenant_id)
                )
                return cur.rowcount > 0
        except Exception:
            return False
    
    def increment_retry(self, retry_id: str, current_retry_count: int, max_retries: int) -> bool:
        """
        Increment retry count and reschedule
        
        Args:
            retry_id: Retry queue item ID
            current_retry_count: Current retry count
            max_retries: Maximum retries
            
        Returns:
            True if rescheduled, False if max retries reached
        """
        if current_retry_count + 1 >= max_retries:
            # Mark as failed
            self.mark_failed(retry_id, f"Max retries reached ({max_retries})")
            return False
        
        try:
            # Exponential backoff: 2^retry_count minutes (up to 32 minutes)
            delay_minutes = min(2 ** (current_retry_count + 1), 32)
            scheduled_at = datetime.now(timezone.utc) + timedelta(minutes=delay_minutes)
            
            with get_cursor(tenant_id=self.tenant_id) as cur:
                cur.execute(
                    """
                    UPDATE email_retry_queue
                    SET retry_count = retry_count + 1,
                        status = 'pending',
                        scheduled_at = %s,
                        updated_at = now()
                    WHERE id = %s AND tenant_id = %s
                    """,
                    (scheduled_at, retry_id, self.tenant_id)
                )
                return cur.rowcount > 0
        except Exception:
            return False


def get_retry_queue_service(tenant_id: Optional[str] = None) -> RetryQueueService:
    """Get retry queue service instance"""
    tenant_id = tenant_id or settings.default_tenant_id
    return RetryQueueService(tenant_id=tenant_id)

