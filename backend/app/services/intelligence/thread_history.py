"""
OMEGA Core v3.0 - Thread History Service
Thread reconstruction from database with chronological ordering
"""
from typing import Dict, Any, List
from datetime import datetime
from app.services.supabase_service import get_thread_emails


class ThreadHistoryService:
    """Thread history reconstruction"""
    
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
    
    def analyze(self, email: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze email thread history
        
        Args:
            email: Email dictionary
            
        Returns:
            Analysis dictionary with thread_history
        """
        thread_id = email.get("gmail_thread_id")
        if not thread_id:
            return {"thread_history": []}
        
        try:
            # Get thread emails from database
            thread_emails = get_thread_emails(thread_id, self.tenant_id, limit=50)
            
            # Build thread history (chronological)
            thread_history = [
                {
                    "sender": e.get("sender_name") or e.get("sender_email", ""),
                    "subject": e.get("subject", ""),
                    "body_preview": (e.get("body", "") or "")[:200],  # Preview only
                    "received_at": e.get("received_at").isoformat() if e.get("received_at") else None,
                }
                for e in sorted(thread_emails, key=lambda x: x.get("received_at") or datetime.min)
            ]
            
            return {"thread_history": thread_history}
        except Exception:
            return {"thread_history": []}

