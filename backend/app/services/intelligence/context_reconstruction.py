"""
OMEGA Core v3.0 - Context Reconstruction Service
Client context building from database history
"""
from typing import Dict, Any, Optional
from app.services.supabase_service import get_client_by_email_hash
from app.services.gmail_service import hash_email


class ContextReconstructionService:
    """Client context reconstruction from history"""
    
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
    
    def analyze(self, email: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze email and build client context
        
        Args:
            email: Email dictionary
            
        Returns:
            Analysis dictionary with client_context, client_preferences
        """
        sender_email = email.get("sender_email", "")
        if not sender_email:
            return {"client_context": None}
        
        try:
            # Get client from database
            email_hash = hash_email(sender_email)
            client = get_client_by_email_hash(email_hash, self.tenant_id)
            
            if not client:
                return {"client_context": None}
            
            # Build context
            client_context = {
                "client_id": client.get("id"),
                "client_name": client.get("name"),
                "last_contact_at": client.get("last_contact_at").isoformat() if client.get("last_contact_at") else None,
                "company": client.get("company"),
            }
            
            return {
                "client_context": client_context,
                "client_name": client.get("name"),
            }
        except Exception:
            return {"client_context": None}

