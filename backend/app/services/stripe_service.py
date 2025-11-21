"""
Stripe Payment Service
Handles payment link creation, webhook processing, and payment status
"""
import stripe
from typing import Dict, Optional, List
from datetime import datetime, timezone
from fastapi import HTTPException

from app.config.stripe_config import get_stripe_settings
from app.services.audit_service import get_audit_service
from app.database import get_cursor


class StripeService:
    def __init__(self, tenant_id: Optional[str] = None):
        self.settings = get_stripe_settings()
        stripe.api_key = self.settings.stripe_api_key
        self.tenant_id = tenant_id
        self.audit = get_audit_service(tenant_id)
    
    def create_payment_link(
        self,
        amount: float,
        description: str,
        client_email: str,
        booking_id: str,
        tenant_id: str
    ) -> Dict:
        """
        Create a Stripe Payment Link for a booking
        
        Args:
            amount: Amount in USD (e.g., 500.00)
            description: Service description (e.g., "DJ Services - Wedding Reception")
            client_email: Client's email for receipt
            booking_id: Unique booking identifier
            tenant_id: Tenant ID for multi-tenant isolation
        
        Returns:
            Dict with payment_link_url, payment_link_id, expires_at
        """
        try:
            # Convert amount to cents
            amount_cents = int(amount * 100)
            
            # Create Price object (one-time payment)
            price = stripe.Price.create(
                unit_amount=amount_cents,
                currency=self.settings.currency,
                product_data={
                    "name": description,
                    "metadata": {
                        "booking_id": booking_id,
                        "tenant_id": tenant_id
                    }
                }
            )
            
            # Create Payment Link
            payment_link = stripe.PaymentLink.create(
                line_items=[{
                    "price": price.id,
                    "quantity": 1
                }],
                after_completion={
                    "type": "redirect",
                    "redirect": {
                        "url": f"{self.settings.business_return_url}?booking_id={booking_id}"
                    }
                },
                metadata={
                    "booking_id": booking_id,
                    "tenant_id": tenant_id,
                    "client_email": client_email
                },
                invoice_creation={
                    "enabled": True,
                    "invoice_data": {
                        "description": description,
                        "metadata": {
                            "booking_id": booking_id,
                            "tenant_id": tenant_id
                        }
                    }
                }
            )
            
            # Log creation
            self.audit.log_event(
                action="payment_link_created",
                resource_type="payment_link",
                resource_id=payment_link.id,
                metadata={
                    "amount": amount,
                    "booking_id": booking_id,
                    "client_email": client_email
                },
                trace_id=None
            )
            
            return {
                "payment_link_url": payment_link.url,
                "payment_link_id": payment_link.id,
                "amount": amount,
                "expires_at": None  # Payment links don't expire by default
            }
            
        except stripe.error.StripeError as e:
            self.audit.log_event(
                action="payment_link_creation_failed",
                resource_type="payment_link",
                metadata={
                    "error": str(e),
                    "booking_id": booking_id
                },
                trace_id=None
            )
            raise HTTPException(status_code=500, detail=f"Payment link creation failed: {str(e)}")
    
    def verify_webhook_signature(
        self,
        payload: bytes,
        signature: str
    ) -> Dict:
        """
        Verify Stripe webhook signature
        Security: Prevents webhook spoofing attacks
        
        Args:
            payload: Raw request body
            signature: Stripe-Signature header
        
        Returns:
            Verified event object
        """
        try:
            event = stripe.Webhook.construct_event(
                payload,
                signature,
                self.settings.stripe_webhook_secret
            )
            return event
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid payload")
        except stripe.error.SignatureVerificationError:
            raise HTTPException(status_code=400, detail="Invalid signature")
    
    def process_payment_success(
        self,
        event: Dict,
        tenant_id: str
    ) -> Dict:
        """
        Process successful payment webhook
        
        Updates:
        - Booking status → "paid"
        - Payment timestamp
        - Invoice URL
        - Sends confirmation email
        """
        try:
            # Extract payment data
            payment_intent = event["data"]["object"]
            booking_id = payment_intent["metadata"].get("booking_id")
            amount_paid = payment_intent["amount_received"] / 100  # Convert from cents
            
            if not booking_id:
                audit = get_audit_service(tenant_id)
                audit.log_event(
                    action="payment_missing_booking_id",
                    resource_type="payment",
                    metadata={"payment_intent_id": payment_intent["id"]},
                    trace_id=None
                )
                return {"status": "error", "message": "No booking_id in metadata"}
            
            # Update booking in database
            with get_cursor(tenant_id=tenant_id) as cursor:
                cursor.execute(
                    """
                    UPDATE bookings
                    SET 
                        payment_status = 'paid',
                        payment_amount = %s,
                        payment_timestamp = NOW(),
                        stripe_payment_intent_id = %s,
                        updated_at = NOW()
                    WHERE booking_id = %s AND tenant_id = %s
                    RETURNING booking_id, payment_status, payment_amount
                    """,
                    (amount_paid, payment_intent["id"], booking_id, tenant_id)
                )
                update_result = cursor.fetchone()
            
            if not update_result:
                audit = get_audit_service(tenant_id)
                audit.log_event(
                    action="payment_booking_not_found",
                    resource_type="payment",
                    metadata={
                        "booking_id": booking_id,
                        "payment_intent_id": payment_intent["id"]
                    },
                    trace_id=None
                )
                return {"status": "error", "message": "Booking not found"}
            
            # Log success
            audit = get_audit_service(tenant_id)
            audit.log_event(
                action="payment_completed",
                resource_type="payment",
                resource_id=payment_intent["id"],
                metadata={
                    "booking_id": booking_id,
                    "amount": amount_paid
                },
                trace_id=None
            )
            
            # TODO: Send confirmation email via Maya
            # TODO: Sync to QuickBooks via Nova
            
            return {
                "status": "success",
                "booking_id": booking_id,
                "amount_paid": amount_paid
            }
            
        except Exception as e:
            audit = get_audit_service(tenant_id)
            audit.log_event(
                action="payment_processing_error",
                resource_type="payment",
                metadata={"error": str(e)},
                trace_id=None
            )
            raise HTTPException(status_code=500, detail=f"Payment processing failed: {str(e)}")


# Singleton factory
_stripe_services: Dict[str, StripeService] = {}

def get_stripe_service(tenant_id: Optional[str] = None) -> StripeService:
    """Get Stripe service instance (per tenant)"""
    key = tenant_id or "default"
    if key not in _stripe_services:
        _stripe_services[key] = StripeService(tenant_id=tenant_id)
    return _stripe_services[key]

