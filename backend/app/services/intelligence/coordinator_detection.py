"""
OMEGA Core v3.0 - Coordinator Detection Service
Event coordinator identification, multiple date detection
"""
from typing import Dict, Any
import re
from datetime import datetime

# Coordinator keywords
COORDINATOR_KEYWORDS = [
    "coordinator", "coordinate", "multiple", "several", "both", "all events",
    "wedding", "reception", "ceremony", "rehearsal", "rehearsal dinner"
]

# Date patterns
DATE_PATTERNS = [
    r'\d{1,2}/\d{1,2}/\d{4}',
    r'\d{1,2}-\d{1,2}-\d{4}',
    r'[A-Z][a-z]+ \d{1,2},? \d{4}',
    r'\d{1,2} [A-Z][a-z]+ \d{4}',
]


class CoordinatorDetectionService:
    """Coordinator detection for multi-event emails"""
    
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
    
    def analyze(self, email: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze email for coordinator/multi-event indicators
        
        Args:
            email: Email dictionary
            
        Returns:
            Analysis dictionary with is_coordinator, event_count, event_dates
        """
        body = (email.get("body", "") or "").lower()
        subject = (email.get("subject", "") or "").lower()
        text = f"{subject} {body}"
        
        # Check for coordinator keywords
        is_coordinator = any(keyword in text for keyword in COORDINATOR_KEYWORDS)
        
        # Extract dates
        dates = []
        for pattern in DATE_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            dates.extend(matches)
        
        event_count = len(set(dates)) if dates else 1
        
        # Multiple dates = coordinator
        if event_count > 1:
            is_coordinator = True
        
        return {
            "is_coordinator": is_coordinator,
            "event_count": event_count,
            "event_dates": dates[:5],  # Limit to 5 dates
        }

