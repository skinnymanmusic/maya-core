"""
OMEGA Core v3.0 - Guardian Manager
Coordinates all guardians and routes audit events
"""
from __future__ import annotations
from typing import Dict, Any, Optional
from app.guardians.solin_mcp import SolinMCP, get_solin_mcp
from app.guardians.sentra_safety import SentraSafety, get_sentra_safety
from app.guardians.vita_repair import VitaRepair, get_vita_repair


class GuardianManager:
    """
    Guardian Manager - Routes audit events to appropriate guardians
    """
    
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self._solin: Optional[SolinMCP] = None
        self._sentra: Optional[SentraSafety] = None
        self._vita: Optional[VitaRepair] = None
    
    @property
    def solin(self) -> SolinMCP:
        """Lazy initialization of Solin MCP"""
        if self._solin is None:
            self._solin = get_solin_mcp(self.tenant_id)
        return self._solin
    
    @property
    def sentra(self) -> SentraSafety:
        """Lazy initialization of Sentra Safety"""
        if self._sentra is None:
            self._sentra = get_sentra_safety(self.tenant_id)
        return self._sentra
    
    @property
    def vita(self) -> VitaRepair:
        """Lazy initialization of Vita Repair"""
        if self._vita is None:
            self._vita = get_vita_repair(self.tenant_id)
        return self._vita
    
    def receive_event(self, log_entry: Dict[str, Any]) -> None:
        """
        Receive audit log entry and route to appropriate guardians
        
        Routing Rules:
        - ERROR level → notify Sentra
        - email_processor + crash → notify Vita
        - All events → route to Solin with flags
        """
        try:
            # Extract routing information
            log_level = log_entry.get("level", "").upper()
            service = log_entry.get("service", "")
            error = log_entry.get("metadata", {}).get("error", "")
            
            # Determine routing flags
            route_to_sentra = log_level == "ERROR"
            route_to_vita = (
                service == "email_processor" and 
                ("crash" in error.lower() or "failure" in error.lower())
            )
            
            # Route to Solin with flags
            self.solin.receive_event(
                action=log_entry.get("action", ""),
                metadata=log_entry.get("metadata", {}),
                route_to_sentra=route_to_sentra,
                route_to_vita=route_to_vita,
            )
            
            # Direct routing if needed
            if route_to_sentra:
                self.sentra.receive_event(
                    action=log_entry.get("action", ""),
                    metadata=log_entry.get("metadata", {}),
                )
            
            if route_to_vita:
                self.vita.receive_event(
                    action=log_entry.get("action", ""),
                    metadata=log_entry.get("metadata", {}),
                )
        except Exception as e:
            # Fail-open: guardian routing failures don't affect audit logging
            pass


# Singleton instances per tenant
_guardian_managers: Dict[str, GuardianManager] = {}


def get_guardian_manager(tenant_id: str) -> GuardianManager:
    """Get or create guardian manager for tenant"""
    if tenant_id not in _guardian_managers:
        _guardian_managers[tenant_id] = GuardianManager(tenant_id)
    return _guardian_managers[tenant_id]

