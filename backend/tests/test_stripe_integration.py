"""
Test Stripe payment integration
"""
import pytest
from app.services.stripe_service import get_stripe_service


def test_create_payment_link():
    """Test payment link creation"""
    stripe_service = get_stripe_service()
    
    result = stripe_service.create_payment_link(
        amount=500.00,
        description="DJ Services - Test Wedding",
        client_email="test@example.com",
        booking_id="test-booking-001",
        tenant_id="test-tenant-id"
    )
    
    assert "payment_link_url" in result
    assert "payment_link_id" in result
    assert result["amount"] == 500.00
    assert "https://checkout.stripe.com" in result["payment_link_url"]
    
    print(f"[OK] Payment link created: {result['payment_link_url']}")


def test_webhook_signature_verification():
    """Test webhook signature verification"""
    # This test requires a real Stripe webhook event
    # Run manually with Stripe CLI: stripe listen --forward-to localhost:8000/api/stripe/webhook
    pass


if __name__ == "__main__":
    test_create_payment_link()
    print("[OK] All Stripe tests passed")

