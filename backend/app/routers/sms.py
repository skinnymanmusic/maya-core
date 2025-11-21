"""
SMS Router for Twilio Webhooks
Handles incoming SMS messages and booking flow
"""
from fastapi import APIRouter, Request, Form, HTTPException
from typing import Optional, Dict, Any
from datetime import datetime, date, time, timezone
from twilio.request_validator import RequestValidator
from twilio.twiml.messaging_response import MessagingResponse

from app.services.sms_service import get_sms_service
from app.services.conversation_service import ConversationService
from app.services.booking_service import BookingService
from app.config.twilio_config import get_twilio_settings
from app.services.audit_service import get_audit_service
from app.middleware.tenant_context import TenantContextMiddleware
from app.config import get_settings

settings = get_settings()
router = APIRouter(prefix="/api/sms", tags=["sms"])


@router.post("/receive")
async def receive_sms(
    request: Request,
    From: str = Form(...),
    Body: str = Form(...),
    MessageSid: str = Form(...)
):
    """
    Twilio webhook for incoming SMS
    
    Twilio sends POST with form data:
    - From: Phone number
    - Body: Message text
    - MessageSid: Unique message ID
    """
    # Verify request is from Twilio
    twilio_settings = get_twilio_settings()
    validator = RequestValidator(twilio_settings.twilio_auth_token)
    
    # Get request URL and form data
    url = str(request.url)
    form_data = await request.form()
    
    # Verify signature
    signature = request.headers.get("X-Twilio-Signature", "")
    if not validator.validate(url, dict(form_data), signature):
        raise HTTPException(status_code=403, detail="Invalid Twilio signature")
    
    # Get tenant_id from request state (set by middleware)
    tenant_id = getattr(request.state, "tenant_id", settings.default_tenant_id)
    
    # Log incoming SMS
    audit = get_audit_service(tenant_id)
    audit.log_event(
        action="sms_received",
        resource_type="sms",
        resource_id=MessageSid,
        metadata={
            "from": From,
            "body_length": len(Body)
        },
        trace_id=None
    )
    
    # Process message through booking flow
    conversation_service = ConversationService(tenant_id)
    booking_service = BookingService(tenant_id)
    sms_service = get_sms_service(tenant_id)
    
    # Get or create conversation
    conversation = conversation_service.get_or_create_conversation(From)
    
    # Save incoming message
    conversation_service.save_message(
        conversation_id=str(conversation["id"]),
        phone_number=From,
        body=Body,
        direction="inbound",
        message_sid=MessageSid
    )
    
    # Process message based on conversation state
    response_message = _process_booking_message(
        conversation=conversation,
        message_body=Body,
        conversation_service=conversation_service,
        booking_service=booking_service,
        phone_number=From
    )
    
    # Send response
    try:
        result = sms_service.send_sms(
            to=From,
            message=response_message,
            tenant_id=tenant_id
        )
        
        # Save outgoing message
        conversation_service.save_message(
            conversation_id=str(conversation["id"]),
            phone_number=From,
            body=response_message,
            direction="outbound",
            message_sid=result.get("message_sid")
        )
    except Exception as e:
        # Log error but don't fail webhook
        audit.log_event(
            action="sms_response_failed",
            resource_type="sms",
            metadata={"error": str(e)},
            trace_id=None
        )
        response_message = "Sorry, there was an error processing your message. Please try again later."
    
    # Return TwiML response (Twilio expects XML)
    response = MessagingResponse()
    response.message(response_message)
    return str(response)


def _process_booking_message(
    conversation: Dict[str, Any],
    message_body: str,
    conversation_service: ConversationService,
    booking_service: BookingService,
    phone_number: str
) -> str:
    """
    Process SMS message based on conversation state
    
    Returns response message to send
    """
    state = conversation.get("conversation_state", "initial")
    body_lower = message_body.lower().strip()
    
    if state == "initial":
        # Check if user wants to book
        if any(word in body_lower for word in ["book", "appointment", "schedule", "reserve"]):
            conversation_service.update_conversation_state(
                str(conversation["id"]),
                "service_selected",
                {"service_type": "beauty_service"}  # Default for SMS flow
            )
            return "Great! What service would you like? (e.g., Nail appointment, Hair cut, etc.)"
        else:
            return "Hi! Thanks for reaching out. Reply with 'book' to schedule an appointment, or ask me anything!"
    
    elif state == "service_selected":
        # Extract service type
        service_type = message_body.strip()
        conversation_service.update_conversation_state(
            str(conversation["id"]),
            "date_selected",
            {"service_type": service_type}
        )
        return f"Perfect! {service_type} it is. What date works for you? (e.g., March 15th or 3/15)"
    
    elif state == "date_selected":
        # Try to extract date (simplified - can be enhanced)
        # For now, accept the message as date
        from datetime import datetime, timezone
        try:
            # Simple date parsing (can be enhanced with dateutil)
            event_date = datetime.now(timezone.utc).date()  # Placeholder - would parse from message
            conversation_service.update_conversation_state(
                str(conversation["id"]),
                "time_selected",
                {"event_date": event_date}
            )
            return f"Got it! What time works for you? (e.g., 2pm or 14:00)"
        except Exception:
            return "I didn't understand that date. Please try again (e.g., March 15th or 3/15)"
    
    elif state == "time_selected":
        # Try to extract time
        from datetime import time
        try:
            # Simple time parsing (can be enhanced)
            event_time = time(14, 0)  # Placeholder - would parse from message
            duration_hours = 1.0  # Default for beauty services
            
            # Get event_date from conversation or use today
            conv_event_date = conversation.get("event_date")
            if isinstance(conv_event_date, date):
                event_date = conv_event_date
            elif isinstance(conv_event_date, datetime):
                event_date = conv_event_date.date()
            else:
                event_date = datetime.now(timezone.utc).date()
            
            # Check availability
            availability = booking_service.check_availability(
                event_date=event_date,
                event_time=event_time,
                duration_hours=duration_hours
            )
            
            if not availability["available"]:
                return f"Sorry, that time slot has {availability['conflict_count']} conflict(s). Please choose another time."
            
            # Update conversation
            conversation_service.update_conversation_state(
                str(conversation["id"]),
                "confirmed",
                {
                    "event_time": event_time,
                    "duration_hours": duration_hours
                }
            )
            
            # Create booking
            updated_conv = conversation_service.get_or_create_conversation(phone_number)
            booking_id = booking_service.create_booking_from_conversation(updated_conv)
            
            if booking_id:
                # Create payment link
                payment_link = booking_service.create_payment_link_for_booking(
                    booking_id=booking_id,
                    amount=79.00,  # Default beauty service price
                    client_email=conversation.get("client_email")
                )
                
                if payment_link:
                    conversation_service.update_conversation_state(
                        str(conversation["id"]),
                        "completed",
                        {"booking_id": booking_id}
                    )
                    return f"Perfect! Your appointment is confirmed. Complete your payment here: {payment_link}"
                else:
                    return "Your appointment is confirmed! We'll send you a payment link shortly."
            else:
                return "There was an error creating your booking. Please contact us directly."
        
        except Exception as e:
            return "I didn't understand that time. Please try again (e.g., 2pm or 14:00)"
    
    else:
        return "Thanks for your message! We'll get back to you soon."


@router.post("/send")
async def send_sms_endpoint(
    request: Request,
    to: str = Form(...),
    message: str = Form(...)
):
    """
    Send SMS message (admin endpoint)
    """
    tenant_id = getattr(request.state, "tenant_id", settings.default_tenant_id)
    sms_service = get_sms_service(tenant_id)
    
    try:
        result = sms_service.send_sms(
            to=to,
            message=message,
            tenant_id=tenant_id
        )
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"SMS send failed: {str(e)}")

