"""
OMEGA Core v3.0 - Equipment Awareness Service
Equipment requirements mapping per venue/location
"""
from typing import Dict, Any, List

# Venue equipment database (simplified)
VENUE_EQUIPMENT = {
    "canopy by hilton": ["sound system", "microphones", "lighting"],
    "canopy": ["sound system", "microphones", "lighting"],
    # Add more venues as needed
}

# Equipment keywords
EQUIPMENT_KEYWORDS = {
    "sound": ["sound", "audio", "speakers", "microphone", "mic", "pa system"],
    "lighting": ["lighting", "lights", "dj lights", "uplighting"],
    "video": ["video", "screen", "projector", "tv"],
    "stage": ["stage", "platform", "riser"],
}


class EquipmentAwarenessService:
    """Equipment awareness per venue"""
    
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
    
    def analyze(self, email: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze email for equipment requirements
        
        Args:
            email: Email dictionary
            
        Returns:
            Analysis dictionary with equipment_needed, equipment_available
        """
        body = (email.get("body", "") or "").lower()
        subject = (email.get("subject", "") or "").lower()
        text = f"{subject} {body}"
        
        equipment_needed = []
        equipment_available = []
        
        # Check venue equipment
        venue = None
        for venue_name in VENUE_EQUIPMENT.keys():
            if venue_name in text:
                venue = venue_name
                equipment_available = VENUE_EQUIPMENT[venue_name]
                break
        
        # Detect equipment mentions
        for equipment_type, keywords in EQUIPMENT_KEYWORDS.items():
            if any(keyword in text for keyword in keywords):
                if equipment_type not in equipment_needed:
                    equipment_needed.append(equipment_type)
        
        return {
            "equipment_needed": equipment_needed,
            "equipment_available": equipment_available,
            "venue": venue,
        }

