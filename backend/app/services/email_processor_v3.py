"""
OMEGA Core v3.0 - Email Processing Pipeline v3.0
Orchestrates all intelligence services, Nova pricing, Claude AI, and Gmail operations
"""
import traceback
from typing import Optional, Dict, Any
from datetime import datetime, timezone
import httpx
from tenacity import retry, stop_after_attempt, wait_exponential
from app.database import get_cursor
from app.services.audit_service import get_audit_service
from app.services.gmail_service import get_message_by_id, create_draft, send_email
from app.services.supabase_service import get_email_by_id, mark_email_processed, get_client_by_email_hash, create_or_update_client, update_client_last_contact, get_thread_emails
from app.services.claude_service import ClaudeService
from app.services.idempotency_service import get_idempotency_service
from app.services.retry_queue_service import get_retry_queue_service
from app.services.gmail_service import hash_email
from app.config import get_settings

settings = get_settings()

# Lazy-loaded intelligence services (to avoid circular imports)
_intelligence_services = None


def _get_intelligence_services():
    """Lazy-load intelligence services"""
    global _intelligence_services
    if _intelligence_services is None:
        try:
            from app.services.intelligence.venue_intelligence import VenueIntelligenceService
            from app.services.intelligence.coordinator_detection import CoordinatorDetectionService
            from app.services.intelligence.acceptance_detection import AcceptanceDetectionService
            from app.services.intelligence.missing_info_detection import MissingInfoDetectionService
            from app.services.intelligence.equipment_awareness import EquipmentAwarenessService
            from app.services.intelligence.thread_history import ThreadHistoryService
            from app.services.intelligence.multi_account_email import MultiAccountEmailService
            from app.services.intelligence.context_reconstruction import ContextReconstructionService
            
            _intelligence_services = {
                'venue': VenueIntelligenceService,
                'coordinator': CoordinatorDetectionService,
                'acceptance': AcceptanceDetectionService,
                'missing_info': MissingInfoDetectionService,
                'equipment': EquipmentAwarenessService,
                'thread_history': ThreadHistoryService,
                'multi_account': MultiAccountEmailService,
                'context': ContextReconstructionService,
            }
        except Exception:
            # Fail-open: if intelligence services not available, continue without them
            _intelligence_services = {}
    return _intelligence_services


# Lazy-loaded calendar service
_calendar_service = None


def _get_calendar_service(tenant_id: str):
    """Lazy-load calendar service"""
    global _calendar_service
    if _calendar_service is None:
        try:
            from app.services.calendar_service_v3 import CalendarServiceV3
            _calendar_service = CalendarServiceV3
        except Exception:
            return None
    return _calendar_service(tenant_id) if _calendar_service else None


# Lazy-loaded Solin MCP
_solin_mcp = None


def _get_solin_mcp(tenant_id: str):
    """Lazy-load Solin MCP for Safe Mode checks"""
    global _solin_mcp
    if _solin_mcp is None:
        try:
            from app.guardians.solin_mcp import get_solin_mcp
            _solin_mcp = get_solin_mcp
        except Exception:
            return None
    return _solin_mcp(tenant_id) if _solin_mcp else None


class EmailProcessorV3:
    """Email processing pipeline v3.0"""
    
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.audit = get_audit_service(tenant_id)
        self.idempotency = get_idempotency_service(tenant_id)
        self.retry_queue = get_retry_queue_service(tenant_id)
        self.claude = ClaudeService(tenant_id)
    
    def process_email(
        self,
        email_id: str,
        account_email: str,
        trace_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Main email processing pipeline
        
        Args:
            email_id: Email ID (UUID string)
            account_email: Gmail account email
            trace_id: Request trace ID
            
        Returns:
            Processing result dictionary
        """
        # Check Safe Mode
        solin = _get_solin_mcp(self.tenant_id)
        if solin and solin.is_safe_mode_enabled():
            self.audit.log_event(
                action="email.processing.blocked.safe_mode",
                resource_type="email",
                resource_id=email_id,
                metadata={"reason": "Safe Mode enabled"},
                trace_id=trace_id
            )
            return {
                "status": "blocked",
                "message": "Email processing blocked: Safe Mode enabled",
                "email_id": email_id
            }
        
        # Get email from database
        email = get_email_by_id(email_id, self.tenant_id)
        if not email:
            return {"status": "error", "message": "Email not found", "email_id": email_id}
        
        gmail_message_id = email.get("gmail_message_id")
        
        # Check idempotency
        if self.idempotency.is_processed(gmail_message_id):
            self.audit.log_event(
                action="email.processing.skipped.idempotency",
                resource_type="email",
                resource_id=email_id,
                metadata={"gmail_message_id": gmail_message_id},
                trace_id=trace_id
            )
            return {"status": "skipped", "message": "Already processed", "email_id": email_id}
        
        # Acquire processor lock
        lock_acquired, lock_error = self.idempotency.acquire_processor_lock(gmail_message_id)
        if not lock_acquired:
            self.audit.log_event(
                action="email.processing.skipped.locked",
                resource_type="email",
                resource_id=email_id,
                metadata={"error": lock_error},
                trace_id=trace_id
            )
            return {"status": "skipped", "message": lock_error, "email_id": email_id}
        
        try:
            # Check if Greg already replied
            if self._check_greg_reply(email):
                self.audit.log_event(
                    action="email.processing.skipped.greg_replied",
                    resource_type="email",
                    resource_id=email_id,
                    trace_id=trace_id
                )
                return {"status": "skipped", "message": "Greg already replied", "email_id": email_id}
            
            # Run all 8 intelligence services
            analysis = self._run_intelligence_services(email)
            
            # Get pricing from Nova API (if conditions met)
            pricing = None
            if analysis.get("acceptance_detected") and analysis.get("acceptance_confidence", 0) > 0.85:
                if not analysis.get("is_coordinator"):
                    pricing = self._get_nova_pricing(analysis, trace_id)
            
            # Generate Claude AI response
            context = self._build_context(email, analysis, pricing)
            response_text = self.claude.generate_response(
                email_body=email.get("body", ""),
                context=context,
                trace_id=trace_id
            )
            
            if not response_text:
                raise Exception("Claude response generation failed")
            
            # Check for calendar conflicts (before auto-send)
            conflicts = None
            calendar_service = _get_calendar_service(self.tenant_id)
            if calendar_service and analysis.get("event_date"):
                conflicts = calendar_service.detect_conflicts(
                    start_time=analysis["event_date"],
                    end_time=analysis.get("event_end_date") or analysis["event_date"],
                    trace_id=trace_id
                )
            
            # Determine send behavior (auto-send vs draft)
            send_behavior = self._determine_send_behavior(email, analysis, conflicts)
            
            # Send or create draft
            if send_behavior["auto_send"]:
                message_id = send_email(
                    account_email=account_email,
                    to=email.get("sender_email", ""),
                    subject=f"Re: {email.get('subject', '')}",
                    body=response_text,
                    thread_id=email.get("gmail_thread_id"),
                    tenant_id=self.tenant_id,
                    trace_id=trace_id
                )
                action = "email.sent"
            else:
                # Add conflict warning if needed
                if conflicts and conflicts.get("has_conflict"):
                    response_text = f"[CALENDAR CONFLICT WARNING: {conflicts.get('conflict_count', 0)} conflicting event(s) detected. Please review before sending.]\n\n{response_text}"
                
                message_id = create_draft(
                    account_email=account_email,
                    to=email.get("sender_email", ""),
                    subject=f"Re: {email.get('subject', '')}",
                    body=response_text,
                    thread_id=email.get("gmail_thread_id"),
                    tenant_id=self.tenant_id,
                    trace_id=trace_id
                )
                action = "email.draft.created"
            
            # Mark email as processed
            mark_email_processed(email_id, self.tenant_id)
            self.idempotency.mark_processed(gmail_message_id, trace_id)
            
            # Update client record
            sender_email = email.get("sender_email", "")
            if sender_email:
                email_hash = hash_email(sender_email)
                client_id = create_or_update_client(
                    email=sender_email,
                    name=email.get("sender_name"),
                    tenant_id=self.tenant_id,
                    trace_id=trace_id
                )
                if client_id:
                    update_client_last_contact(client_id, self.tenant_id)
            
            # Auto-block calendar on acceptance (if no conflicts)
            if analysis.get("acceptance_detected") and analysis.get("acceptance_confidence", 0) > 0.85:
                if calendar_service and not (conflicts and conflicts.get("has_conflict")):
                    calendar_service.auto_block_for_confirmed_gig(
                        event_date=analysis.get("event_date"),
                        client_name=analysis.get("client_name") or email.get("sender_name", "Client"),
                        venue=analysis.get("venue"),
                        location=analysis.get("location"),
                        duration_hours=analysis.get("duration_hours", 6.0),
                        client_id=client_id if sender_email else None,
                        trace_id=trace_id
                    )
            
            # Audit log success
            self.audit.log_event(
                action=action,
                resource_type="email",
                resource_id=email_id,
                metadata={
                    "gmail_message_id": gmail_message_id,
                    "message_id": message_id,
                    "auto_send": send_behavior["auto_send"],
                    "confidence": analysis.get("acceptance_confidence"),
                },
                trace_id=trace_id
            )
            
            return {
                "status": "success",
                "email_id": email_id,
                "message_id": message_id,
                "auto_send": send_behavior["auto_send"],
                "action": action
            }
            
        except Exception as e:
            # Enqueue retry
            error_message = str(e)
            error_stack = traceback.format_exc()
            
            self.retry_queue.enqueue_retry(
                email_id=email_id,
                gmail_message_id=gmail_message_id,
                account_email=account_email,
                error_message=error_message,
                trace_id=trace_id
            )
            
            # Log error
            self.audit.log_event(
                action="email.processing.error",
                resource_type="email",
                resource_id=email_id,
                metadata={
                    "error": error_message,
                    "error_stack": error_stack,
                    "gmail_message_id": gmail_message_id,
                    "service": "email_processor_v3",
                },
                trace_id=trace_id
            )
            
            return {
                "status": "error",
                "message": error_message,
                "email_id": email_id,
                "retry_enqueued": True
            }
        
        finally:
            # Always release lock
            self.idempotency.release_processor_lock(gmail_message_id)
    
    def _check_greg_reply(self, email: Dict[str, Any]) -> bool:
        """Check if Greg already replied to this thread"""
        try:
            thread_id = email.get("gmail_thread_id")
            if not thread_id:
                return False
            
            thread_emails = get_thread_emails(thread_id, self.tenant_id, limit=50)
            
            # Check if any email in thread is from Greg's emails
            greg_emails = [
                settings.greg_sme_email,
                settings.greg_l3_email,
            ]
            
            for thread_email in thread_emails:
                if thread_email.get("sender_email") in greg_emails:
                    return True
            
            return False
        except Exception:
            return False
    
    def _run_intelligence_services(self, email: Dict[str, Any]) -> Dict[str, Any]:
        """Run all 8 intelligence services"""
        analysis = {}
        services = _get_intelligence_services()
        
        for service_name, service_class in services.items():
            try:
                service = service_class(self.tenant_id)
                result = service.analyze(email)
                analysis.update(result)
            except Exception as e:
                # Fail-open: intelligence service failures don't block processing
                self.audit.log_event(
                    action="intelligence.service.error",
                    resource_type="email",
                    metadata={"service": service_name, "error": str(e)}
                )
        
        return analysis
    
    @retry(
        stop=stop_after_attempt(4),
        wait=wait_exponential(multiplier=0.2, min=0.2, max=5)
    )
    def _get_nova_pricing(
        self,
        analysis: Dict[str, Any],
        trace_id: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Get pricing from Nova API with exponential backoff
        
        Retry strategy: 200ms, 1s, 2s, 5s
        """
        try:
            if not settings.nova_api_url:
                return None
            
            event_info = {
                "event_type": analysis.get("event_type"),
                "event_date": analysis.get("event_date"),
                "duration_hours": analysis.get("duration_hours", 6.0),
                "venue": analysis.get("venue"),
                "location": analysis.get("location"),
            }
            
            with httpx.Client(timeout=10.0) as client:
                response = client.post(
                    f"{settings.nova_api_url}/api/pricing/calculate",
                    json=event_info,
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
                return response.json()
                
        except Exception as e:
            self.audit.log_event(
                action="nova.pricing.error",
                resource_type="pricing",
                metadata={"error": str(e), "event_info": event_info},
                trace_id=trace_id
            )
            # Graceful failure: return None (no fake pricing)
            return None
    
    def _build_context(
        self,
        email: Dict[str, Any],
        analysis: Dict[str, Any],
        pricing: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """Build context for Claude AI"""
        context = {
            "venue": analysis.get("venue"),
            "location": analysis.get("location"),
            "client_name": email.get("sender_name"),
            "acceptance_detected": analysis.get("acceptance_detected", False),
            "acceptance_confidence": analysis.get("acceptance_confidence", 0),
            "missing_info": analysis.get("missing_info", []),
            "questions": analysis.get("questions", [])[:3],  # Limit to 3
            "equipment_needed": analysis.get("equipment_needed", []),
            "is_coordinator": analysis.get("is_coordinator", False),
            "thread_history": analysis.get("thread_history", []),
        }
        
        if pricing:
            context["pricing"] = pricing
        
        return context
    
    def _determine_send_behavior(
        self,
        email: Dict[str, Any],
        analysis: Dict[str, Any],
        conflicts: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Determine auto-send vs draft behavior
        
        Rules:
        - Only for test senders (channkun@gmail.com)
        - Only if confidence > 0.85
        - Only if no conflicts detected
        - Real clients → Always draft
        """
        sender_email = email.get("sender_email", "").lower()
        test_senders = ["channkun@gmail.com"]
        
        is_test_sender = sender_email in test_senders
        high_confidence = analysis.get("acceptance_confidence", 0) > 0.85
        has_conflicts = conflicts and conflicts.get("has_conflict", False)
        
        auto_send = is_test_sender and high_confidence and not has_conflicts
        
        return {
            "auto_send": auto_send,
            "reason": "test_sender" if is_test_sender else "real_client",
            "confidence": analysis.get("acceptance_confidence", 0),
            "has_conflicts": has_conflicts,
        }
    
    def retry_email(
        self,
        email_id: str,
        gmail_message_id: str,
        account_email: str
    ) -> Dict[str, Any]:
        """
        Retry processing a failed email (called by retry worker)
        
        Args:
            email_id: Email ID
            gmail_message_id: Gmail message ID
            account_email: Account email
            
        Returns:
            Processing result
        """
        return self.process_email(email_id, account_email, trace_id=None)

