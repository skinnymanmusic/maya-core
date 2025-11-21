"""
OMEGA Core v3.0 - Venue Intelligence Service
Venue detection with Canopy expertise, Eli integration, fallback database
"""
import httpx
from typing import Optional, Dict, Any
from app.services.audit_service import get_audit_service
from app.config import get_settings

settings = get_settings()

# Canopy by Hilton locations database (fallback)
CANOPY_LOCATIONS = {
    "canopy by hilton": ["atlanta", "boston", "chicago", "dallas", "denver", "miami", "nashville", "new york", "phoenix", "seattle"],
    "canopy": ["atlanta", "boston", "chicago", "dallas", "denver", "miami", "nashville", "new york", "phoenix", "seattle"],
}


class VenueIntelligenceService:
    """Venue detection and intelligence"""
    
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.audit = get_audit_service(tenant_id)
    
    def analyze(self, email: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze email for venue information
        
        Args:
            email: Email dictionary
            
        Returns:
            Analysis dictionary with venue, location, equipment_needed
        """
        body = (email.get("body", "") or "").lower()
        subject = (email.get("subject", "") or "").lower()
        text = f"{subject} {body}"
        
        venue = None
        location = None
        equipment_needed = []
        
        # Check for Canopy by Hilton
        for keyword, locations in CANOPY_LOCATIONS.items():
            if keyword in text:
                # Try to extract location
                for loc in locations:
                    if loc in text:
                        venue = f"Canopy by Hilton {loc.title()}"
                        location = loc.title()
                        break
                
                if not venue:
                    venue = "Canopy by Hilton"
        
        # Try Eli API if venue keyword detected
        if not venue and ("venue" in text or "location" in text or "place" in text):
            venue_data = self._query_eli_api(text)
            if venue_data:
                venue = venue_data.get("venue_name")
                location = venue_data.get("location")
                equipment_needed = venue_data.get("equipment", [])
        
        # Fallback: simple keyword detection
        if not venue:
            venue_keywords = ["venue", "location", "place", "hall", "ballroom", "hotel", "resort"]
            for keyword in venue_keywords:
                if keyword in text:
                    # Extract potential venue name (simple heuristic)
                    words = text.split()
                    idx = next((i for i, w in enumerate(words) if keyword in w), None)
                    if idx and idx < len(words) - 1:
                        venue = words[idx + 1].title() if idx + 1 < len(words) else None
                    break
        
        return {
            "venue": venue,
            "location": location,
            "equipment_needed": equipment_needed,
        }
    
    def _query_eli_api(self, text: str) -> Optional[Dict[str, Any]]:
        """Query Eli API for venue intelligence"""
        try:
            if not settings.eli_api_url:
                return None
            
            with httpx.Client(timeout=5.0) as client:
                response = client.post(
                    f"{settings.eli_api_url}/research/venue",
                    json={"text": text},
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
                return response.json()
        except Exception:
            # Fail-open: Eli API failure doesn't block processing
            return None

