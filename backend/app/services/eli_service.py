"""
OMEGA Core v3.0 - Eli Service
Venue intelligence integration (external API + local fallback)
"""
from __future__ import annotations
import httpx
from typing import Optional, Dict, Any
from app.config import get_settings
from app.services.audit_service import get_audit_service

settings = get_settings()


class EliService:
    """
    Eli Venue Intelligence Service
    Researches venue locations, equipment, and install history
    """
    
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.audit = get_audit_service(tenant_id)
        self.api_url = settings.eli_api_url
    
    def research_venue(self, venue_name: str, location: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Research venue information
        
        Args:
            venue_name: Venue name
            location: Optional location/city
            
        Returns:
            Venue data dictionary or None if not found
        """
        if not self.api_url:
            # No API configured - return None (fallback to local database)
            return None
        
        try:
            async def _fetch():
                async with httpx.AsyncClient(timeout=5.0) as client:
                    response = await client.post(
                        f"{self.api_url}/research/venue",
                        json={
                            "venue_name": venue_name,
                            "location": location,
                        },
                    )
                    if response.status_code == 200:
                        return response.json()
                    return None
            
            # Note: This is a sync method but Eli API might be async
            # For now, return None and let VenueIntelligenceService handle fallback
            # TODO: Make this async or use sync httpx client
            return None
        except Exception as e:
            # Fail-open: Eli failures don't block venue detection
            self.audit.log_event(
                action="eli.research_venue.error",
                resource_type="eli",
                metadata={"error": str(e), "venue_name": venue_name},
                tenant_id=self.tenant_id,
            )
            return None
    
    def get_equipment_awareness(self, venue_name: str) -> Optional[Dict[str, Any]]:
        """
        Get equipment awareness for venue
        
        Args:
            venue_name: Venue name
            
        Returns:
            Equipment information or None
        """
        if not self.api_url:
            return None
        
        try:
            # Similar to research_venue - placeholder for now
            # VenueIntelligenceService has local fallback
            return None
        except Exception as e:
            self.audit.log_event(
                action="eli.equipment_awareness.error",
                resource_type="eli",
                metadata={"error": str(e), "venue_name": venue_name},
                tenant_id=self.tenant_id,
            )
            return None

