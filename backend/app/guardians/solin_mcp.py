"""
OMEGA Core v3.0 - Solin MCP (Master Control Program)
Orchestrates all guardians and manages Safe Mode
"""
from __future__ import annotations
from typing import Dict, Any, Optional
from datetime import datetime, timedelta, timezone
from app.services.audit_service import get_audit_service
from app.guardians.sentra_safety import get_sentra_safety
from app.guardians.vita_repair import get_vita_repair
from app.database import get_cursor
from app.config import get_settings

settings = get_settings()


class SolinMCP:
    """
    Solin MCP - Master Control Program
    Orchestrates all guardians and manages Safe Mode
    """
    
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.audit = get_audit_service(tenant_id)
        self._safe_mode_enabled = False
        self._safe_mode_reason: Optional[str] = None
    
    def receive_event(
        self,
        action: str,
        metadata: Dict[str, Any],
        route_to_sentra: bool = False,
        route_to_vita: bool = False,
    ) -> None:
        """
        Receive audit event and route to appropriate guardians
        
        Args:
            action: Audit action name
            metadata: Event metadata
            route_to_sentra: Explicit flag to route to Sentra
            route_to_vita: Explicit flag to route to Vita
        """
        try:
            # Route to Sentra if flagged
            if route_to_sentra:
                sentra = get_sentra_safety(self.tenant_id)
                sentra.receive_event(action, metadata)
            
            # Route to Vita if flagged
            if route_to_vita:
                vita = get_vita_repair(self.tenant_id)
                vita.receive_event(action, metadata)
            
            # Log action
            self.log_action(action, metadata)
        except Exception as e:
            # Fail-open: guardian failures don't affect main pipeline
            pass
    
    def log_action(self, action: str, metadata: Dict[str, Any]) -> None:
        """Log guardian action"""
        self.audit.log_event(
            action=f"guardian.solin.{action}",
            resource_type="guardian",
            metadata=metadata,
            tenant_id=self.tenant_id,
        )
    
    def observe_guardians(self) -> Dict[str, Any]:
        """
        Monitor guardian health and return observation data
        
        Returns:
            Dict with sentra_warnings, vita_failures, thresholds, etc.
        """
        try:
            now = datetime.now(timezone.utc)
            window_start = now - timedelta(minutes=15)
            
            # Count Sentra warnings in last 15 minutes
            sentra_warnings = 0
            with get_cursor(tenant_id=self.tenant_id) as cur:
                cur.execute(
                    """
                    SELECT COUNT(*)::int
                    FROM audit_log
                    WHERE tenant_id = %s
                      AND action LIKE 'guardian.sentra.%'
                      AND level = 'WARNING'
                      AND created_at >= %s
                    """,
                    (self.tenant_id, window_start),
                )
                sentra_warnings = cur.fetchone()[0] or 0
            
            # Count Vita failures in last 15 minutes
            vita_failures = 0
            with get_cursor(tenant_id=self.tenant_id) as cur:
                cur.execute(
                    """
                    SELECT COUNT(*)::int
                    FROM audit_log
                    WHERE tenant_id = %s
                      AND action LIKE 'guardian.vita.%'
                      AND level = 'ERROR'
                      AND created_at >= %s
                    """,
                    (self.tenant_id, window_start),
                )
                vita_failures = cur.fetchone()[0] or 0
            
            return {
                "sentra_warnings": sentra_warnings,
                "vita_failures": vita_failures,
                "threshold": 5,
                "window_minutes": 15,
                "observed_at": now.isoformat(),
            }
        except Exception as e:
            return {
                "sentra_warnings": 0,
                "vita_failures": 0,
                "threshold": 5,
                "window_minutes": 15,
                "error": str(e),
            }
    
    def enforce_global_rules(self) -> None:
        """
        Apply global safety rules and activate Safe Mode if thresholds exceeded
        """
        try:
            observation = self.observe_guardians()
            
            # Check if thresholds exceeded
            if observation["sentra_warnings"] >= 5:
                self.activate_safe_mode(
                    reason=f"Repeated Sentra warnings: {observation['sentra_warnings']} in 15 minutes",
                    observation=observation,
                )
            elif observation["vita_failures"] >= 5:
                self.activate_safe_mode(
                    reason=f"Repeated Vita failures: {observation['vita_failures']} in 15 minutes",
                    observation=observation,
                )
        except Exception as e:
            # Fail-open: rule enforcement failures don't block system
            pass
    
    def mcp_health_check(self) -> Dict[str, Any]:
        """
        Perform comprehensive MCP health check
        
        Returns:
            Dict with status (healthy/degraded/safe_mode/warning) and details
        """
        try:
            observation = self.observe_guardians()
            safe_mode = self.is_safe_mode_enabled()
            
            # Determine status
            if safe_mode:
                status = "safe_mode"
            elif observation["sentra_warnings"] >= 3 or observation["vita_failures"] >= 3:
                status = "warning"
            elif observation["sentra_warnings"] > 0 or observation["vita_failures"] > 0:
                status = "degraded"
            else:
                status = "healthy"
            
            return {
                "status": status,
                "safe_mode_enabled": safe_mode,
                "safe_mode_reason": self._safe_mode_reason,
                "observation": observation,
                "checked_at": datetime.now(timezone.utc).isoformat(),
            }
        except Exception as e:
            return {
                "status": "degraded",
                "error": str(e),
                "checked_at": datetime.now(timezone.utc).isoformat(),
            }
    
    def activate_safe_mode(self, reason: str, observation: Optional[Dict[str, Any]] = None) -> None:
        """
        Activate Safe Mode - freeze system operations
        
        Args:
            reason: Reason for Safe Mode activation
            observation: Optional observation data
        """
        try:
            self._safe_mode_enabled = True
            self._safe_mode_reason = reason
            
            # Store in database
            with get_cursor(tenant_id=self.tenant_id) as cur:
                cur.execute(
                    """
                    INSERT INTO system_state (tenant_id, state_key, state_value, updated_at)
                    VALUES (%s, 'safe_mode', 'true', NOW())
                    ON CONFLICT (tenant_id, state_key)
                    DO UPDATE SET state_value = 'true', updated_at = NOW()
                    """,
                    (self.tenant_id,),
                )
                cur.connection.commit()
            
            # Log activation
            self.audit.log_event(
                action="guardian.solin.safe_mode.activated",
                resource_type="system",
                metadata={
                    "reason": reason,
                    "observation": observation or {},
                },
                tenant_id=self.tenant_id,
            )
            
            # TODO: Send notifications (email/Discord)
        except Exception as e:
            # Fail-open: Safe Mode activation failures don't block system
            pass
    
    def deactivate_safe_mode(self, reason: str) -> None:
        """
        Deactivate Safe Mode - resume system operations
        
        Args:
            reason: Reason for Safe Mode deactivation
        """
        try:
            self._safe_mode_enabled = False
            self._safe_mode_reason = None
            
            # Update database
            with get_cursor(tenant_id=self.tenant_id) as cur:
                cur.execute(
                    """
                    INSERT INTO system_state (tenant_id, state_key, state_value, updated_at)
                    VALUES (%s, 'safe_mode', 'false', NOW())
                    ON CONFLICT (tenant_id, state_key)
                    DO UPDATE SET state_value = 'false', updated_at = NOW()
                    """,
                    (self.tenant_id,),
                )
                cur.connection.commit()
            
            # Log deactivation
            self.audit.log_event(
                action="guardian.solin.safe_mode.deactivated",
                resource_type="system",
                metadata={"reason": reason},
                tenant_id=self.tenant_id,
            )
        except Exception as e:
            # Fail-open: Safe Mode deactivation failures don't block system
            pass
    
    def is_safe_mode_enabled(self) -> bool:
        """
        Check if Safe Mode is enabled (in-memory + database check)
        
        Returns:
            True if Safe Mode is enabled
        """
        try:
            # Check in-memory first
            if self._safe_mode_enabled:
                return True
            
            # Check database
            with get_cursor(tenant_id=self.tenant_id) as cur:
                cur.execute(
                    """
                    SELECT state_value
                    FROM system_state
                    WHERE tenant_id = %s AND state_key = 'safe_mode'
                    """,
                    (self.tenant_id,),
                )
                row = cur.fetchone()
                if row and row[0] == "true":
                    self._safe_mode_enabled = True
                    return True
            
            return False
        except Exception as e:
            # Fail-open: return False if check fails
            return False
    
    def handle_aegis_risk_snapshot(self, snapshot: Dict[str, Any]) -> None:
        """
        Handle Aegis risk snapshot and activate Safe Mode if critical
        
        Args:
            snapshot: TenantRiskSnapshot from Aegis
        """
        try:
            risk_level = snapshot.get("risk_level", "low")
            
            if risk_level == "critical":
                self.activate_safe_mode(
                    reason=f"Aegis critical risk: {snapshot.get('risk_score', 0)}",
                    observation=snapshot,
                )
            elif risk_level == "high":
                # Log warning but don't auto-activate
                self.audit.log_event(
                    action="guardian.solin.aegis.high_risk",
                    resource_type="system",
                    metadata={"snapshot": snapshot},
                    tenant_id=self.tenant_id,
                )
        except Exception as e:
            # Fail-open: Aegis integration failures don't block system
            pass


# Singleton instances per tenant
_solin_instances: Dict[str, SolinMCP] = {}


def get_solin_mcp(tenant_id: str) -> SolinMCP:
    """Get or create Solin MCP instance for tenant"""
    if tenant_id not in _solin_instances:
        _solin_instances[tenant_id] = SolinMCP(tenant_id)
    return _solin_instances[tenant_id]

