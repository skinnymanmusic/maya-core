"""
OMEGA Core v3.0 - Gmail API Service
Gmail API integration for message retrieval, sending, and draft management
"""
import hashlib
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from app.database import get_cursor
from app.services.audit_service import get_audit_service
from app.config import get_settings

settings = get_settings()

# Gmail service instances (cached per tenant)
_gmail_services = {}


def _get_gmail_service(account_email: str) -> Any:
    """Get or create Gmail API service instance"""
    if account_email not in _gmail_services:
        credentials = service_account.Credentials.from_service_account_file(
            settings.google_credentials_path,
            scopes=['https://www.googleapis.com/auth/gmail.readonly', 'https://www.googleapis.com/auth/gmail.send', 'https://www.googleapis.com/auth/gmail.compose']
        )
        delegated_credentials = credentials.with_subject(account_email)
        _gmail_services[account_email] = build('gmail', 'v1', credentials=delegated_credentials)
    return _gmail_services[account_email]


def hash_email(email: str) -> str:
    """Compute SHA256 hash of email for lookup"""
    return hashlib.sha256(email.lower().strip().encode()).hexdigest()


def get_message_by_id(message_id: str, account_email: str, tenant_id: str) -> Optional[Dict[str, Any]]:
    """
    Get Gmail message by ID
    
    Args:
        message_id: Gmail message ID
        account_email: Gmail account email
        tenant_id: Tenant ID
        
    Returns:
        Message dictionary or None
    """
    try:
        service = _get_gmail_service(account_email)
        message = service.users().messages().get(userId='me', id=message_id, format='full').execute()
        return message
    except HttpError as e:
        audit = get_audit_service(tenant_id)
        audit.log_event(
            action="gmail.api.error",
            resource_type="gmail",
            resource_id=message_id,
            metadata={"error": str(e), "account_email": account_email}
        )
        return None


def store_email_in_db(
    gmail_message_id: str,
    gmail_thread_id: str,
    account_email: str,
    sender_email: str,
    sender_name: str,
    subject: str,
    body: str,
    received_at: datetime,
    tenant_id: str,
    trace_id: Optional[str] = None
) -> Optional[str]:
    """
    Store email in database
    
    Args:
        gmail_message_id: Gmail message ID
        gmail_thread_id: Gmail thread ID
        account_email: Account email
        sender_email: Sender email
        sender_name: Sender name
        subject: Email subject
        body: Email body
        received_at: Received timestamp
        tenant_id: Tenant ID
        trace_id: Request trace ID
        
    Returns:
        Email ID (UUID string) or None if duplicate
    """
    audit = get_audit_service(tenant_id)
    
    try:
        with get_cursor(tenant_id=tenant_id) as cur:
            # Check for duplicate
            cur.execute(
                "SELECT id FROM emails WHERE gmail_message_id = %s AND tenant_id = %s",
                (gmail_message_id, tenant_id)
            )
            existing = cur.fetchone()
            if existing:
                audit.log_event(
                    action="gmail.email.duplicate",
                    resource_type="email",
                    resource_id=existing[0],
                    metadata={"gmail_message_id": gmail_message_id},
                    trace_id=trace_id
                )
                return existing[0]
            
            # Insert new email
            import uuid
            email_id = str(uuid.uuid4())
            cur.execute(
                """
                INSERT INTO emails (
                    id, tenant_id, gmail_message_id, gmail_thread_id, account_email,
                    sender_email, sender_name, subject, body, received_at, processed, created_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    email_id,
                    tenant_id,
                    gmail_message_id,
                    gmail_thread_id,
                    account_email,
                    sender_email,
                    sender_name,
                    subject,
                    body,
                    received_at,
                    False,
                    datetime.now(timezone.utc),
                )
            )
            
            audit.log_event(
                action="gmail.email.stored",
                resource_type="email",
                resource_id=email_id,
                metadata={"gmail_message_id": gmail_message_id, "sender_email": sender_email},
                trace_id=trace_id
            )
            
            return email_id
            
    except Exception as e:
        audit.log_event(
            action="gmail.email.store.error",
            resource_type="email",
            metadata={"error": str(e), "gmail_message_id": gmail_message_id},
            trace_id=trace_id
        )
        return None


def create_draft(
    account_email: str,
    to: str,
    subject: str,
    body: str,
    thread_id: Optional[str] = None,
    tenant_id: str = None,
    trace_id: Optional[str] = None
) -> Optional[str]:
    """
    Create Gmail draft
    
    Args:
        account_email: Gmail account email
        to: Recipient email
        subject: Email subject
        body: Email body
        thread_id: Optional thread ID for threading
        tenant_id: Tenant ID
        trace_id: Request trace ID
        
    Returns:
        Draft ID or None
    """
    audit = get_audit_service(tenant_id or settings.default_tenant_id)
    
    try:
        service = _get_gmail_service(account_email)
        
        message = {
            'message': {
                'to': to,
                'subject': subject,
                'body': body,
            }
        }
        
        if thread_id:
            message['message']['threadId'] = thread_id
        
        draft = service.users().drafts().create(userId='me', body=message).execute()
        draft_id = draft['id']
        
        audit.log_event(
            action="gmail.draft.created",
            resource_type="gmail",
            resource_id=draft_id,
            metadata={"to": to, "subject": subject},
            trace_id=trace_id
        )
        
        return draft_id
        
    except Exception as e:
        audit.log_event(
            action="gmail.draft.create.error",
            resource_type="gmail",
            metadata={"error": str(e), "to": to},
            trace_id=trace_id
        )
        return None


def send_email(
    account_email: str,
    to: str,
    subject: str,
    body: str,
    thread_id: Optional[str] = None,
    tenant_id: str = None,
    trace_id: Optional[str] = None
) -> Optional[str]:
    """
    Send email via Gmail API
    
    Args:
        account_email: Gmail account email
        to: Recipient email
        subject: Email subject
        body: Email body
        thread_id: Optional thread ID for threading
        tenant_id: Tenant ID
        trace_id: Request trace ID
        
    Returns:
        Message ID or None
    """
    audit = get_audit_service(tenant_id or settings.default_tenant_id)
    
    try:
        service = _get_gmail_service(account_email)
        
        message = {
            'to': to,
            'subject': subject,
            'body': body,
        }
        
        if thread_id:
            message['threadId'] = thread_id
        
        sent_message = service.users().messages().send(userId='me', body={'raw': message}).execute()
        message_id = sent_message['id']
        
        audit.log_event(
            action="gmail.email.sent",
            resource_type="gmail",
            resource_id=message_id,
            metadata={"to": to, "subject": subject},
            trace_id=trace_id
        )
        
        return message_id
        
    except Exception as e:
        audit.log_event(
            action="gmail.email.send.error",
            resource_type="gmail",
            metadata={"error": str(e), "to": to},
            trace_id=trace_id
        )
        return None


def setup_watch(
    account_email: str,
    topic: str,
    tenant_id: str,
    trace_id: Optional[str] = None
) -> Optional[Dict[str, Any]]:
    """
    Set up Gmail watch subscription
    
    Args:
        account_email: Gmail account email
        topic: Pub/Sub topic
        tenant_id: Tenant ID
        trace_id: Request trace ID
        
    Returns:
        Watch response with expiration and history_id
    """
    audit = get_audit_service(tenant_id)
    
    try:
        service = _get_gmail_service(account_email)
        
        watch_request = {
            'topicName': topic,
            'labelIds': ['INBOX'],
        }
        
        watch_response = service.users().watch(userId='me', body=watch_request).execute()
        
        audit.log_event(
            action="gmail.watch.setup",
            resource_type="gmail",
            metadata={
                "account_email": account_email,
                "topic": topic,
                "expiration": watch_response.get('expiration'),
                "history_id": watch_response.get('historyId'),
            },
            trace_id=trace_id
        )
        
        return watch_response
        
    except Exception as e:
        audit.log_event(
            action="gmail.watch.setup.error",
            resource_type="gmail",
            metadata={"error": str(e), "account_email": account_email},
            trace_id=trace_id
        )
        return None

