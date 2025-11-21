"""
SMS Service for Beauty Booking
Uses Twilio for SMS sending/receiving
"""
from twilio.rest import Client
from typing import Dict, Optional
from app.config.twilio_config import get_twilio_settings
from app.services.audit_service import get_audit_service


class SMSService:
    """SMS service using Twilio"""
    
    def __init__(self, tenant_id: Optional[str] = None):
        self.settings = get_twilio_settings()
        self.client = Client(
            self.settings.twilio_account_sid,
            self.settings.twilio_auth_token
        )
        self.tenant_id = tenant_id
        self.audit = get_audit_service(tenant_id)
    
    def send_sms(
        self,
        to: str,
        message: str,
        tenant_id: Optional[str] = None
    ) -> Dict:
        """
        Send SMS message
        
        Args:
            to: Phone number (E.164 format: +12345678900)
            message: Message body (160 chars max for single SMS)
            tenant_id: Tenant ID for audit logging
        
        Returns:
            Dict with message_sid, status
        """
        tenant_id = tenant_id or self.tenant_id
        try:
            # Send via Twilio
            twilio_message = self.client.messages.create(
                to=to,
                from_=self.settings.twilio_phone_number,
                body=message
            )
            
            # Log success
            audit = get_audit_service(tenant_id)
            audit.log_event(
                action="sms_sent",
                resource_type="sms",
                resource_id=twilio_message.sid,
                metadata={
                    "to": to,
                    "message_length": len(message)
                },
                trace_id=None
            )
            
            return {
                "message_sid": twilio_message.sid,
                "status": twilio_message.status,
                "to": to
            }
            
        except Exception as e:
            audit = get_audit_service(tenant_id)
            audit.log_event(
                action="sms_send_failed",
                resource_type="sms",
                metadata={
                    "error": str(e),
                    "to": to
                },
                trace_id=None
            )
            raise


# Singleton factory
_sms_services: Dict[str, SMSService] = {}

def get_sms_service(tenant_id: Optional[str] = None) -> SMSService:
    """Get SMS service instance (per tenant)"""
    key = tenant_id or "default"
    if key not in _sms_services:
        _sms_services[key] = SMSService(tenant_id=tenant_id)
    return _sms_services[key]

