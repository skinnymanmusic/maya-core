"""
OMEGA Core v3.0 - Claude AI Service
Safe prompt enforcement, response generation, metadata redaction
"""
import re
from typing import Optional, Dict, Any, List
from anthropic import Anthropic
from app.config import get_settings
from app.services.audit_service import get_audit_service

settings = get_settings()

# Claude client
_client = None


def _get_client() -> Anthropic:
    """Get or create Claude client"""
    global _client
    if _client is None:
        _client = Anthropic(api_key=settings.anthropic_api_key)
    return _client


# Universal system prompt with safety rules
MAYA_SYSTEM_PROMPT = """You are Maya Sinclair, a professional email assistant for DJ Skinny (Greg) at Skinny Man Entertainment and Level Three LLC.

CRITICAL SAFETY RULES (NEVER VIOLATE):
- ❌ NEVER include links, URLs, or external references in your responses
- ❌ NEVER hallucinate hours, prices, event details, or venue information
- ❌ NEVER provide external advice outside DJ/entertainment services
- ❌ NEVER mention competitors
- ❌ NEVER include sensitive metadata (sender_email, etc.)
- ✅ ALWAYS use professional email tone
- ✅ ALWAYS verify information before stating as fact
- ✅ ALWAYS ask for missing information rather than assuming

Your role is to:
- Respond to client inquiries professionally
- Ask clarifying questions when information is missing
- Provide accurate information about services and availability
- Maintain a friendly, professional tone
- Never invent details you don't know"""


class ClaudeService:
    """Claude AI service with safe prompt enforcement"""
    
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.client = _get_client()
        self.system_prompt = MAYA_SYSTEM_PROMPT
        self.audit = get_audit_service(tenant_id)
    
    def generate_response(
        self,
        email_body: str,
        context: Dict[str, Any],
        trace_id: Optional[str] = None
    ) -> Optional[str]:
        """
        Generate email response using Claude
        
        Args:
            email_body: Original email body
            context: Full context (intelligence results, client info, etc.)
            trace_id: Request trace ID
            
        Returns:
            Generated response text or None
        """
        try:
            # Build prompt with context (optimized, redacted)
            prompt = self._build_prompt(email_body, context)
            
            # Generate response
            response = self.client.messages.create(
                model=settings.claude_model,
                max_tokens=settings.claude_max_tokens,
                system=self.system_prompt,
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            
            response_text = response.content[0].text if response.content else ""
            
            # Sanitize response
            response_text = self._sanitize_response(response_text)
            
            self.audit.log_event(
                action="claude.response.generated",
                resource_type="email",
                metadata={"context_keys": list(context.keys())},
                trace_id=trace_id
            )
            
            return response_text
            
        except Exception as e:
            self.audit.log_event(
                action="claude.response.error",
                resource_type="email",
                metadata={"error": str(e)},
                trace_id=trace_id
            )
            return None
    
    def _build_prompt(self, email_body: str, context: Dict[str, Any]) -> str:
        """Build optimized prompt with context"""
        # Truncate email body to 2000 chars
        email_truncated = email_body[:2000] + "..." if len(email_body) > 2000 else email_body
        
        # Build context summary
        context_parts = []
        
        if context.get("venue"):
            context_parts.append(f"Venue: {context['venue']}")
        
        if context.get("client_name"):
            context_parts.append(f"Client: {context['client_name']}")
        
        if context.get("acceptance_detected"):
            context_parts.append("Client has accepted the booking")
        
        if context.get("missing_info"):
            questions = context.get("questions", [])[:3]  # Limit to 3 questions
            context_parts.append(f"Missing info: {', '.join(questions)}")
        
        if context.get("equipment_needed"):
            context_parts.append(f"Equipment: {', '.join(context['equipment_needed'])}")
        
        context_str = "\n".join(context_parts) if context_parts else "No additional context"
        
        prompt = f"""Client Email:
{email_truncated}

Context:
{context_str}

Please write a professional, friendly response to this email. Ask for any missing information. Do not invent details."""
        
        return prompt
    
    def _sanitize_response(self, response: str) -> str:
        """Sanitize response to remove unsafe content"""
        # Remove URLs
        response = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+])+', '[URL_REMOVED]', response)
        
        # Remove email addresses (except in context)
        response = re.sub(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', '[EMAIL_REMOVED]', response)
        
        # Remove HTML tags
        response = re.sub(r'<[^>]+>', '', response)
        
        # Remove scripts
        response = re.sub(r'<script[^>]*>.*?</script>', '', response, flags=re.DOTALL | re.IGNORECASE)
        
        return response.strip()
    
    def refine_response(
        self,
        draft_response: str,
        feedback: str,
        trace_id: Optional[str] = None
    ) -> Optional[str]:
        """
        Refine response based on feedback
        
        Args:
            draft_response: Original draft response
            feedback: Feedback or instructions
            trace_id: Request trace ID
            
        Returns:
            Refined response or None
        """
        try:
            response = self.client.messages.create(
                model=settings.claude_model,
                max_tokens=settings.claude_max_tokens,
                system=self.system_prompt,
                messages=[
                    {"role": "user", "content": f"Original response:\n{draft_response}\n\nFeedback: {feedback}\n\nPlease refine the response."}
                ]
            )
            
            refined = response.content[0].text if response.content else ""
            refined = self._sanitize_response(refined)
            
            self.audit.log_event(
                action="claude.response.refined",
                resource_type="email",
                trace_id=trace_id
            )
            
            return refined
            
        except Exception as e:
            self.audit.log_event(
                action="claude.response.refine.error",
                resource_type="email",
                metadata={"error": str(e)},
                trace_id=trace_id
            )
            return None

