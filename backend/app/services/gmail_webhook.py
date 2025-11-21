"""
OMEGA Core v3.0 - Gmail Webhook Service
Full Google JWT verification, SHA256 fingerprinting, database locking
"""
import base64
import hashlib
import json
from typing import Dict, Any, Optional, Tuple
import jwt
from jwt import PyJWKClient
from datetime import datetime, timezone, timedelta
from app.database import get_cursor
from app.services.audit_service import get_audit_service
from app.config import get_settings

settings = get_settings()

# Google JWKS client
_jwks_client = None


def _get_jwks_client() -> PyJWKClient:
    """Get or create Google JWKS client"""
    global _jwks_client
    if _jwks_client is None:
        _jwks_client = PyJWKClient("https://www.googleapis.com/oauth2/v3/certs")
    return _jwks_client


def verify_jwt_token(token: str, tenant_id: str) -> Tuple[bool, Optional[str]]:
    """
    Verify Google JWT token from Pub/Sub
    
    Args:
        token: JWT token string
        tenant_id: Tenant ID for audit logging
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    audit = get_audit_service(tenant_id)
    
    try:
        # Decode without verification first to get header
        unverified = jwt.decode(token, options={"verify_signature": False})
        
        # Validate issuer
        iss = unverified.get("iss")
        if iss not in ["https://accounts.google.com", "accounts.google.com"]:
            error_msg = f"Invalid issuer: {iss}"
            audit.log_event(
                action="gmail.webhook.jwt.invalid",
                resource_type="webhook",
                metadata={"error": error_msg, "issuer": iss}
            )
            return False, error_msg
        
        # Validate audience
        aud = unverified.get("aud")
        if aud != settings.gmail_webhook_url:
            error_msg = f"Invalid audience: {aud}"
            audit.log_event(
                action="gmail.webhook.jwt.invalid",
                resource_type="webhook",
                metadata={"error": error_msg, "audience": aud}
            )
            return False, error_msg
        
        # Validate subject (service account)
        sub = unverified.get("sub")
        if sub != settings.gmail_pubsub_service_account:
            error_msg = f"Invalid subject: {sub}"
            audit.log_event(
                action="gmail.webhook.jwt.invalid",
                resource_type="webhook",
                metadata={"error": error_msg, "subject": sub}
            )
            return False, error_msg
        
        # Validate expiration with clock skew tolerance
        now = datetime.now(timezone.utc)
        exp = datetime.fromtimestamp(unverified.get("exp", 0), tz=timezone.utc)
        iat = datetime.fromtimestamp(unverified.get("iat", 0), tz=timezone.utc)
        
        if exp < now - timedelta(minutes=5):  # 5-minute clock skew tolerance
            error_msg = "Token expired"
            audit.log_event(
                action="gmail.webhook.jwt.invalid",
                resource_type="webhook",
                metadata={"error": error_msg, "exp": exp.isoformat(), "now": now.isoformat()}
            )
            return False, error_msg
        
        if iat > now + timedelta(minutes=5):  # Future-dated token
            error_msg = "Token issued in future"
            audit.log_event(
                action="gmail.webhook.jwt.invalid",
                resource_type="webhook",
                metadata={"error": error_msg, "iat": iat.isoformat(), "now": now.isoformat()}
            )
            return False, error_msg
        
        # Verify signature using JWKS
        jwks_client = _get_jwks_client()
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        
        jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience=settings.gmail_webhook_url,
            issuer=iss,
        )
        
        return True, None
        
    except jwt.ExpiredSignatureError:
        error_msg = "Token expired"
        audit.log_event(
            action="gmail.webhook.jwt.invalid",
            resource_type="webhook",
            metadata={"error": error_msg}
        )
        return False, error_msg
    except jwt.InvalidTokenError as e:
        error_msg = f"Invalid token: {str(e)}"
        audit.log_event(
            action="gmail.webhook.jwt.invalid",
            resource_type="webhook",
            metadata={"error": error_msg}
        )
        return False, error_msg
    except Exception as e:
        error_msg = f"JWT verification error: {str(e)}"
        audit.log_event(
            action="gmail.webhook.jwt.error",
            resource_type="webhook",
            metadata={"error": error_msg}
        )
        return False, error_msg


def compute_request_fingerprint(message_id: str, publish_time: str, data_length: int) -> str:
    """
    Compute SHA256 fingerprint for replay prevention
    
    Formula: SHA256(message_id + publish_time + data_length)
    
    Args:
        message_id: Pub/Sub message ID
        publish_time: Message publish time
        data_length: Length of message data
        
    Returns:
        SHA256 hash (hex string)
    """
    fingerprint_data = f"{message_id}{publish_time}{data_length}"
    return hashlib.sha256(fingerprint_data.encode()).hexdigest()


def parse_pubsub_message(message_data: str) -> Dict[str, Any]:
    """
    Parse Pub/Sub message with strict base64 decoding
    
    Args:
        message_data: Base64-encoded message data
        
    Returns:
        Parsed message dictionary
        
    Raises:
        ValueError: If base64 decode fails
    """
    try:
        decoded = base64.b64decode(message_data, validate=True)
        return json.loads(decoded.decode('utf-8'))
    except Exception as e:
        raise ValueError(f"Failed to parse Pub/Sub message: {str(e)}")


def check_fingerprint(fingerprint: str, tenant_id: str) -> bool:
    """
    Check if fingerprint already exists (replay detection)
    
    Args:
        fingerprint: SHA256 fingerprint
        tenant_id: Tenant ID
        
    Returns:
        True if fingerprint exists (replay detected), False otherwise
    """
    try:
        with get_cursor(tenant_id=tenant_id) as cur:
            cur.execute(
                "SELECT 1 FROM sync_log WHERE fingerprint = %s AND tenant_id = %s LIMIT 1",
                (fingerprint, tenant_id)
            )
            return cur.fetchone() is not None
    except Exception:
        # Fail-open: if check fails, allow processing
        return False


def store_fingerprint(fingerprint: str, tenant_id: str, metadata: Dict[str, Any]) -> None:
    """Store fingerprint in sync_log table"""
    try:
        with get_cursor(tenant_id=tenant_id) as cur:
            cur.execute(
                """
                INSERT INTO sync_log (tenant_id, sync_type, fingerprint, metadata, created_at)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (fingerprint) DO NOTHING
                """,
                (
                    tenant_id,
                    "gmail_webhook",
                    fingerprint,
                    json.dumps(metadata),
                    datetime.now(timezone.utc),
                )
            )
    except Exception:
        # Fail-open: fingerprint storage failure doesn't block processing
        pass


def acquire_lock(gmail_message_id: str, tenant_id: str) -> Tuple[bool, Optional[str]]:
    """
    Acquire PostgreSQL advisory lock on gmail_message_id
    
    Args:
        gmail_message_id: Gmail message ID
        tenant_id: Tenant ID
        
    Returns:
        Tuple of (lock_acquired, error_message)
    """
    try:
        # Hash message ID to get lock key
        lock_key = hash(gmail_message_id) & 0x7FFFFFFF  # Ensure positive integer
        
        with get_cursor(tenant_id=tenant_id) as cur:
            cur.execute("SELECT pg_try_advisory_lock(%s)", (lock_key,))
            acquired = cur.fetchone()[0]
            
            if not acquired:
                return False, "Lock already exists (idempotency)"
            
            return True, None
    except Exception as e:
        return False, f"Lock acquisition failed: {str(e)}"


def release_lock(gmail_message_id: str, tenant_id: str) -> None:
    """Release PostgreSQL advisory lock"""
    try:
        lock_key = hash(gmail_message_id) & 0x7FFFFFFF
        with get_cursor(tenant_id=tenant_id) as cur:
            cur.execute("SELECT pg_advisory_unlock(%s)", (lock_key,))
    except Exception:
        # Fail-open: lock release failure is logged but doesn't crash
        pass


def process_webhook_message(
    request_body: Dict[str, Any],
    tenant_id: str,
    trace_id: Optional[str] = None
) -> Tuple[bool, Optional[str], Optional[Dict[str, Any]]]:
    """
    Process Gmail webhook message with full security flow
    
    Args:
        request_body: Pub/Sub message body
        tenant_id: Tenant ID
        trace_id: Request trace ID
        
    Returns:
        Tuple of (success, error_message, parsed_message)
    """
    audit = get_audit_service(tenant_id)
    
    try:
        # Extract message data
        message = request_body.get("message", {})
        message_data = message.get("data", "")
        message_id = message.get("messageId", "")
        publish_time = message.get("publishTime", "")
        
        if not message_data:
            error_msg = "Missing message data"
            audit.log_event(
                action="gmail.webhook.parse.error",
                resource_type="webhook",
                metadata={"error": error_msg},
                trace_id=trace_id
            )
            return False, error_msg, None
        
        # Parse with strict base64 decode
        try:
            parsed = parse_pubsub_message(message_data)
        except ValueError as e:
            error_msg = f"Base64 decode error: {str(e)}"
            audit.log_event(
                action="gmail.webhook.parse.error",
                resource_type="webhook",
                metadata={"error": error_msg},
                trace_id=trace_id
            )
            return False, error_msg, None
        
        # Compute fingerprint
        data_length = len(message_data)
        fingerprint = compute_request_fingerprint(message_id, publish_time, data_length)
        
        # Check for replay
        if check_fingerprint(fingerprint, tenant_id):
            error_msg = "Replay detected"
            audit.log_event(
                action="gmail.webhook.replay.detected",
                resource_type="webhook",
                metadata={"fingerprint": fingerprint, "message_id": message_id},
                trace_id=trace_id
            )
            return False, error_msg, None
        
        # Extract gmail_message_id from parsed message
        gmail_message_id = parsed.get("emailAddress") or parsed.get("historyId") or message_id
        
        # Acquire lock
        lock_acquired, lock_error = acquire_lock(gmail_message_id, tenant_id)
        if not lock_acquired:
            audit.log_event(
                action="gmail.webhook.lock.failed",
                resource_type="webhook",
                metadata={"error": lock_error, "gmail_message_id": gmail_message_id},
                trace_id=trace_id
            )
            return False, lock_error, None
        
        try:
            # Store fingerprint
            store_fingerprint(
                fingerprint,
                tenant_id,
                {
                    "message_id": message_id,
                    "gmail_message_id": gmail_message_id,
                    "publish_time": publish_time,
                }
            )
            
            audit.log_event(
                action="gmail.webhook.processed",
                resource_type="webhook",
                resource_id=gmail_message_id,
                metadata={"fingerprint": fingerprint},
                trace_id=trace_id
            )
            
            return True, None, parsed
            
        finally:
            # Always release lock
            release_lock(gmail_message_id, tenant_id)
            
    except Exception as e:
        error_msg = f"Webhook processing error: {str(e)}"
        audit.log_event(
            action="gmail.webhook.error",
            resource_type="webhook",
            metadata={"error": error_msg},
            trace_id=trace_id
        )
        return False, error_msg, None

