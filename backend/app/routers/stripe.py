"""
Stripe Payment Router
Handles webhook callbacks and payment status checks
"""
from fastapi import APIRouter, Request, Header, HTTPException, Depends
from typing import Optional
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.services.stripe_service import get_stripe_service
from app.middleware.tenant_context import TenantContextMiddleware
from app.services.audit_service import get_audit_service
from app.database import get_cursor


router = APIRouter(prefix="/api/stripe", tags=["stripe"])
limiter = Limiter(key_func=get_remote_address)


@router.post("/webhook")
@limiter.limit("100/minute")
async def stripe_webhook(
    request: Request,
    stripe_signature: Optional[str] = Header(None, alias="Stripe-Signature")
):
    """
    Stripe webhook endpoint
    Security: Verifies webhook signature
    
    Handles:
    - payment_intent.succeeded
    - payment_intent.payment_failed
    - charge.refunded
    """
    if not stripe_signature:
        raise HTTPException(status_code=400, detail="Missing Stripe-Signature header")
    
    stripe_service = get_stripe_service()
    
    # Get raw body for signature verification
    body = await request.body()
    
    # Verify webhook signature
    event = stripe_service.verify_webhook_signature(body, stripe_signature)
    
    # Get tenant_id from event metadata
    tenant_id = event["data"]["object"]["metadata"].get("tenant_id")
    if not tenant_id:
        raise HTTPException(status_code=400, detail="Missing tenant_id in metadata")
    
    # Process event
    if event["type"] == "payment_intent.succeeded":
        result = stripe_service.process_payment_success(event, tenant_id)
        return {"status": "success", "data": result}
    
    elif event["type"] == "payment_intent.payment_failed":
        # TODO: Handle failed payments
        audit = get_audit_service(tenant_id)
        audit.log_event(
            action="payment_failed",
            resource_type="payment",
            metadata={"event_id": event["id"]},
            trace_id=None
        )
        return {"status": "acknowledged", "event": "payment_failed"}
    
    elif event["type"] == "charge.refunded":
        # TODO: Handle refunds
        audit = get_audit_service(tenant_id)
        audit.log_event(
            action="charge_refunded",
            resource_type="payment",
            metadata={"event_id": event["id"]},
            trace_id=None
        )
        return {"status": "acknowledged", "event": "charge_refunded"}
    
    else:
        # Unknown event type
        return {"status": "ignored", "event_type": event["type"]}


@router.get("/payment-status/{booking_id}")
@limiter.limit("100/minute")
async def get_payment_status(
    request: Request,
    booking_id: str,
):
    """
    Check payment status for a booking
    """
    tenant_id = getattr(request.state, "tenant_id", None)
    if not tenant_id:
        raise HTTPException(status_code=400, detail="Missing tenant_id")
    stripe_service = get_stripe_service(tenant_id)
    
    # Query database for payment status
    with get_cursor(tenant_id=tenant_id) as cursor:
        cursor.execute(
            """
            SELECT 
                booking_id,
                payment_status,
                payment_amount,
                payment_timestamp,
                stripe_payment_intent_id
            FROM bookings
            WHERE booking_id = %s AND tenant_id = %s
            """,
            (booking_id, tenant_id)
        )
        result = cursor.fetchone()
    
    if not result:
        raise HTTPException(status_code=404, detail="Booking not found")
    
    return {
        "booking_id": result["booking_id"],
        "payment_status": result["payment_status"],
        "payment_amount": float(result["payment_amount"]) if result["payment_amount"] else None,
        "payment_timestamp": result["payment_timestamp"].isoformat() if result["payment_timestamp"] else None,
        "stripe_payment_intent_id": result["stripe_payment_intent_id"]
    }

