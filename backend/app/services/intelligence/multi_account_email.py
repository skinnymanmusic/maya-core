"""
OMEGA Core v3.0 - Multi-Account Email Service
Account-specific behavior, auto-send vs draft logic, Greg reply detection
"""
from typing import Dict, Any
from app.config import get_settings

settings = get_settings()

# Test senders (auto-send allowed)
TEST_SENDERS = ["channkun@gmail.com"]

# Greg's email addresses
GREG_EMAILS = [
    settings.greg_sme_email,
    settings.greg_l3_email,
]


class MultiAccountEmailService:
    """Multi-account routing and behavior"""
    
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
    
    def analyze(self, email: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze email for account-specific routing
        
        Args:
            email: Email dictionary
            
        Returns:
            Analysis dictionary with is_test_sender, is_greg_reply, account_routing
        """
        sender_email = (email.get("sender_email", "") or "").lower()
        
        is_test_sender = sender_email in [s.lower() for s in TEST_SENDERS]
        is_greg_reply = sender_email in [e.lower() for e in GREG_EMAILS if e]
        
        # Account routing logic
        account_routing = {
            "auto_send_allowed": is_test_sender,
            "always_draft": not is_test_sender,
            "is_test_sender": is_test_sender,
            "is_greg_reply": is_greg_reply,
        }
        
        return {
            "is_test_sender": is_test_sender,
            "is_greg_reply": is_greg_reply,
            "account_routing": account_routing,
        }

