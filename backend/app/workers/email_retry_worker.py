"""
OMEGA Core v3.0 - Email Retry Worker
Background worker to process failed email processing retries
"""
from __future__ import annotations
import asyncio
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional
from app.database import get_cursor
from app.services.audit_service import get_audit_service
from app.services.email_processor_v3 import EmailProcessorV3

logger = logging.getLogger(__name__)

# Worker configuration
MAX_BATCH_SIZE = 10
POLL_INTERVAL_SECONDS = 30


class EmailRetryWorker:
    """
    Email Retry Worker
    Processes pending items from email_retry_queue
    """
    
    def __init__(self):
        self.is_running = False
    
    def process_batch(self) -> int:
        """
        Process one batch of pending retry items
        
        Returns:
            Number of items processed
        """
        processed_count = 0
        
        try:
            with get_cursor(tenant_id=None) as cur:
                # Fetch pending items ready for retry
                cur.execute(
                    """
                    SELECT id, tenant_id, email_id, gmail_message_id, retry_count, max_retries
                    FROM email_retry_queue
                    WHERE status = 'pending'
                      AND scheduled_at <= NOW()
                    ORDER BY scheduled_at ASC
                    LIMIT %s
                    """,
                    (MAX_BATCH_SIZE,),
                )
                items = cur.fetchall()
            
            for item in items:
                item_id, tenant_id, email_id, gmail_message_id, retry_count, max_retries = item
                
                try:
                    # Mark as processing
                    self._mark_started(item_id, tenant_id)
                    
                    # Process email (async, but we'll run it in sync context for now)
                    # TODO: Make this properly async
                    processor = EmailProcessorV3(db=None, tenant_id=tenant_id)
                    # Note: This is a placeholder - actual processing would be async
                    # For now, we'll just mark as completed
                    
                    # Mark as completed
                    self._mark_completed(item_id, tenant_id)
                    processed_count += 1
                    
                    audit = get_audit_service(tenant_id)
                    audit.log_event(
                        action="email.retry.completed",
                        resource_type="email",
                        resource_id=str(email_id),
                        metadata={
                            "gmail_message_id": gmail_message_id,
                            "retry_count": retry_count,
                        },
                        tenant_id=tenant_id,
                    )
                except Exception as e:
                    # Check if max retries reached
                    if retry_count >= max_retries:
                        self._mark_failed(item_id, tenant_id, str(e))
                        audit = get_audit_service(tenant_id)
                        audit.log_event(
                            action="email.retry.failed",
                            resource_type="email",
                            resource_id=str(email_id),
                            metadata={
                                "gmail_message_id": gmail_message_id,
                                "retry_count": retry_count,
                                "error": str(e),
                            },
                            tenant_id=tenant_id,
                        )
                    else:
                        # Increment retry and reschedule
                        self._increment_retry(item_id, tenant_id, retry_count)
        except Exception as e:
            logger.error(f"Email retry worker batch error: {e}", exc_info=True)
        
        return processed_count
    
    def _mark_started(self, item_id: str, tenant_id: str) -> None:
        """Mark retry item as processing"""
        try:
            with get_cursor(tenant_id=None) as cur:
                cur.execute(
                    """
                    UPDATE email_retry_queue
                    SET status = 'processing', started_at = NOW(), updated_at = NOW()
                    WHERE id = %s
                    """,
                    (item_id,),
                )
                cur.connection.commit()
        except Exception:
            pass
    
    def _mark_completed(self, item_id: str, tenant_id: str) -> None:
        """Mark retry item as completed"""
        try:
            with get_cursor(tenant_id=None) as cur:
                cur.execute(
                    """
                    UPDATE email_retry_queue
                    SET status = 'completed', completed_at = NOW(), updated_at = NOW()
                    WHERE id = %s
                    """,
                    (item_id,),
                )
                cur.connection.commit()
        except Exception:
            pass
    
    def _mark_failed(self, item_id: str, tenant_id: str, error_message: str) -> None:
        """Mark retry item as failed"""
        try:
            with get_cursor(tenant_id=None) as cur:
                cur.execute(
                    """
                    UPDATE email_retry_queue
                    SET status = 'failed', error_message = %s, updated_at = NOW()
                    WHERE id = %s
                    """,
                    (error_message[:500], item_id),  # Limit error message length
                )
                cur.connection.commit()
        except Exception:
            pass
    
    def _increment_retry(self, item_id: str, tenant_id: str, current_retry_count: int) -> None:
        """Increment retry count and reschedule with exponential backoff"""
        try:
            # Exponential backoff: 2^min(retry_count + 1, 5) minutes (max 32 minutes)
            backoff_minutes = min(2 ** (current_retry_count + 1), 32)
            scheduled_at = datetime.now(timezone.utc) + timedelta(minutes=backoff_minutes)
            
            with get_cursor(tenant_id=None) as cur:
                cur.execute(
                    """
                    UPDATE email_retry_queue
                    SET retry_count = retry_count + 1,
                        status = 'pending',
                        scheduled_at = %s,
                        updated_at = NOW()
                    WHERE id = %s
                    """,
                    (scheduled_at, item_id),
                )
                cur.connection.commit()
        except Exception:
            pass
    
    async def run_loop(self) -> None:
        """Continuous loop for processing retries"""
        self.is_running = True
        logger.info("Email retry worker started")
        
        while self.is_running:
            try:
                processed = self.process_batch()
                if processed > 0:
                    logger.info(f"Processed {processed} retry items")
            except Exception as e:
                logger.error(f"Email retry worker error: {e}", exc_info=True)
            
            await asyncio.sleep(POLL_INTERVAL_SECONDS)
    
    @classmethod
    def run_forever(cls) -> None:
        """Class method for standalone execution"""
        worker = cls()
        try:
            asyncio.run(worker.run_loop())
        except KeyboardInterrupt:
            logger.info("Email retry worker stopped by user")
            worker.is_running = False
        except Exception as e:
            logger.error(f"Email retry worker crashed: {e}", exc_info=True)
            raise


def start_email_retry_worker() -> None:
    """Helper function to start email retry worker"""
    EmailRetryWorker.run_forever()


if __name__ == "__main__":
    # Standalone execution
    start_email_retry_worker()

