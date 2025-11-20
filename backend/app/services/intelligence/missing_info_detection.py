"""
OMEGA Core v3.0 - Missing Info Detection Service
Missing information detection with contextual questions
"""
from typing import Dict, Any, List

# Required information fields
REQUIRED_FIELDS = {
    "date": ["date", "when", "day", "time"],
    "venue": ["venue", "location", "where", "place"],
    "duration": ["duration", "hours", "how long", "length"],
    "event_type": ["type", "event", "wedding", "party", "corporate"],
    "guest_count": ["guests", "people", "attendees", "count"],
}


class MissingInfoDetectionService:
    """Missing information detection"""
    
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
    
    def analyze(self, email: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze email for missing required information
        
        Args:
            email: Email dictionary
            
        Returns:
            Analysis dictionary with missing_info, questions
        """
        body = (email.get("body", "") or "").lower()
        subject = (email.get("subject", "") or "").lower()
        text = f"{subject} {body}"
        
        missing_info = []
        questions = []
        
        # Check each required field
        for field, keywords in REQUIRED_FIELDS.items():
            found = any(keyword in text for keyword in keywords)
            if not found:
                missing_info.append(field)
                questions.append(self._generate_question(field))
        
        return {
            "missing_info": missing_info,
            "questions": questions,
        }
    
    def _generate_question(self, field: str) -> str:
        """Generate contextual question for missing field"""
        questions = {
            "date": "What date and time is the event?",
            "venue": "What is the venue or location?",
            "duration": "How long is the event?",
            "event_type": "What type of event is this?",
            "guest_count": "How many guests are expected?",
        }
        return questions.get(field, f"What is the {field}?")

