"""
OMEGA Core v3.0 - Configuration Management
"""
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment variable support"""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Application
    app_name: str = "OMEGA Core v3.0"
    app_version: str = "3.0.0"
    debug: bool = False
    
    # Database
    database_url: str
    database_ssl: bool = True
    
    # Default Tenant
    default_tenant_id: str
    
    # JWT Authentication
    jwt_secret_key: str
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7
    
    # Encryption
    encryption_key: str  # Fernet key for AES-256
    
    # Anthropic Claude
    anthropic_api_key: str
    claude_model: str = "claude-sonnet-4-20250514"
    claude_max_tokens: int = 4096
    
    # OpenAI (Hybrid LLM)
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4o"
    
    # Google APIs
    google_credentials_path: str = "credentials/gmail-credentials.json"
    gmail_webhook_url: str
    gmail_pubsub_topic: str
    gmail_pubsub_service_account: str
    
    # Google OAuth (v4.0 SSO)
    google_oauth_client_id: Optional[str] = None
    google_oauth_client_secret: Optional[str] = None
    google_oauth_redirect_uri: Optional[str] = None
    
    # Microsoft OAuth (v4.0 SSO)
    microsoft_oauth_client_id: Optional[str] = None
    microsoft_oauth_client_secret: Optional[str] = None
    microsoft_oauth_redirect_uri: Optional[str] = None
    microsoft_oauth_tenant: str = "common"
    
    # External APIs
    nova_api_url: Optional[str] = None
    eli_api_url: Optional[str] = None
    
    # Rate Limiting
    rate_limit_per_minute: int = 100
    rate_limit_webhook_per_minute: int = 100
    rate_limit_calendar_per_minute: int = 50
    
    # Safe Mode
    safe_mode_enabled: bool = False
    safe_mode_reason: Optional[str] = None
    
    # LLM Task Routing
    use_hybrid_llm: bool = True
    hybrid_llm_fallback_enabled: bool = True

