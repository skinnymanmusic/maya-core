"""
OMEGA Core v3.0 - Archivus Service
Long-term memory engine for thread summaries, client/venue profiles, and system notes
"""
from __future__ import annotations
import uuid
from typing import Dict, Any, Optional, List
from datetime import datetime, timezone
from app.database import get_cursor
from app.services.audit_service import get_audit_service
from app.services.claude_service import ClaudeService
from app.config import get_settings

settings = get_settings()


class ArchivusService:
    """
    Archivus Memory Engine
    Stores long-term patterns, thread summaries, and system notes
    """
    
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.audit = get_audit_service(tenant_id)
        self.claude = ClaudeService()
    
    def record_thread_summary(
        self,
        thread_id: str,
        raw_email_body: str,
        structured_context: Optional[Dict[str, Any]] = None,
    ) -> Optional[str]:
        """
        Summarize email thread and store in Archivus
        
        Args:
            thread_id: Gmail thread ID
            raw_email_body: Raw email body text
            structured_context: Optional context (client_id, venue_name, event_details)
            
        Returns:
            Thread summary ID or None if failed
        """
        try:
            # Generate summary using Claude
            summary_prompt = f"""Summarize this email thread in 2-3 sentences. Focus on:
- Main topic or request
- Key details (dates, locations, people)
- Any action items or decisions

Email content:
{raw_email_body[:2000]}"""
            
            # Use Claude service with proper method signature
            summary = self.claude.generate_response(
                email_body=raw_email_body[:2000],
                context={"summary_request": True, "prompt": summary_prompt},
                trace_id=None,
            )
            # Limit summary length if needed
            if summary and len(summary) > 500:
                summary = summary[:500] + "..."
            
            # Extract key points from structured context
            key_points = {}
            if structured_context:
                if structured_context.get("client_id"):
                    key_points["client_id"] = structured_context["client_id"]
                if structured_context.get("venue_name"):
                    key_points["venue_name"] = structured_context["venue_name"]
                if structured_context.get("event_date"):
                    key_points["event_date"] = structured_context["event_date"]
                if structured_context.get("event_type"):
                    key_points["event_type"] = structured_context["event_type"]
            
            # Store in database
            thread_summary_id = str(uuid.uuid4())
            with get_cursor(tenant_id=self.tenant_id) as cur:
                cur.execute(
                    """
                    INSERT INTO archivus_threads (
                        id, tenant_id, gmail_thread_id, summary, key_points,
                        client_context, venue_context, created_at, updated_at
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, NOW(), NOW())
                    ON CONFLICT (tenant_id, gmail_thread_id)
                    DO UPDATE SET
                        summary = EXCLUDED.summary,
                        key_points = EXCLUDED.key_points,
                        client_context = EXCLUDED.client_context,
                        venue_context = EXCLUDED.venue_context,
                        updated_at = NOW()
                    """,
                    (
                        thread_summary_id,
                        self.tenant_id,
                        thread_id,
                        summary,
                        key_points,
                        structured_context.get("client_context") if structured_context else None,
                        structured_context.get("venue_context") if structured_context else None,
                    ),
                )
                cur.connection.commit()
            
            self.audit.log_event(
                action="archivus.thread_summary.recorded",
                resource_type="archivus",
                resource_id=thread_summary_id,
                metadata={"thread_id": thread_id},
                tenant_id=self.tenant_id,
            )
            
            return thread_summary_id
        except Exception as e:
            # Fail-open: Archivus failures don't block email processing
            self.audit.log_event(
                action="archivus.thread_summary.error",
                resource_type="archivus",
                metadata={"error": str(e), "thread_id": thread_id},
                tenant_id=self.tenant_id,
            )
            return None
    
    def get_client_profile(self, client_id: str) -> Dict[str, Any]:
        """
        Aggregate client memories and thread summaries
        
        Args:
            client_id: Client UUID
            
        Returns:
            Aggregated client profile
        """
        try:
            with get_cursor(tenant_id=self.tenant_id) as cur:
                # Get thread summaries for this client
                cur.execute(
                    """
                    SELECT summary, key_points, created_at
                    FROM archivus_threads
                    WHERE tenant_id = %s
                      AND key_points->>'client_id' = %s
                    ORDER BY created_at DESC
                    LIMIT 10
                    """,
                    (self.tenant_id, client_id),
                )
                threads = cur.fetchall()
                
                # Get client memories
                cur.execute(
                    """
                    SELECT memory_type, key, value, confidence
                    FROM archivus_memories
                    WHERE tenant_id = %s
                      AND memory_type = 'client_profile'
                      AND key = %s
                    ORDER BY updated_at DESC
                    LIMIT 5
                    """,
                    (self.tenant_id, client_id),
                )
                memories = cur.fetchall()
                
                return {
                    "client_id": client_id,
                    "thread_summaries": [
                        {
                            "summary": t[0],
                            "key_points": t[1],
                            "created_at": t[2].isoformat() if t[2] else None,
                        }
                        for t in threads
                    ],
                    "memories": [
                        {
                            "type": m[0],
                            "key": m[1],
                            "value": m[2],
                            "confidence": m[3],
                        }
                        for m in memories
                    ],
                }
        except Exception as e:
            # Fail-open: return empty profile on error
            self.audit.log_event(
                action="archivus.client_profile.error",
                resource_type="archivus",
                metadata={"error": str(e), "client_id": client_id},
                tenant_id=self.tenant_id,
            )
            return {"client_id": client_id, "thread_summaries": [], "memories": []}
    
    def get_venue_profile(self, venue_name: str) -> Dict[str, Any]:
        """
        Aggregate venue memories and thread summaries
        
        Args:
            venue_name: Venue name
            
        Returns:
            Aggregated venue profile
        """
        try:
            with get_cursor(tenant_id=self.tenant_id) as cur:
                # Get thread summaries for this venue
                cur.execute(
                    """
                    SELECT summary, key_points, created_at
                    FROM archivus_threads
                    WHERE tenant_id = %s
                      AND key_points->>'venue_name' = %s
                    ORDER BY created_at DESC
                    LIMIT 10
                    """,
                    (self.tenant_id, venue_name),
                )
                threads = cur.fetchall()
                
                # Get venue memories
                cur.execute(
                    """
                    SELECT memory_type, key, value, confidence
                    FROM archivus_memories
                    WHERE tenant_id = %s
                      AND memory_type = 'venue_profile'
                      AND key = %s
                    ORDER BY updated_at DESC
                    LIMIT 5
                    """,
                    (self.tenant_id, venue_name),
                )
                memories = cur.fetchall()
                
                return {
                    "venue_name": venue_name,
                    "thread_summaries": [
                        {
                            "summary": t[0],
                            "key_points": t[1],
                            "created_at": t[2].isoformat() if t[2] else None,
                        }
                        for t in threads
                    ],
                    "memories": [
                        {
                            "type": m[0],
                            "key": m[1],
                            "value": m[2],
                            "confidence": m[3],
                        }
                        for m in memories
                    ],
                }
        except Exception as e:
            # Fail-open: return empty profile on error
            self.audit.log_event(
                action="archivus.venue_profile.error",
                resource_type="archivus",
                metadata={"error": str(e), "venue_name": venue_name},
                tenant_id=self.tenant_id,
            )
            return {"venue_name": venue_name, "thread_summaries": [], "memories": []}
    
    def record_system_note(
        self,
        category: str,
        summary: str,
        details: Optional[Dict[str, Any]] = None,
    ) -> Optional[str]:
        """
        Record system-level note (guardian events, Safe Mode, migrations, etc.)
        
        Args:
            category: Note category (e.g., "guardian_daemon", "safe_mode")
            summary: Brief summary
            details: Optional detailed information
            
        Returns:
            System note ID or None if failed
        """
        try:
            note_id = str(uuid.uuid4())
            with get_cursor(tenant_id=self.tenant_id) as cur:
                cur.execute(
                    """
                    INSERT INTO archivus_memories (
                        id, tenant_id, memory_type, key, value, confidence, created_at, updated_at
                    )
                    VALUES (%s, %s, 'system_note', %s, %s, 1.0, NOW(), NOW())
                    """,
                    (
                        note_id,
                        self.tenant_id,
                        category,
                        {
                            "summary": summary,
                            "details": details or {},
                        },
                    ),
                )
                cur.connection.commit()
            
            self.audit.log_event(
                action="archivus.system_note.recorded",
                resource_type="archivus",
                resource_id=note_id,
                metadata={"category": category, "summary": summary},
                tenant_id=self.tenant_id,
            )
            
            return note_id
        except Exception as e:
            # Fail-open: system note failures don't block operations
            self.audit.log_event(
                action="archivus.system_note.error",
                resource_type="archivus",
                metadata={"error": str(e), "category": category},
                tenant_id=self.tenant_id,
            )
            return None

