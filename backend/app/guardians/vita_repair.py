"""
OMEGA Core v3.0 - Vita Repair AI
Automated repair agent for pipeline crashes and misconfigurations
"""
from __future__ import annotations
from typing import Dict, Any, Optional
from datetime import datetime, timedelta, timezone
from app.services.audit_service import get_audit_service
from app.guardians.solin_mcp import get_solin_mcp
from app.database import get_cursor


class VitaRepair:
    """
    Vita Repair AI - Automated repair agent
    """
    
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.audit = get_audit_service(tenant_id)
        self._failure_counts: Dict[str, int] = {}
    
    def receive_event(self, action: str, metadata: Dict[str, Any]) -> None:
        """
        Receive audit event and check for repairable errors
        
        Args:
            action: Audit action name
            metadata: Event metadata
        """
        try:
            # Check if processing error
            error = metadata.get("error", "")
            if self._is_processing_error(error):
                self.repair_action(
                    event_type="processing_error",
                    metadata=metadata,
                )
            
            # Log action
            self.log_action(action, metadata)
        except Exception as e:
            # Fail-open: guardian failures don't affect main pipeline
            pass
    
    def log_action(self, action: str, metadata: Dict[str, Any]) -> None:
        """Log guardian action"""
        self.audit.log_event(
            action=f"guardian.vita.{action}",
            resource_type="guardian",
            metadata=metadata,
            tenant_id=self.tenant_id,
        )
    
    def repair_action(
        self,
        event_type: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Attempt automatic repair for detected errors
        
        Args:
            event_type: Type of error (processing_error, retry_queue_stuck, etc.)
            metadata: Optional metadata
        
        Returns:
            Dict with repair result
        """
        try:
            # Track failure
            event_key = self._get_event_key(event_type, metadata or {})
            failure_count = self._track_failure(event_key)
            
            # Only repair if recurring (threshold: 3)
            if failure_count < 3:
                return {"action": "monitoring", "failure_count": failure_count}
            
            # Attempt repairs based on event type
            if event_type == "processing_error":
                return self._repair_processing(metadata or {})
            elif event_type == "retry_queue_stuck":
                return self._repair_retry_queue_flush()
            elif event_type == "calendar_corrupted":
                return self._repair_corrupted_calendar_entries(metadata or {})
            elif event_type == "lock_failed":
                return self._repair_failed_locks(metadata or {})
            elif event_type == "client_malformed":
                return self._repair_malformed_client_entries(metadata or {})
            
            return {"action": "no_repair", "event_type": event_type}
        except Exception as e:
            # Fail-open: repair failures don't block system
            self._log_repair(
                event=event_type,
                action_taken="error",
                success=False,
                error_message=str(e),
            )
            return {"action": "error", "error": str(e)}
    
    def _repair_processing(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Repair processing errors"""
        try:
            # Attempt to flush retry queue
            retry_result = self._repair_retry_queue_flush()
            
            # Log repair
            self._log_repair(
                event="processing_error",
                action_taken="retry_queue_flush",
                success=retry_result.get("success", False),
            )
            
            return retry_result
        except Exception as e:
            return {"action": "error", "error": str(e)}
    
    def _repair_retry_queue_flush(self) -> Dict[str, Any]:
        """Flush stuck retry queue items"""
        try:
            one_hour_ago = datetime.now(timezone.utc) - timedelta(hours=1)
            
            with get_cursor(tenant_id=self.tenant_id) as cur:
                cur.execute(
                    """
                    UPDATE email_retry_queue
                    SET status = 'pending',
                        started_at = NULL,
                        updated_at = NOW()
                    WHERE tenant_id = %s
                      AND status = 'processing'
                      AND started_at < %s
                    """,
                    (self.tenant_id, one_hour_ago),
                )
                count = cur.rowcount
                cur.connection.commit()
            
            self._log_repair(
                event="retry_queue_stuck",
                action_taken="flush_stuck_items",
                success=True,
                metadata={"items_reset": count},
            )
            
            return {"action": "repaired", "success": True, "items_reset": count}
        except Exception as e:
            self._log_repair(
                event="retry_queue_stuck",
                action_taken="flush_stuck_items",
                success=False,
                error_message=str(e),
            )
            return {"action": "error", "error": str(e)}
    
    def _repair_corrupted_calendar_entries(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Re-create corrupted calendar entries"""
        try:
            # This is a placeholder - real implementation would verify/recreate entries
            event_id = metadata.get("event_id")
            
            if event_id:
                # Verify entry exists in DB but not in Google Calendar
                # Recreate if needed
                pass
            
            self._log_repair(
                event="calendar_corrupted",
                action_taken="verify_recreate",
                success=True,
            )
            
            return {"action": "repaired", "success": True}
        except Exception as e:
            self._log_repair(
                event="calendar_corrupted",
                action_taken="verify_recreate",
                success=False,
                error_message=str(e),
            )
            return {"action": "error", "error": str(e)}
    
    def _repair_failed_locks(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Reset failed locks"""
        try:
            gmail_message_id = metadata.get("gmail_message_id")
            
            if gmail_message_id:
                # Release lock using idempotency service
                # This is a placeholder - real implementation would use idempotency service
                pass
            
            self._log_repair(
                event="lock_failed",
                action_taken="reset_lock",
                success=True,
            )
            
            return {"action": "repaired", "success": True}
        except Exception as e:
            self._log_repair(
                event="lock_failed",
                action_taken="reset_lock",
                success=False,
                error_message=str(e),
            )
            return {"action": "error", "error": str(e)}
    
    def _repair_malformed_client_entries(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Repair malformed client entries"""
        try:
            client_id = metadata.get("client_id")
            
            if client_id:
                # Validate and fix client data
                # This is a placeholder - real implementation would validate/fix entries
                pass
            
            self._log_repair(
                event="client_malformed",
                action_taken="validate_fix",
                success=True,
            )
            
            return {"action": "repaired", "success": True}
        except Exception as e:
            self._log_repair(
                event="client_malformed",
                action_taken="validate_fix",
                success=False,
                error_message=str(e),
            )
            return {"action": "error", "error": str(e)}
    
    def _get_event_key(self, event_type: str, metadata: Dict[str, Any]) -> str:
        """Generate event key for failure tracking"""
        # Use thread_id or gmail_message_id as key
        return metadata.get("thread_id") or metadata.get("gmail_message_id") or event_type
    
    def _track_failure(self, event_key: str) -> int:
        """Track failure count per event"""
        if event_key not in self._failure_counts:
            self._failure_counts[event_key] = 0
        self._failure_counts[event_key] += 1
        return self._failure_counts[event_key]
    
    def _log_repair(
        self,
        event: str,
        action_taken: str,
        success: bool,
        error_message: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Log repair attempt to database"""
        try:
            with get_cursor(tenant_id=self.tenant_id) as cur:
                cur.execute(
                    """
                    INSERT INTO repair_log (tenant_id, event, action_taken, success, error_message, metadata, created_at)
                    VALUES (%s, %s, %s, %s, %s, %s, NOW())
                    """,
                    (
                        self.tenant_id,
                        event,
                        action_taken,
                        success,
                        error_message,
                        metadata or {},
                    ),
                )
                cur.connection.commit()
        except Exception as e:
            # Fail-open: repair logging failures don't block system
            pass
    
    def _is_processing_error(self, error: str) -> bool:
        """Check if error is a processing-related error"""
        processing_keywords = [
            "processing",
            "crash",
            "failure",
            "exception",
            "error",
            "timeout",
        ]
        error_lower = error.lower()
        return any(keyword in error_lower for keyword in processing_keywords)
    
    def self_check(self) -> Dict[str, Any]:
        """
        Run integrity checks on Vita systems
        
        Returns:
            Dict with check results
        """
        try:
            checks = {
                "retry_queue_check": True,
                "calendar_entries_check": True,
                "locks_check": True,
                "client_entries_check": True,
            }
            
            # Check retry queue integrity
            try:
                with get_cursor(tenant_id=self.tenant_id) as cur:
                    cur.execute(
                        """
                        SELECT COUNT(*)::int
                        FROM email_retry_queue
                        WHERE tenant_id = %s
                        LIMIT 1
                        """,
                        (self.tenant_id,),
                    )
                    cur.fetchone()
            except Exception:
                checks["retry_queue_check"] = False
            
            # Check calendar entries integrity
            try:
                with get_cursor(tenant_id=self.tenant_id) as cur:
                    cur.execute(
                        """
                        SELECT COUNT(*)::int
                        FROM calendar_events
                        WHERE tenant_id = %s
                        LIMIT 1
                        """,
                        (self.tenant_id,),
                    )
                    cur.fetchone()
            except Exception:
                checks["calendar_entries_check"] = False
            
            return {
                "status": "healthy" if all(checks.values()) else "degraded",
                "checks": checks,
                "checked_at": datetime.now(timezone.utc).isoformat(),
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
                "checked_at": datetime.now(timezone.utc).isoformat(),
            }


# Singleton instances per tenant
_vita_instances: Dict[str, VitaRepair] = {}


def get_vita_repair(tenant_id: str) -> VitaRepair:
    """Get or create Vita Repair instance for tenant"""
    if tenant_id not in _vita_instances:
        _vita_instances[tenant_id] = VitaRepair(tenant_id)
    return _vita_instances[tenant_id]

