"""
Stripe Configuration
Security: API keys from environment only
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class StripeSettings(BaseSettings):
    # Stripe API Keys (from .env)
    stripe_api_key: str  # Secret key (sk_live_xxx or sk_test_xxx)
    stripe_publishable_key: str  # Public key (pk_live_xxx or pk_test_xxx)
    stripe_webhook_secret: str  # Webhook signing secret
    
    # Business Settings
    business_name: str = "Skinny Man Entertainment"
    business_support_email: str = "maya@skinnymanmusic.com"
    business_return_url: str = "https://skinnymanmusic.com/booking-confirmed"
    
    # Payment Settings
    currency: str = "usd"
    payment_method_types: list = ["card", "us_bank_account"]
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        env_prefix="STRIPE_"
    )


@lru_cache()
def get_stripe_settings() -> StripeSettings:
    return StripeSettings()

