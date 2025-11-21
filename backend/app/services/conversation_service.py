"""
Conversation Service for SMS Booking Flow
Manages conversation state and message history
"""
from typing import Optional, Dict, Any, List
from datetime import datetime, date, time, timezone
from app.database import get_cursor
from app.services.audit_service import get_audit_service


class ConversationService:
    """Service for managing SMS conversations"""
    
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.audit = get_audit_service(tenant_id)
    
    def get_or_create_conversation(self, phone_number: str, trace_id: Optional[str] = None) -> Dict[str, Any]:
        """Get existing conversation or create new one"""
        with get_cursor(tenant_id=self.tenant_id) as cursor:
            # Check for existing active conversation
            cursor.execute("""
                SELECT * FROM conversations
                WHERE tenant_id = %s AND phone_number = %s
                AND conversation_state NOT IN ('completed', 'cancelled')
                ORDER BY created_at DESC
                LIMIT 1
            """, (self.tenant_id, phone_number))
            existing = cursor.fetchone()
            
            if existing:
                return dict(existing)
            
            # Create new conversation
            cursor.execute("""
                INSERT INTO conversations (
                    tenant_id, phone_number, conversation_state, created_at, updated_at
                ) VALUES (%s, %s, 'initial', NOW(), NOW())
                RETURNING *
            """, (self.tenant_id, phone_number))
            new_conv = cursor.fetchone()
            
            self.audit.log_event(
                action="conversation.created",
                resource_type="conversation",
                resource_id=str(new_conv["id"]),
                metadata={"phone_number": phone_number},
                trace_id=trace_id
            )
            
            return dict(new_conv)
    
    def update_conversation_state(
        self,
        conversation_id: str,
        state: str,
        updates: Optional[Dict[str, Any]] = None,
        trace_id: Optional[str] = None
    ) -> bool:
        """Update conversation state and optional fields"""
        try:
            update_fields = ["conversation_state = %s", "updated_at = NOW()"]
            params = [state, conversation_id, self.tenant_id]
            
            if updates:
                if "service_type" in updates:
                    update_fields.append("service_type = %s")
                    params.insert(-2, updates["service_type"])
                if "event_date" in updates:
                    update_fields.append("event_date = %s")
                    params.insert(-2, updates["event_date"])
                if "event_time" in updates:
                    update_fields.append("event_time = %s")
                    params.insert(-2, updates["event_time"])
                if "duration_hours" in updates:
                    update_fields.append("duration_hours = %s")
                    params.insert(-2, updates["duration_hours"])
                if "booking_id" in updates:
                    update_fields.append("booking_id = %s")
                    params.insert(-2, updates["booking_id"])
                if "client_email" in updates:
                    update_fields.append("client_email = %s")
                    params.insert(-2, updates["client_email"])
                if "client_name" in updates:
                    update_fields.append("client_name = %s")
                    params.insert(-2, updates["client_name"])
            
            with get_cursor(tenant_id=self.tenant_id) as cursor:
                cursor.execute(
                    f"""
                    UPDATE conversations
                    SET {', '.join(update_fields)}
                    WHERE id = %s AND tenant_id = %s
                    """,
                    params
                )
            
            self.audit.log_event(
                action="conversation.state_updated",
                resource_type="conversation",
                resource_id=conversation_id,
                metadata={"new_state": state, "updates": updates or {}},
                trace_id=trace_id
            )
            
            return True
        except Exception as e:
            self.audit.log_event(
                action="conversation.update_failed",
                resource_type="conversation",
                resource_id=conversation_id,
                metadata={"error": str(e)},
                trace_id=trace_id
            )
            return False
    
    def save_message(
        self,
        conversation_id: str,
        phone_number: str,
        body: str,
        direction: str,
        message_sid: Optional[str] = None,
        trace_id: Optional[str] = None
    ) -> Optional[str]:
        """Save SMS message to database"""
        try:
            with get_cursor(tenant_id=self.tenant_id) as cursor:
                cursor.execute("""
                    INSERT INTO sms_messages (
                        tenant_id, conversation_id, phone_number, message_sid,
                        direction, body, created_at
                    ) VALUES (%s, %s, %s, %s, %s, %s, NOW())
                    RETURNING id
                """, (self.tenant_id, conversation_id, phone_number, message_sid, direction, body))
                message_id = cursor.fetchone()[0]
                
                # Update conversation last_message_at
                cursor.execute("""
                    UPDATE conversations
                    SET last_message_at = NOW()
                    WHERE id = %s AND tenant_id = %s
                """, (conversation_id, self.tenant_id))
            
            return str(message_id)
        except Exception as e:
            self.audit.log_event(
                action="sms_message.save_failed",
                resource_type="sms_message",
                metadata={"error": str(e), "conversation_id": conversation_id},
                trace_id=trace_id
            )
            return None
    
    def get_conversation_messages(self, conversation_id: str, limit: int = 50) -> List[Dict[str, Any]]:
        """Get message history for a conversation"""
        with get_cursor(tenant_id=self.tenant_id) as cursor:
            cursor.execute("""
                SELECT * FROM sms_messages
                WHERE conversation_id = %s AND tenant_id = %s
                ORDER BY created_at ASC
                LIMIT %s
            """, (conversation_id, self.tenant_id, limit))
            rows = cursor.fetchall()
            return [dict(row) for row in rows]

