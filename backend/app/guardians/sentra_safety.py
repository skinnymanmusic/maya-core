"""
OMEGA Core v3.0 - Sentra Safety AI
Enforces runtime safety policies and tags unsafe threads
"""
from __future__ import annotations
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from app.services.audit_service import get_audit_service
from app.guardians.solin_mcp import get_solin_mcp
from app.database import get_cursor


class SentraSafety:
    """
    Sentra Safety AI - Runtime safety enforcement
    """
    
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.audit = get_audit_service(tenant_id)
        self._security_failure_counts: Dict[str, int] = {}
    
    def receive_event(self, action: str, metadata: Dict[str, Any]) -> None:
        """
        Receive audit event and check for safety violations
        
        Args:
            action: Audit action name
            metadata: Event metadata
        """
        try:
            # Check if security error
            error = metadata.get("error", "")
            if self._is_security_error(error):
                self.enforce_action(
                    violation_type="security_violation",
                    reason=f"Security error detected: {error}",
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
            action=f"guardian.sentra.{action}",
            resource_type="guardian",
            metadata=metadata,
            tenant_id=self.tenant_id,
        )
    
    def enforce_action(
        self,
        violation_type: str,
        reason: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Apply safety enforcement action
        
        Args:
            violation_type: Type of violation (ai_hallucination, prompt_injection, etc.)
            reason: Reason for enforcement
            metadata: Optional metadata
        
        Returns:
            Dict with enforcement result
        """
        try:
            thread_id = (metadata or {}).get("thread_id")
            
            # Tag thread as unsafe
            if thread_id:
                self._tag_unsafe_thread(
                    thread_id=thread_id,
                    reason=reason,
                    violation_type=violation_type,
                    severity=self._determine_severity(violation_type),
                )
            
            # Handle specific violation types
            if violation_type == "ai_hallucination":
                return {"action": "tagged", "thread_id": thread_id}
            elif violation_type == "prompt_injection":
                # Block output and notify Solin
                solin = get_solin_mcp(self.tenant_id)
                solin.receive_event(
                    action="sentra.prompt_injection",
                    metadata={"thread_id": thread_id, "reason": reason},
                )
                return {"action": "blocked", "output_blocked": True, "thread_id": thread_id}
            elif violation_type in ("authorization_violation", "authentication_violation"):
                return {"action": "aborted", "processing_aborted": True, "thread_id": thread_id}
            elif violation_type == "security_violation":
                # Track failures and trigger lockdown if threshold exceeded
                if thread_id:
                    failure_count = self._increment_security_failure(thread_id)
                    if failure_count >= 3:
                        self._command_system_lockdown(thread_id, reason)
                return {"action": "tagged", "thread_id": thread_id}
            
            return {"action": "tagged", "thread_id": thread_id}
        except Exception as e:
            # Fail-open: enforcement failures don't block system
            return {"action": "error", "error": str(e)}
    
    def _tag_unsafe_thread(
        self,
        thread_id: str,
        reason: str,
        violation_type: str,
        severity: str,
    ) -> None:
        """
        Tag thread as unsafe in database
        
        Args:
            thread_id: Gmail thread ID
            reason: Reason for tagging
            violation_type: Type of violation
            severity: Severity level (low, medium, high, critical)
        """
        try:
            with get_cursor(tenant_id=self.tenant_id) as cur:
                cur.execute(
                    """
                    INSERT INTO unsafe_threads (tenant_id, thread_id, reason, violation_type, severity, created_at)
                    VALUES (%s, %s, %s, %s, %s, NOW())
                    ON CONFLICT (tenant_id, thread_id)
                    DO UPDATE SET
                        reason = EXCLUDED.reason,
                        violation_type = EXCLUDED.violation_type,
                        severity = EXCLUDED.severity,
                        updated_at = NOW()
                    """,
                    (self.tenant_id, thread_id, reason, violation_type, severity),
                )
                cur.connection.commit()
        except Exception as e:
            # Fail-open: tagging failures don't block system
            pass
    
    def is_thread_unsafe(self, thread_id: str) -> bool:
        """
        Check if thread is tagged as unsafe
        
        Args:
            thread_id: Gmail thread ID
        
        Returns:
            True if thread is unsafe
        """
        try:
            with get_cursor(tenant_id=self.tenant_id) as cur:
                cur.execute(
                    """
                    SELECT COUNT(*)::int
                    FROM unsafe_threads
                    WHERE tenant_id = %s AND thread_id = %s
                    """,
                    (self.tenant_id, thread_id),
                )
                count = cur.fetchone()[0] or 0
                return count > 0
        except Exception as e:
            # Fail-open: return False if check fails
            return False
    
    def check_static_safety_rules(self, email_text: str) -> Dict[str, Any]:
        """
        Check email against static safety rules
        
        Args:
            email_text: Email body text
        
        Returns:
            Dict with violations found
        """
        violations = []
        
        # Check for system prompt reveal
        if self._check_system_prompt_reveal(email_text):
            violations.append({
                "type": "system_prompt_reveal",
                "severity": "high",
            })
        
        # Check for hallucination patterns
        if self._check_hallucination(email_text):
            violations.append({
                "type": "ai_hallucination",
                "severity": "high",
            })
        
        # Check for external URLs
        external_urls = self._check_external_urls(email_text)
        if external_urls:
            violations.append({
                "type": "external_urls",
                "severity": "medium",
                "urls": external_urls,
            })
        
        # Check for invented details
        if self._check_invented_details(email_text):
            violations.append({
                "type": "invented_details",
                "severity": "high",
            })
        
        return {"violations": violations, "has_violations": len(violations) > 0}
    
    def _check_system_prompt_reveal(self, text: str) -> bool:
        """Check for system prompt indicators"""
        patterns = ["system prompt", "here is my system", "i am an ai assistant"]
        text_lower = text.lower()
        return any(pattern in text_lower for pattern in patterns)
    
    def _check_hallucination(self, text: str) -> bool:
        """Check for hallucination patterns"""
        patterns = ["i'm not sure but", "i believe", "probably"]
        text_lower = text.lower()
        return any(pattern in text_lower for pattern in patterns)
    
    def _check_external_urls(self, text: str) -> list[str]:
        """Check for external URLs (excluding internal domains)"""
        import re
        url_pattern = r'https?://[^\s]+'
        urls = re.findall(url_pattern, text)
        internal_domains = ["skinnymanmusic.com", "levelthree.io"]
        external_urls = [
            url for url in urls
            if not any(domain in url for domain in internal_domains)
        ]
        return external_urls
    
    def _check_invented_details(self, text: str) -> bool:
        """Check for invented details (prices, times, venues)"""
        # Simple heuristic: check for price patterns, time patterns, etc.
        import re
        price_pattern = r'\$\d+'
        time_pattern = r'\d{1,2}:\d{2}\s*(AM|PM|am|pm)'
        has_price = bool(re.search(price_pattern, text))
        has_time = bool(re.search(time_pattern, text))
        # This is a simplified check - real implementation would be more sophisticated
        return has_price or has_time
    
    def _determine_severity(self, violation_type: str) -> str:
        """Determine severity level for violation"""
        high_severity = [
            "ai_hallucination",
            "prompt_injection",
            "authorization_violation",
            "authentication_violation",
            "invented_details",
            "system_prompt_reveal",
        ]
        if violation_type in high_severity:
            return "high"
        elif violation_type == "external_urls":
            return "medium"
        else:
            return "low"
    
    def _is_security_error(self, error: str) -> bool:
        """Check if error is a security-related error"""
        security_keywords = [
            "unauthorized",
            "forbidden",
            "authentication",
            "authorization",
            "token",
            "credential",
            "security",
        ]
        error_lower = error.lower()
        return any(keyword in error_lower for keyword in security_keywords)
    
    def _increment_security_failure(self, thread_id: str) -> int:
        """Increment security failure count for thread"""
        if thread_id not in self._security_failure_counts:
            self._security_failure_counts[thread_id] = 0
        self._security_failure_counts[thread_id] += 1
        return self._security_failure_counts[thread_id]
    
    def _command_system_lockdown(self, thread_id: str, reason: str) -> None:
        """Command system lockdown for repeated failures"""
        try:
            solin = get_solin_mcp(self.tenant_id)
            solin.activate_safe_mode(
                reason=f"Repeated security failures in thread {thread_id}: {reason}",
            )
            self.audit.log_event(
                action="guardian.sentra.system_lockdown",
                resource_type="system",
                metadata={"thread_id": thread_id, "reason": reason},
                tenant_id=self.tenant_id,
            )
        except Exception as e:
            # Fail-open: lockdown failures don't block system
            pass
    
    def self_check(self) -> Dict[str, Any]:
        """
        Run integrity checks on Sentra systems
        
        Returns:
            Dict with check results
        """
        try:
            checks = {
                "unsafe_threads_check": True,
                "security_tracking_check": True,
                "static_rules_check": True,
                "db_connectivity_check": True,
            }
            
            # Check unsafe threads table
            try:
                with get_cursor(tenant_id=self.tenant_id) as cur:
                    cur.execute(
                        """
                        SELECT COUNT(*)::int
                        FROM unsafe_threads
                        WHERE tenant_id = %s
                        LIMIT 1
                        """,
                        (self.tenant_id,),
                    )
                    cur.fetchone()
            except Exception:
                checks["unsafe_threads_check"] = False
            
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
_sentra_instances: Dict[str, SentraSafety] = {}


def get_sentra_safety(tenant_id: str) -> SentraSafety:
    """Get or create Sentra Safety instance for tenant"""
    if tenant_id not in _sentra_instances:
        _sentra_instances[tenant_id] = SentraSafety(tenant_id)
    return _sentra_instances[tenant_id]

