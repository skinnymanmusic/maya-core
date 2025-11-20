"""
OMEGA Core v3.0 - Supabase/PostgreSQL Service
Database operations for emails, clients, calendar events
"""
import uuid
from typing import Optional, Dict, Any, List
from datetime import datetime, timezone
from app.database import get_cursor
from app.encryption import encrypt, decrypt
from app.services.audit_service import get_audit_service
from app.config import get_settings

settings = get_settings()


def get_email_by_id(email_id: str, tenant_id: str) -> Optional[Dict[str, Any]]:
    """Get email by ID"""
    try:
        with get_cursor(tenant_id=tenant_id) as cur:
            cur.execute(
                "SELECT * FROM emails WHERE id = %s AND tenant_id = %s",
                (email_id, tenant_id)
            )
            row = cur.fetchone()
            if row:
                return dict(row)
            return None
    except Exception:
        return None


def mark_email_processed(email_id: str, tenant_id: str) -> bool:
    """Mark email as processed"""
    try:
        with get_cursor(tenant_id=tenant_id) as cur:
            cur.execute(
                "UPDATE emails SET processed = TRUE, processed_at = %s WHERE id = %s AND tenant_id = %s",
                (datetime.now(timezone.utc), email_id, tenant_id)
            )
            return cur.rowcount > 0
    except Exception:
        return False


def get_client_by_email_hash(email_hash: str, tenant_id: str) -> Optional[Dict[str, Any]]:
    """Get client by email hash"""
    try:
        with get_cursor(tenant_id=tenant_id) as cur:
            cur.execute(
                "SELECT * FROM clients WHERE email_hash = %s AND tenant_id = %s",
                (email_hash, tenant_id)
            )
            row = cur.fetchone()
            if row:
                client = dict(row)
                # Decrypt PII fields
                if client.get('name'):
                    client['name'] = decrypt(client['name'])
                if client.get('email'):
                    client['email'] = decrypt(client['email'])
                if client.get('phone'):
                    client['phone'] = decrypt(client['phone'])
                if client.get('company'):
                    client['company'] = decrypt(client['company'])
                return client
            return None
    except Exception:
        return None


def create_or_update_client(
    email: str,
    name: Optional[str] = None,
    phone: Optional[str] = None,
    company: Optional[str] = None,
    tenant_id: str = None,
    trace_id: Optional[str] = None
) -> Optional[str]:
    """Create or update client record"""
    from app.services.gmail_service import hash_email
    
    tenant_id = tenant_id or settings.default_tenant_id
    audit = get_audit_service(tenant_id)
    email_hash = hash_email(email)
    
    try:
        with get_cursor(tenant_id=tenant_id) as cur:
            # Check if exists
            cur.execute(
                "SELECT id FROM clients WHERE email_hash = %s AND tenant_id = %s",
                (email_hash, tenant_id)
            )
            existing = cur.fetchone()
            
            if existing:
                client_id = existing[0]
                # Update
                updates = []
                params = []
                if name:
                    updates.append("name = %s")
                    params.append(encrypt(name))
                if phone:
                    updates.append("phone = %s")
                    params.append(encrypt(phone))
                if company:
                    updates.append("company = %s")
                    params.append(encrypt(company))
                
                if updates:
                    updates.append("updated_at = %s")
                    params.append(datetime.now(timezone.utc))
                    params.extend([client_id, tenant_id])
                    cur.execute(
                        f"UPDATE clients SET {', '.join(updates)} WHERE id = %s AND tenant_id = %s",
                        params
                    )
            else:
                # Create
                client_id = str(uuid.uuid4())
                cur.execute(
                    """
                    INSERT INTO clients (
                        id, tenant_id, name, email, email_hash, phone, company, created_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """,
                    (
                        client_id,
                        tenant_id,
                        encrypt(name) if name else None,
                        encrypt(email),
                        email_hash,
                        encrypt(phone) if phone else None,
                        encrypt(company) if company else None,
                        datetime.now(timezone.utc),
                    )
                )
            
            audit.log_event(
                action="client.created_or_updated",
                resource_type="client",
                resource_id=client_id,
                metadata={"email_hash": email_hash},
                trace_id=trace_id
            )
            
            return client_id
            
    except Exception as e:
        audit.log_event(
            action="client.create.error",
            resource_type="client",
            metadata={"error": str(e), "email_hash": email_hash},
            trace_id=trace_id
        )
        return None


def update_client_last_contact(client_id: str, tenant_id: str) -> None:
    """Update client last_contact_at timestamp"""
    try:
        with get_cursor(tenant_id=tenant_id) as cur:
            cur.execute(
                "UPDATE clients SET last_contact_at = %s WHERE id = %s AND tenant_id = %s",
                (datetime.now(timezone.utc), client_id, tenant_id)
            )
    except Exception:
        pass


def get_calendar_event_by_google_id(google_event_id: str, tenant_id: str) -> Optional[Dict[str, Any]]:
    """Get calendar event by Google event ID"""
    try:
        with get_cursor(tenant_id=tenant_id) as cur:
            cur.execute(
                "SELECT * FROM calendar_events WHERE google_event_id = %s AND tenant_id = %s",
                (google_event_id, tenant_id)
            )
            row = cur.fetchone()
            if row:
                return dict(row)
            return None
    except Exception:
        return None


def create_calendar_event(
    google_event_id: str,
    title: str,
    start_time: datetime,
    end_time: datetime,
    location: Optional[str] = None,
    description: Optional[str] = None,
    client_id: Optional[str] = None,
    color_id: int = 1,
    tenant_id: str = None,
    trace_id: Optional[str] = None
) -> Optional[str]:
    """Create calendar event in database"""
    tenant_id = tenant_id or settings.default_tenant_id
    audit = get_audit_service(tenant_id)
    
    try:
        event_id = str(uuid.uuid4())
        with get_cursor(tenant_id=tenant_id) as cur:
            cur.execute(
                """
                INSERT INTO calendar_events (
                    id, tenant_id, google_event_id, title, start_time, end_time,
                    location, description, client_id, color_id, created_at
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    event_id,
                    tenant_id,
                    google_event_id,
                    title,
                    start_time,
                    end_time,
                    location,
                    description,
                    client_id,
                    color_id,
                    datetime.now(timezone.utc),
                )
            )
        
        audit.log_event(
            action="calendar.event.created",
            resource_type="calendar",
            resource_id=event_id,
            metadata={"google_event_id": google_event_id, "title": title},
            trace_id=trace_id
        )
        
        return event_id
        
    except Exception as e:
        audit.log_event(
            action="calendar.event.create.error",
            resource_type="calendar",
            metadata={"error": str(e), "google_event_id": google_event_id},
            trace_id=trace_id
        )
        return None


def delete_event(event_id: str, tenant_id: str, trace_id: Optional[str] = None) -> bool:
    """Delete calendar event from database"""
    audit = get_audit_service(tenant_id)
    
    try:
        with get_cursor(tenant_id=tenant_id) as cur:
            cur.execute(
                "DELETE FROM calendar_events WHERE id = %s AND tenant_id = %s",
                (event_id, tenant_id)
            )
            deleted = cur.rowcount > 0
            
            if deleted:
                audit.log_event(
                    action="calendar.event.deleted",
                    resource_type="calendar",
                    resource_id=event_id,
                    trace_id=trace_id
                )
            
            return deleted
    except Exception as e:
        audit.log_event(
            action="calendar.event.delete.error",
            resource_type="calendar",
            metadata={"error": str(e), "event_id": event_id},
            trace_id=trace_id
        )
        return False


def get_thread_emails(thread_id: str, tenant_id: str, limit: int = 50) -> List[Dict[str, Any]]:
    """Get all emails in a thread"""
    try:
        with get_cursor(tenant_id=tenant_id) as cur:
            cur.execute(
                """
                SELECT * FROM emails
                WHERE gmail_thread_id = %s AND tenant_id = %s
                ORDER BY received_at ASC
                LIMIT %s
                """,
                (thread_id, tenant_id, limit)
            )
            return [dict(row) for row in cur.fetchall()]
    except Exception:
        return []

