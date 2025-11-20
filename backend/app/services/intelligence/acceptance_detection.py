"""
OMEGA Core v3.0 - Acceptance Detection Service
Quote acceptance recognition with confidence scoring
"""
from typing import Dict, Any, Optional
from datetime import datetime
import re

# High confidence acceptance keywords
HIGH_CONFIDENCE_KEYWORDS = [
    "yes", "accepted", "confirmed", "we accept", "sounds good", "let's do it",
    "book it", "reserve", "we're in", "count us in", "we'll take it"
]

# Low confidence acceptance keywords
LOW_CONFIDENCE_KEYWORDS = [
    "interested", "maybe", "possibly", "considering", "thinking about",
    "sounds interesting", "let me check", "get back to you"
]

# Rejection keywords
REJECTION_KEYWORDS = [
    "no", "not interested", "decline", "pass", "not available", "can't", "cannot"
]


class AcceptanceDetectionService:
    """Acceptance detection with confidence scoring"""
    
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
    
    def analyze(self, email: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze email for acceptance indicators
        
        Args:
            email: Email dictionary
            
        Returns:
            Analysis dictionary with acceptance_detected, acceptance_confidence, event_date, duration_hours
        """
        body = (email.get("body", "") or "").lower()
        subject = (email.get("subject", "") or "").lower()
        text = f"{subject} {body}"
        
        # Check for rejection first
        if any(keyword in text for keyword in REJECTION_KEYWORDS):
            return {
                "acceptance_detected": False,
                "acceptance_confidence": 0.0,
            }
        
        # Check for high confidence acceptance
        high_confidence = any(keyword in text for keyword in HIGH_CONFIDENCE_KEYWORDS)
        low_confidence = any(keyword in text for keyword in LOW_CONFIDENCE_KEYWORDS)
        
        acceptance_detected = high_confidence or low_confidence
        confidence = 0.9 if high_confidence else (0.6 if low_confidence else 0.0)
        
        # Extract event date (simple heuristic)
        event_date = self._extract_date(text)
        duration_hours = self._extract_duration(text)
        
        return {
            "acceptance_detected": acceptance_detected,
            "acceptance_confidence": confidence,
            "event_date": event_date,
            "duration_hours": duration_hours,
        }
    
    def _extract_date(self, text: str) -> Optional[datetime]:
        """Extract event date from text"""
        # Simple date extraction (can be enhanced)
        date_patterns = [
            r'\d{1,2}/\d{1,2}/\d{4}',
            r'\d{1,2}-\d{1,2}-\d{4}',
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text)
            if match:
                try:
                    date_str = match.group(0)
                    if '/' in date_str:
                        return datetime.strptime(date_str, "%m/%d/%Y")
                    elif '-' in date_str:
                        return datetime.strptime(date_str, "%m-%d-%Y")
                except Exception:
                    pass
        
        return None
    
    def _extract_duration(self, text: str) -> float:
        """Extract duration in hours"""
        # Simple duration extraction
        duration_patterns = [
            r'(\d+)\s*hours?',
            r'(\d+)\s*hrs?',
            r'(\d+):00',  # Time format like "6:00"
        ]
        
        for pattern in duration_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                try:
                    return float(match.group(1))
                except Exception:
                    pass
        
        return 6.0  # Default duration

