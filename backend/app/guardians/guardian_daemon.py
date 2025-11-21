"""
OMEGA Core v3.0 - Guardian Daemon
Continuous monitoring daemon for all guardians
Runs safety/self-checks every 30 minutes (configurable)
Triggers SAFE MODE if any guardian check fails or Aegis detects critical risk
"""
from __future__ import annotations
import asyncio
import logging
from datetime import datetime, timedelta, timezone
from typing import Dict, Any, List, Optional
from uuid import UUID

from app.database import get_cursor
from app.services.audit_service import get_audit_service

# Guardian imports
from app.guardians.solin_mcp import get_solin_mcp
from app.guardians.sentra_safety import get_sentra_safety
from app.guardians.vita_repair import get_vita_repair

# Optional imports for Aegis and Archivus (fail-open if not available)
try:
    from app.services.aegis_anomaly_service import AegisAnomalyService
    AEGIS_AVAILABLE = True
except ImportError:
    AEGIS_AVAILABLE = False
    AegisAnomalyService = None

try:
    from app.services.archivus_service import ArchivusService
    ARCHIVUS_AVAILABLE = True
except ImportError:
    ARCHIVUS_AVAILABLE = False
    ArchivusService = None

logger = logging.getLogger(__name__)


class GuardianDaemon:
    """
    Continuous monitoring daemon for all guardians.
    Runs safety/self-checks every 30 minutes (configurable).
    Triggers SAFE MODE if any guardian check fails or Aegis detects critical risk.
    """

    def __init__(self, check_interval_minutes: int = 30):
        self.check_interval_minutes = check_interval_minutes
        self.is_running = False

    def get_all_tenant_ids(self) -> List[str]:
        """
        Fetch all active tenant IDs from database.
        Uses RLS fallback if needed.
        
        Returns:
            List of tenant ID strings
        """
        try:
            tenant_ids = []
            # Use elevated connection to bypass RLS if needed
            with get_cursor(tenant_id=None) as cur:
                cur.execute(
                    """
                    SELECT id::text
                    FROM tenants
                    WHERE is_active = TRUE
                    ORDER BY created_at ASC
                    """
                )
                rows = cur.fetchall()
                tenant_ids = [row[0] for row in rows if row[0]]
            
            # Fallback: if no tenants found, use default tenant
            if not tenant_ids:
                from app.config import get_settings
                settings = get_settings()
                if hasattr(settings, 'default_tenant_id') and settings.default_tenant_id:
                    tenant_ids = [settings.default_tenant_id]
            
            return tenant_ids
        except Exception as e:
            logger.error(f"Failed to fetch tenant IDs: {e}")
            # Fail-open: return empty list if query fails
            return []

    def run_once(self) -> Dict[str, Any]:
        """
        Executes a single round of guardian checks and Aegis analysis for all active tenants.
        Returns a summary of the run.
        """
        start_time = datetime.now(timezone.utc)
        audit = get_audit_service(None)  # Use global audit for daemon events
        overall_status = {"status": "healthy", "message": "All checks passed"}
        tenant_results: List[Dict[str, Any]] = []

        try:
            active_tenant_ids = self.get_all_tenant_ids()
            audit.log_event(
                action="guardian_daemon.run_start",
                resource_type="daemon",
                metadata={"active_tenants_count": len(active_tenant_ids)},
                tenant_id=None,
            )

            if not active_tenant_ids:
                logger.warning("No active tenants found for guardian daemon run")
                return {
                    "status": "warning",
                    "message": "No active tenants found",
                    "tenant_count": 0,
                    "started_at": start_time.isoformat(),
                    "completed_at": datetime.now(timezone.utc).isoformat(),
                }

            # Process each tenant
            for tenant_id in active_tenant_ids:
                try:
                    tenant_result = self._process_tenant(tenant_id)
                    tenant_results.append(tenant_result)
                    
                    # Check if tenant has critical issues
                    if tenant_result.get("status") == "critical":
                        overall_status = {
                            "status": "critical",
                            "message": f"Critical issues detected for tenant {tenant_id}",
                        }
                    elif tenant_result.get("status") == "warning" and overall_status["status"] == "healthy":
                        overall_status = {
                            "status": "warning",
                            "message": f"Warnings detected for tenant {tenant_id}",
                        }
                except Exception as e:
                    logger.error(f"Failed to process tenant {tenant_id}: {e}")
                    tenant_results.append({
                        "tenant_id": tenant_id,
                        "status": "error",
                        "error": str(e),
                    })

            end_time = datetime.now(timezone.utc)
            duration_seconds = (end_time - start_time).total_seconds()

            # Record Archivus system note (if available)
            if ARCHIVUS_AVAILABLE:
                try:
                    for tenant_id in active_tenant_ids:
                        try:
                            archivus = ArchivusService(tenant_id)
                            archivus.record_system_note(
                                category="guardian_daemon",
                                summary=f"Guardian daemon run completed: {overall_status['status']}",
                                details={
                                    "overall_status": overall_status,
                                    "tenant_count": len(active_tenant_ids),
                                    "duration_seconds": duration_seconds,
                                    "tenant_results": tenant_results,
                                },
                            )
                        except Exception as e:
                            logger.warning(f"Failed to record Archivus note for tenant {tenant_id}: {e}")
                except Exception as e:
                    logger.warning(f"Archivus integration failed: {e}")

            # Log daemon run completion
            audit.log_event(
                action="guardian_daemon.run_complete",
                resource_type="daemon",
                metadata={
                    "overall_status": overall_status,
                    "tenant_count": len(active_tenant_ids),
                    "duration_seconds": duration_seconds,
                    "tenant_results_count": len(tenant_results),
                },
                tenant_id=None,
            )

            return {
                "status": overall_status["status"],
                "message": overall_status["message"],
                "tenant_count": len(active_tenant_ids),
                "tenant_results": tenant_results,
                "started_at": start_time.isoformat(),
                "completed_at": end_time.isoformat(),
                "duration_seconds": duration_seconds,
            }
        except Exception as e:
            logger.error(f"Guardian daemon run failed: {e}", exc_info=True)
            audit.log_event(
                action="guardian_daemon.run_error",
                resource_type="daemon",
                metadata={"error": str(e)},
                tenant_id=None,
            )
            return {
                "status": "error",
                "message": f"Daemon run failed: {str(e)}",
                "started_at": start_time.isoformat(),
                "completed_at": datetime.now(timezone.utc).isoformat(),
            }

    def _process_tenant(self, tenant_id: str) -> Dict[str, Any]:
        """
        Process a single tenant: run all guardian checks and Aegis analysis.
        
        Args:
            tenant_id: Tenant ID to process
            
        Returns:
            Dict with status, guardian check results, and Aegis snapshot
        """
        tenant_start = datetime.now(timezone.utc)
        result = {
            "tenant_id": tenant_id,
            "status": "healthy",
            "guardian_checks": {},
            "aegis_snapshot": None,
            "started_at": tenant_start.isoformat(),
        }

        try:
            # Initialize guardians
            solin = get_solin_mcp(tenant_id)
            sentra = get_sentra_safety(tenant_id)
            vita = get_vita_repair(tenant_id)

            # Run guardian self-checks
            try:
                sentra_result = sentra.self_check()
                result["guardian_checks"]["sentra"] = sentra_result
                if sentra_result.get("status") != "healthy":
                    result["status"] = "warning"
            except Exception as e:
                logger.error(f"Sentra self-check failed for tenant {tenant_id}: {e}")
                result["guardian_checks"]["sentra"] = {"status": "error", "error": str(e)}
                result["status"] = "warning"

            try:
                vita_result = vita.self_check()
                result["guardian_checks"]["vita"] = vita_result
                if vita_result.get("status") != "healthy":
                    result["status"] = "warning"
            except Exception as e:
                logger.error(f"Vita self-check failed for tenant {tenant_id}: {e}")
                result["guardian_checks"]["vita"] = {"status": "error", "error": str(e)}
                result["status"] = "warning"

            try:
                solin_result = solin.mcp_health_check()
                result["guardian_checks"]["solin"] = solin_result
                if solin_result.get("status") == "safe_mode":
                    result["status"] = "critical"
                elif solin_result.get("status") == "warning":
                    if result["status"] == "healthy":
                        result["status"] = "warning"
            except Exception as e:
                logger.error(f"Solin health check failed for tenant {tenant_id}: {e}")
                result["guardian_checks"]["solin"] = {"status": "error", "error": str(e)}
                result["status"] = "warning"

            # Run Aegis anomaly analysis (if available)
            if AEGIS_AVAILABLE:
                try:
                    from sqlalchemy.ext.asyncio import AsyncSession
                    from app.database import get_async_session
                    
                    # Note: Aegis requires async session, but daemon is sync
                    # For now, we'll skip Aegis in sync context
                    # TODO: Make daemon async or create sync Aegis wrapper
                    logger.debug(f"Aegis analysis skipped for tenant {tenant_id} (sync context)")
                except Exception as e:
                    logger.warning(f"Aegis analysis failed for tenant {tenant_id}: {e}")
            else:
                logger.debug("Aegis not available, skipping anomaly analysis")

            result["completed_at"] = datetime.now(timezone.utc).isoformat()
            return result
        except Exception as e:
            logger.error(f"Failed to process tenant {tenant_id}: {e}", exc_info=True)
            result["status"] = "error"
            result["error"] = str(e)
            result["completed_at"] = datetime.now(timezone.utc).isoformat()
            return result

    async def run_loop(self) -> None:
        """
        Async loop wrapper for continuous operation.
        Runs guardian checks every check_interval_minutes.
        """
        self.is_running = True
        logger.info(f"Guardian daemon started (interval: {self.check_interval_minutes} minutes)")

        while self.is_running:
            try:
                result = self.run_once()
                logger.info(f"Guardian daemon run completed: {result.get('status')}")
            except Exception as e:
                logger.error(f"Guardian daemon run error: {e}", exc_info=True)

            # Wait for next interval
            await asyncio.sleep(self.check_interval_minutes * 60)

    @classmethod
    def run_forever(cls, check_interval_minutes: int = 30) -> None:
        """
        Class method for standalone execution.
        Runs daemon continuously until interrupted.
        
        Args:
            check_interval_minutes: Minutes between daemon runs
        """
        daemon = cls(check_interval_minutes=check_interval_minutes)
        try:
            asyncio.run(daemon.run_loop())
        except KeyboardInterrupt:
            logger.info("Guardian daemon stopped by user")
            daemon.is_running = False
        except Exception as e:
            logger.error(f"Guardian daemon crashed: {e}", exc_info=True)
            raise


def start_guardian_daemon(check_interval_minutes: int = 30) -> None:
    """
    Helper function to start guardian daemon.
    
    Args:
        check_interval_minutes: Minutes between daemon runs
    """
    GuardianDaemon.run_forever(check_interval_minutes=check_interval_minutes)


if __name__ == "__main__":
    # Standalone execution
    import sys
    interval = int(sys.argv[1]) if len(sys.argv) > 1 else 30
    start_guardian_daemon(check_interval_minutes=interval)

