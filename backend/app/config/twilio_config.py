"""
Twilio Configuration for SMS
"""
from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class TwilioSettings(BaseSettings):
    twilio_account_sid: str
    twilio_auth_token: str
    twilio_phone_number: str  # Your Twilio number (e.g., +12345678900)
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
        env_prefix="TWILIO_"
    )


@lru_cache()
def get_twilio_settings() -> TwilioSettings:
    return TwilioSettings()

