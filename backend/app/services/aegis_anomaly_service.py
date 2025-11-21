"""
OMEGA Core v3.0 - Aegis Anomaly Service
Phase 12: Risk scoring and anomaly detection
"""
from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List, Optional
from app.database import get_cursor
from app.services.audit_service import get_audit_service


@dataclass
class TenantRiskSnapshot:
    """Risk snapshot for a tenant"""
    tenant_id: str
    unsafe_threads_24h: int
    unsafe_threads_7d: int
    retries_24h: int
    retries_7d: int
    repair_failures_24h: int
    repair_failures_7d: int
    emails_processed_24h: int
    emails_processed_7d: int
    risk_score: float
    risk_level: str  # "low" | "medium" | "high" | "critical"
    generated_at: datetime


class AegisAnomalyService:
    """
    Aegis Anomaly Detection and Risk Scoring
    Computes tenant risk snapshots and detects anomalies
    """
    
    def __init__(self):
        self.audit = get_audit_service(None)  # Global audit for Aegis
    
    def analyze_tenant(self, tenant_id: str) -> Optional[TenantRiskSnapshot]:
        """
        Analyze tenant and compute risk snapshot
        
        Args:
            tenant_id: Tenant UUID
            
        Returns:
            TenantRiskSnapshot or None if analysis fails
        """
        try:
            now = datetime.now(timezone.utc)
            d24 = now - timedelta(hours=24)
            d7d = now - timedelta(days=7)
            
            with get_cursor(tenant_id=None) as cur:
                # Count unsafe threads
                unsafe_24h = self._count_unsafe_threads(cur, tenant_id, d24)
                unsafe_7d = self._count_unsafe_threads(cur, tenant_id, d7d)
                
                # Count retries
                retries_24h = self._count_retries(cur, tenant_id, d24)
                retries_7d = self._count_retries(cur, tenant_id, d7d)
                
                # Count repair failures
                repair_24h = self._count_repair_failures(cur, tenant_id, d24)
                repair_7d = self._count_repair_failures(cur, tenant_id, d7d)
                
                # Count emails processed
                emails_24h = self._count_emails_processed(cur, tenant_id, d24)
                emails_7d = self._count_emails_processed(cur, tenant_id, d7d)
            
            # Compute risk score
            risk_score = self._compute_risk_score(
                unsafe_24h, unsafe_7d,
                retries_24h, retries_7d,
                repair_24h, repair_7d,
                emails_24h, emails_7d,
            )
            
            # Classify risk level
            risk_level = self._classify_risk_level(risk_score)
            
            return TenantRiskSnapshot(
                tenant_id=tenant_id,
                unsafe_threads_24h=unsafe_24h,
                unsafe_threads_7d=unsafe_7d,
                retries_24h=retries_24h,
                retries_7d=retries_7d,
                repair_failures_24h=repair_24h,
                repair_failures_7d=repair_7d,
                emails_processed_24h=emails_24h,
                emails_processed_7d=emails_7d,
                risk_score=risk_score,
                risk_level=risk_level,
                generated_at=now,
            )
        except Exception as e:
            # Fail-open: Aegis failures don't block system
            self.audit.log_event(
                action="aegis.analyze_tenant.error",
                resource_type="aegis",
                metadata={"error": str(e), "tenant_id": tenant_id},
                tenant_id=None,
            )
            return None
    
    def _count_unsafe_threads(self, cur, tenant_id: str, since: datetime) -> int:
        """Count unsafe threads since timestamp"""
        try:
            cur.execute(
                """
                SELECT COUNT(*)::int
                FROM unsafe_threads
                WHERE tenant_id = %s AND created_at >= %s
                """,
                (tenant_id, since),
            )
            return int(cur.fetchone()[0] or 0)
        except Exception:
            return 0
    
    def _count_retries(self, cur, tenant_id: str, since: datetime) -> int:
        """Count retry queue items since timestamp"""
        try:
            cur.execute(
                """
                SELECT COUNT(*)::int
                FROM email_retry_queue
                WHERE tenant_id = %s
                  AND created_at >= %s
                  AND status IN ('pending', 'failed')
                """,
                (tenant_id, since),
            )
            return int(cur.fetchone()[0] or 0)
        except Exception:
            return 0
    
    def _count_repair_failures(self, cur, tenant_id: str, since: datetime) -> int:
        """Count repair failures since timestamp"""
        try:
            cur.execute(
                """
                SELECT COUNT(*)::int
                FROM repair_log
                WHERE tenant_id = %s
                  AND created_at >= %s
                  AND success = FALSE
                """,
                (tenant_id, since),
            )
            return int(cur.fetchone()[0] or 0)
        except Exception:
            return 0
    
    def _count_emails_processed(self, cur, tenant_id: str, since: datetime) -> int:
        """Count emails processed since timestamp"""
        try:
            cur.execute(
                """
                SELECT COUNT(*)::int
                FROM audit_log
                WHERE tenant_id = %s
                  AND created_at >= %s
                  AND action = 'email.processed'
                """,
                (tenant_id, since),
            )
            return int(cur.fetchone()[0] or 0)
        except Exception:
            return 0
    
    def _compute_risk_score(
        self,
        unsafe_24h: int, unsafe_7d: int,
        retries_24h: int, retries_7d: int,
        repair_24h: int, repair_7d: int,
        emails_24h: int, emails_7d: int,
    ) -> float:
        """
        Compute risk score (0-100)
        
        Weights:
        - Unsafe threads: 4.0
        - Retry queue: 1.5
        - Repair failures: 3.0
        """
        # Normalize by email activity
        if emails_7d == 0:
            emails_7d = 1  # Avoid division by zero
        
        # Compute rates (per 100 emails)
        unsafe_rate_24h = (unsafe_24h / max(emails_24h, 1)) * 100
        unsafe_rate_7d = (unsafe_7d / emails_7d) * 100
        unsafe_spike = max(0, unsafe_rate_24h - unsafe_rate_7d) * 4.0
        
        retry_rate_24h = (retries_24h / max(emails_24h, 1)) * 100
        retry_rate_7d = (retries_7d / emails_7d) * 100
        retry_spike = max(0, retry_rate_24h - retry_rate_7d) * 1.5
        
        repair_rate_24h = (repair_24h / max(emails_24h, 1)) * 100
        repair_rate_7d = (repair_7d / emails_7d) * 100
        repair_spike = max(0, repair_rate_24h - repair_rate_7d) * 3.0
        
        # Base risk from absolute values
        base_risk = min(unsafe_24h * 2.0 + retries_24h * 0.5 + repair_24h * 1.5, 50)
        
        # Total risk score
        risk_score = min(base_risk + unsafe_spike + retry_spike + repair_spike, 100)
        
        return round(risk_score, 2)
    
    def _classify_risk_level(self, risk_score: float) -> str:
        """Classify risk level from score"""
        if risk_score >= 75:
            return "critical"
        elif risk_score >= 50:
            return "high"
        elif risk_score >= 25:
            return "medium"
        else:
            return "low"
    
    def analyze_all_tenants(self) -> List[TenantRiskSnapshot]:
        """
        Analyze all active tenants
        
        Returns:
            List of TenantRiskSnapshot for all tenants
        """
        try:
            # Get all active tenant IDs
            with get_cursor(tenant_id=None) as cur:
                cur.execute(
                    """
                    SELECT id::text
                    FROM tenants
                    WHERE is_active = TRUE
                    """
                )
                tenant_ids = [row[0] for row in cur.fetchall()]
            
            # Analyze each tenant
            snapshots = []
            for tenant_id in tenant_ids:
                snapshot = self.analyze_tenant(tenant_id)
                if snapshot:
                    snapshots.append(snapshot)
            
            return snapshots
        except Exception as e:
            # Fail-open: return empty list on error
            self.audit.log_event(
                action="aegis.analyze_all_tenants.error",
                resource_type="aegis",
                metadata={"error": str(e)},
                tenant_id=None,
            )
            return []

