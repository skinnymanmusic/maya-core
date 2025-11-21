"""
Booking Service for SMS Booking Flow
Manages booking state machine and calendar integration
"""
from typing import Optional, Dict, Any
from datetime import datetime, date, time, timezone
from app.database import get_cursor
from app.services.audit_service import get_audit_service
from app.services.calendar_service_v3 import CalendarServiceV3
from app.services.stripe_service import get_stripe_service


class BookingService:
    """Service for managing SMS bookings"""
    
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.audit = get_audit_service(tenant_id)
        self.calendar = CalendarServiceV3(tenant_id)
    
    def create_booking_from_conversation(
        self,
        conversation: Dict[str, Any],
        trace_id: Optional[str] = None
    ) -> Optional[str]:
        """Create booking record from conversation"""
        try:
            import time
            booking_id = f"booking-sms-{conversation['phone_number'].replace('+', '').replace('-', '')}-{int(time.time())}"
            
            with get_cursor(tenant_id=self.tenant_id) as cursor:
                cursor.execute("""
                    INSERT INTO bookings (
                        booking_id, tenant_id, client_email, service_description,
                        event_date, event_location, payment_status, created_at, updated_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, 'pending', NOW(), NOW())
                    RETURNING booking_id
                """, (
                    booking_id,
                    self.tenant_id,
                    conversation.get("client_email"),
                    f"{conversation.get('service_type', 'Service')} - SMS Booking",
                    conversation.get("event_date"),
                    conversation.get("event_location"),
                ))
                result = cursor.fetchone()
                
                if result:
                    self.audit.log_event(
                        action="booking.created_from_sms",
                        resource_type="booking",
                        resource_id=booking_id,
                        metadata={"conversation_id": str(conversation["id"])},
                        trace_id=trace_id
                    )
                    return booking_id
            
            return None
        except Exception as e:
            self.audit.log_event(
                action="booking.creation_failed",
                resource_type="booking",
                metadata={"error": str(e), "conversation_id": str(conversation.get("id"))},
                trace_id=trace_id
            )
            return None
    
    def check_availability(
        self,
        event_date: date,
        event_time: time,
        duration_hours: float,
        trace_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """Check calendar availability for booking"""
        try:
            # Combine date and time into datetime
            start_time = datetime.combine(event_date, event_time).replace(tzinfo=timezone.utc)
            # Calculate end time using timedelta
            end_time = start_time + timedelta(hours=duration_hours)
            
            conflicts = self.calendar.check_availability(
                start_time=start_time,
                end_time=end_time,
                trace_id=trace_id
            )
            
            has_conflict = len(conflicts) > 0
            
            return {
                "available": not has_conflict,
                "has_conflict": has_conflict,
                "conflict_count": len(conflicts),
                "conflicts": conflicts
            }
        except Exception as e:
            self.audit.log_event(
                action="booking.availability_check_failed",
                resource_type="booking",
                metadata={"error": str(e)},
                trace_id=trace_id
            )
            return {
                "available": False,
                "has_conflict": True,
                "conflict_count": 0,
                "conflicts": []
            }
    
    def create_payment_link_for_booking(
        self,
        booking_id: str,
        amount: float,
        client_email: Optional[str] = None,
        trace_id: Optional[str] = None
    ) -> Optional[str]:
        """Create Stripe payment link for booking"""
        try:
            stripe_service = get_stripe_service(self.tenant_id)
            if not stripe_service:
                return None
            
            payment_result = stripe_service.create_payment_link(
                amount=amount,
                description=f"SMS Booking - {booking_id}",
                client_email=client_email or "",
                booking_id=booking_id,
                tenant_id=self.tenant_id
            )
            
            # Update booking with payment link
            with get_cursor(tenant_id=self.tenant_id) as cursor:
                cursor.execute("""
                    UPDATE bookings
                    SET stripe_payment_link_id = %s, updated_at = NOW()
                    WHERE booking_id = %s AND tenant_id = %s
                """, (payment_result.get("payment_link_id"), booking_id, self.tenant_id))
            
            return payment_result.get("payment_link_url")
        except Exception as e:
            self.audit.log_event(
                action="booking.payment_link_creation_failed",
                resource_type="booking",
                resource_id=booking_id,
                metadata={"error": str(e)},
                trace_id=trace_id
            )
            return None

