"""
Payment Reminder Worker
Sends automated payment reminders for unpaid bookings
"""
import time
from datetime import datetime, timedelta, timezone
from typing import List, Dict, Optional
from app.database import get_cursor
from app.services.gmail_service import send_email
from app.services.audit_service import get_audit_service
from app.config import get_settings

settings = get_settings()


class PaymentReminderWorker:
    """Background worker for sending payment reminders"""
    
    def __init__(self, tenant_id: Optional[str] = None):
        self.tenant_id = tenant_id or settings.default_tenant_id
        self.audit = get_audit_service(self.tenant_id)
    
    def run(self):
        """
        Main worker loop
        Checks for unpaid bookings and sends reminders
        """
        while True:
            try:
                # Get all unpaid bookings
                unpaid_bookings = self._get_unpaid_bookings()
                
                for booking in unpaid_bookings:
                    days_since_created = (datetime.now(timezone.utc) - booking['created_at']).days
                    
                    # Day 3: Friendly reminder
                    if days_since_created == 3 and not booking.get('reminder_1_sent'):
                        self._send_reminder_1(booking)
                    
                    # Day 7: Second reminder with urgency
                    elif days_since_created == 7 and not booking.get('reminder_2_sent'):
                        self._send_reminder_2(booking)
                    
                    # Day 14: Final notice
                    elif days_since_created == 14 and not booking.get('reminder_3_sent'):
                        self._send_reminder_3(booking)
                
                # Sleep for 1 hour before next check
                time.sleep(3600)
                
            except Exception as e:
                self.audit.log_event(
                    action="payment_reminder_worker_error",
                    resource_type="worker",
                    metadata={"error": str(e)},
                    trace_id=None
                )
                time.sleep(60)  # Sleep 1 minute on error
    
    def _get_unpaid_bookings(self) -> List[Dict]:
        """Get all unpaid bookings"""
        with get_cursor(tenant_id=self.tenant_id) as cursor:
            cursor.execute("""
                SELECT 
                    booking_id, tenant_id, client_email, service_description,
                    event_date, payment_status, payment_amount,
                    stripe_payment_link_id, created_at,
                    reminder_1_sent, reminder_2_sent, reminder_3_sent
                FROM bookings
                WHERE payment_status = 'pending'
                AND created_at > NOW() - INTERVAL '30 days'
                ORDER BY created_at ASC
            """)
            rows = cursor.fetchall()
            return [dict(row) for row in rows]
    
    def _send_reminder_1(self, booking: Dict):
        """Send friendly reminder (Day 3)"""
        try:
            subject = f"Payment reminder for your upcoming event"
            body = f"""Hi there!

Just a friendly reminder that we're still waiting for payment for your upcoming event on {booking['event_date'].strftime('%B %d, %Y') if booking.get('event_date') else 'your scheduled date'}.

You can complete your payment securely here:
{self._get_payment_link(booking)}

If you have any questions, just reply to this email!

Thanks,
Maya
"""
            
            send_email(
                account_email=settings.maya_email,
                to=booking['client_email'],
                subject=subject,
                body=body,
                tenant_id=self.tenant_id,
                trace_id=None
            )
            
            # Mark reminder sent
            with get_cursor(tenant_id=self.tenant_id) as cursor:
                cursor.execute("""
                    UPDATE bookings
                    SET reminder_1_sent = TRUE, reminder_1_sent_at = NOW()
                    WHERE booking_id = %s AND tenant_id = %s
                """, (booking['booking_id'], self.tenant_id))
            
            self.audit.log_event(
                action="payment_reminder_1_sent",
                resource_type="booking",
                resource_id=booking['booking_id'],
                metadata={"client_email": booking['client_email']},
                trace_id=None
            )
        except Exception as e:
            self.audit.log_event(
                action="payment_reminder_1_failed",
                resource_type="booking",
                resource_id=booking['booking_id'],
                metadata={"error": str(e)},
                trace_id=None
            )
    
    def _send_reminder_2(self, booking: Dict):
        """Send urgent reminder (Day 7)"""
        try:
            subject = f"URGENT: Payment still pending for your event"
            body = f"""Hi there,

This is a reminder that payment for your upcoming event on {booking['event_date'].strftime('%B %d, %Y') if booking.get('event_date') else 'your scheduled date'} is still pending.

Please complete your payment as soon as possible:
{self._get_payment_link(booking)}

If you've already paid, please let us know and we'll update your booking status.

Thanks,
Maya
"""
            
            send_email(
                account_email=settings.maya_email,
                to=booking['client_email'],
                subject=subject,
                body=body,
                tenant_id=self.tenant_id,
                trace_id=None
            )
            
            # Mark reminder sent
            with get_cursor(tenant_id=self.tenant_id) as cursor:
                cursor.execute("""
                    UPDATE bookings
                    SET reminder_2_sent = TRUE, reminder_2_sent_at = NOW()
                    WHERE booking_id = %s AND tenant_id = %s
                """, (booking['booking_id'], self.tenant_id))
            
            self.audit.log_event(
                action="payment_reminder_2_sent",
                resource_type="booking",
                resource_id=booking['booking_id'],
                metadata={"client_email": booking['client_email']},
                trace_id=None
            )
        except Exception as e:
            self.audit.log_event(
                action="payment_reminder_2_failed",
                resource_type="booking",
                resource_id=booking['booking_id'],
                metadata={"error": str(e)},
                trace_id=None
            )
    
    def _send_reminder_3(self, booking: Dict):
        """Send final notice (Day 14)"""
        try:
            subject = f"FINAL NOTICE: Payment required to confirm your booking"
            body = f"""Hi there,

This is a final notice that payment for your upcoming event on {booking['event_date'].strftime('%B %d, %Y') if booking.get('event_date') else 'your scheduled date'} is still pending.

Your booking may be cancelled if payment is not received soon. Please complete your payment immediately:
{self._get_payment_link(booking)}

If you have any questions or concerns, please reply to this email right away.

Thanks,
Maya
"""
            
            send_email(
                account_email=settings.maya_email,
                to=booking['client_email'],
                subject=subject,
                body=body,
                tenant_id=self.tenant_id,
                trace_id=None
            )
            
            # Mark reminder sent
            with get_cursor(tenant_id=self.tenant_id) as cursor:
                cursor.execute("""
                    UPDATE bookings
                    SET reminder_3_sent = TRUE, reminder_3_sent_at = NOW()
                    WHERE booking_id = %s AND tenant_id = %s
                """, (booking['booking_id'], self.tenant_id))
            
            self.audit.log_event(
                action="payment_reminder_3_sent",
                resource_type="booking",
                resource_id=booking['booking_id'],
                metadata={"client_email": booking['client_email']},
                trace_id=None
            )
        except Exception as e:
            self.audit.log_event(
                action="payment_reminder_3_failed",
                resource_type="booking",
                resource_id=booking['booking_id'],
                metadata={"error": str(e)},
                trace_id=None
            )
    
    def _get_payment_link(self, booking: Dict) -> str:
        """Get payment link URL from booking"""
        # If we have stripe_payment_link_id, we'd need to fetch the URL from Stripe
        # For now, return a placeholder or fetch from database
        payment_link_id = booking.get('stripe_payment_link_id')
        if payment_link_id:
            # In production, fetch actual URL from Stripe API
            return f"https://checkout.stripe.com/pay/{payment_link_id}"
        return "[Payment link not available - please contact support]"


def start_worker(tenant_id: Optional[str] = None):
    """Start the payment reminder worker"""
    worker = PaymentReminderWorker(tenant_id)
    worker.run()


if __name__ == "__main__":
    start_worker()

