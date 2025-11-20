"""
OMEGA Core v3.0 - Calendar Service v3.0
Google Calendar integration with auto-blocking, conflict detection, and tenant timezone support
"""
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta, timezone
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from app.database import get_cursor
from app.services.audit_service import get_audit_service
from app.services.supabase_service import create_calendar_event, delete_event, get_calendar_event_by_google_id
from app.config import get_settings

settings = get_settings()

# Calendar service instances (cached per tenant)
_calendar_services = {}


def _get_calendar_service(account_email: str):
    """Get or create Calendar API service instance"""
    if account_email not in _calendar_services:
        credentials = service_account.Credentials.from_service_account_file(
            settings.google_credentials_path,
            scopes=['https://www.googleapis.com/auth/calendar']
        )
        delegated_credentials = credentials.with_subject(account_email)
        _calendar_services[account_email] = build('calendar', 'v3', credentials=delegated_credentials)
    return _calendar_services[account_email]


class CalendarServiceV3:
    """Calendar service with auto-blocking and conflict detection"""
    
    def __init__(self, tenant_id: str):
        self.tenant_id = tenant_id
        self.audit = get_audit_service(tenant_id)
        # Default account email - can be overridden per tenant
        self.account_email = getattr(settings, 'maya_email', 'maya@skinnymanmusic.com')
    
    def _get_tenant_timezone(self) -> str:
        """Get tenant timezone from database, default to UTC"""
        try:
            with get_cursor(tenant_id=self.tenant_id) as cur:
                cur.execute(
                    "SELECT timezone FROM tenants WHERE id = %s",
                    (self.tenant_id,)
                )
                row = cur.fetchone()
                return row[0] if row and row[0] else "UTC"
        except Exception:
            return "UTC"
    
    def _check_safe_mode(self, trace_id: Optional[str] = None) -> bool:
        """Check if Safe Mode is enabled"""
        try:
            from app.guardians.solin_mcp import get_solin_mcp
            solin = get_solin_mcp(self.tenant_id)
            if solin and solin.is_safe_mode_enabled():
                self.audit.log_event(
                    action="calendar.operation.blocked.safe_mode",
                    resource_type="calendar",
                    metadata={"reason": "Safe Mode enabled"},
                    trace_id=trace_id
                )
                return True
            return False
        except Exception:
            return False
    
    def create_event(
        self,
        title: str,
        start_time: datetime,
        end_time: datetime,
        location: Optional[str] = None,
        description: Optional[str] = None,
        client_id: Optional[str] = None,
        color_id: int = 1,
        trace_id: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Create calendar event in Google Calendar and database
        
        Args:
            title: Event title
            start_time: Start datetime
            end_time: End datetime
            location: Event location
            description: Event description
            client_id: Client ID (UUID string)
            color_id: Calendar color ID (1-11)
            trace_id: Request trace ID
            
        Returns:
            Event dictionary with id, google_event_id, or None
        """
        if self._check_safe_mode(trace_id):
            return None
        
        try:
            service = _get_calendar_service(self.account_email)
            timezone_str = self._get_tenant_timezone()
            
            event = {
                'summary': title,
                'start': {
                    'dateTime': start_time.isoformat(),
                    'timeZone': timezone_str,
                },
                'end': {
                    'dateTime': end_time.isoformat(),
                    'timeZone': timezone_str,
                },
                'colorId': str(color_id),
            }
            
            if location:
                event['location'] = location
            if description:
                event['description'] = description
            
            created_event = service.events().insert(
                calendarId='primary',
                body=event
            ).execute()
            
            google_event_id = created_event.get('id')
            
            # Store in database
            event_id = create_calendar_event(
                google_event_id=google_event_id,
                title=title,
                start_time=start_time,
                end_time=end_time,
                location=location,
                description=description,
                client_id=client_id,
                color_id=color_id,
                tenant_id=self.tenant_id,
                trace_id=trace_id
            )
            
            self.audit.log_event(
                action="calendar.event.created",
                resource_type="calendar",
                resource_id=event_id,
                metadata={"google_event_id": google_event_id, "title": title},
                trace_id=trace_id
            )
            
            return {
                "id": event_id,
                "google_event_id": google_event_id,
                "title": title,
                "start_time": start_time.isoformat(),
                "end_time": end_time.isoformat(),
            }
            
        except HttpError as e:
            self.audit.log_event(
                action="calendar.event.create.error",
                resource_type="calendar",
                metadata={"error": str(e)},
                trace_id=trace_id
            )
            return None
    
    def delete_event(
        self,
        event_id: str,
        trace_id: Optional[str] = None
    ) -> bool:
        """
        Delete calendar event from Google Calendar and database
        
        Args:
            event_id: Event ID (UUID string)
            trace_id: Request trace ID
            
        Returns:
            True if deleted, False otherwise
        """
        if self._check_safe_mode(trace_id):
            return False
        
        try:
            # Get event from database
            with get_cursor(tenant_id=self.tenant_id) as cur:
                cur.execute(
                    "SELECT google_event_id FROM calendar_events WHERE id = %s AND tenant_id = %s",
                    (event_id, self.tenant_id)
                )
                row = cur.fetchone()
                if not row:
                    return False
                
                google_event_id = row[0]
            
            # Delete from Google Calendar
            service = _get_calendar_service(self.account_email)
            service.events().delete(
                calendarId='primary',
                eventId=google_event_id
            ).execute()
            
            # Delete from database
            deleted = delete_event(event_id, self.tenant_id, trace_id)
            
            if deleted:
                self.audit.log_event(
                    action="calendar.event.deleted",
                    resource_type="calendar",
                    resource_id=event_id,
                    trace_id=trace_id
                )
            
            return deleted
            
        except HttpError as e:
            self.audit.log_event(
                action="calendar.event.delete.error",
                resource_type="calendar",
                metadata={"error": str(e), "event_id": event_id},
                trace_id=trace_id
            )
            return False
    
    def list_events(
        self,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        List calendar events in date range
        
        Args:
            start_date: Start date (default: today)
            end_date: End date (default: 30 days from start)
            limit: Maximum number of events
            offset: Offset for pagination
            
        Returns:
            List of event dictionaries
        """
        try:
            if not start_date:
                start_date = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)
            if not end_date:
                end_date = start_date + timedelta(days=30)
            
            with get_cursor(tenant_id=self.tenant_id) as cur:
                cur.execute(
                    """
                    SELECT id::text, google_event_id, title, start_time, end_time,
                           location, description, client_id::text, color_id,
                           tenant_id::text, created_at::text, updated_at::text
                    FROM calendar_events
                    WHERE tenant_id = %s
                      AND start_time >= %s
                      AND start_time <= %s
                    ORDER BY start_time ASC
                    LIMIT %s OFFSET %s
                    """,
                    (self.tenant_id, start_date, end_date, limit, offset)
                )
                rows = cur.fetchall()
                return [
                    {
                        "id": row[0],
                        "google_event_id": row[1],
                        "title": row[2],
                        "start_time": row[3].isoformat() if row[3] else None,
                        "end_time": row[4].isoformat() if row[4] else None,
                        "location": row[5],
                        "description": row[6],
                        "client_id": row[7],
                        "color_id": row[8],
                        "tenant_id": row[9],
                        "created_at": row[10],
                        "updated_at": row[11],
                    }
                    for row in rows
                ]
        except Exception:
            return []
    
    def check_availability(
        self,
        start_time: datetime,
        end_time: datetime,
        trace_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Check calendar availability for time window
        
        Args:
            start_time: Start datetime
            end_time: End datetime
            trace_id: Request trace ID
            
        Returns:
            Availability dictionary with available, has_conflict, conflict_count, conflicts
        """
        conflicts = self.detect_conflicts(start_time, end_time, trace_id)
        
        return {
            "available": not conflicts.get("has_conflict", False),
            "has_conflict": conflicts.get("has_conflict", False),
            "conflict_count": conflicts.get("conflict_count", 0),
            "conflicts": conflicts.get("conflicts", []),
        }
    
    def detect_conflicts(
        self,
        start_time: datetime,
        end_time: datetime,
        trace_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Detect calendar conflicts for time window
        
        Args:
            start_time: Start datetime
            end_time: End datetime
            trace_id: Request trace ID
            
        Returns:
            Conflict dictionary with has_conflict, conflict_count, conflicts
        """
        try:
            with get_cursor(tenant_id=self.tenant_id) as cur:
                cur.execute(
                    """
                    SELECT id::text, title, start_time, end_time
                    FROM calendar_events
                    WHERE tenant_id = %s
                      AND (
                        (start_time <= %s AND end_time > %s)
                        OR (start_time < %s AND end_time >= %s)
                        OR (start_time >= %s AND end_time <= %s)
                      )
                    ORDER BY start_time ASC
                    """,
                    (
                        self.tenant_id,
                        start_time, start_time,  # Overlap condition 1
                        end_time, end_time,      # Overlap condition 2
                        start_time, end_time,    # Overlap condition 3
                    )
                )
                rows = cur.fetchall()
                conflicts = [
                    {
                        "id": row[0],
                        "title": row[1],
                        "start_time": row[2].isoformat() if row[2] else None,
                        "end_time": row[3].isoformat() if row[3] else None,
                    }
                    for row in rows
                ]
                
                has_conflict = len(conflicts) > 0
                
                if has_conflict:
                    self.audit.log_event(
                        action="calendar.conflict.detected",
                        resource_type="calendar",
                        metadata={
                            "conflict_count": len(conflicts),
                            "start_time": start_time.isoformat(),
                            "end_time": end_time.isoformat(),
                        },
                        trace_id=trace_id
                    )
                
                return {
                    "has_conflict": has_conflict,
                    "conflict_count": len(conflicts),
                    "conflicts": conflicts,
                }
        except Exception as e:
            self.audit.log_event(
                action="calendar.conflict.detect.error",
                resource_type="calendar",
                metadata={"error": str(e)},
                trace_id=trace_id
            )
            return {"has_conflict": False, "conflict_count": 0, "conflicts": []}
    
    def auto_block_for_confirmed_gig(
        self,
        event_date: datetime,
        client_name: str,
        venue: Optional[str] = None,
        location: Optional[str] = None,
        duration_hours: float = 6.0,
        context: Optional[str] = None,
        client_id: Optional[str] = None,
        trace_id: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Auto-block time for confirmed booking
        
        Title format: "SME Booking — {Client Name}"
        Color: 4 (red)
        
        Args:
            event_date: Event date/time
            client_name: Client name
            venue: Venue name
            location: Event location
            duration_hours: Duration in hours
            context: Additional context
            client_id: Client ID (UUID string)
            trace_id: Request trace ID
            
        Returns:
            Event dictionary or None
        """
        if self._check_safe_mode(trace_id):
            return None
        
        # Check for conflicts first
        end_time = event_date + timedelta(hours=duration_hours)
        conflicts = self.detect_conflicts(event_date, end_time, trace_id)
        
        if conflicts.get("has_conflict"):
            self.audit.log_event(
                action="calendar.auto_block.skipped.conflict",
                resource_type="calendar",
                metadata={
                    "client_name": client_name,
                    "conflict_count": conflicts.get("conflict_count", 0),
                },
                trace_id=trace_id
            )
            return None
        
        # Build description
        description_parts = []
        if venue:
            description_parts.append(f"Venue: {venue}")
        if location:
            description_parts.append(f"Location: {location}")
        if context:
            description_parts.append(f"Context: {context}")
        description = "\n".join(description_parts) if description_parts else "Auto-blocked from email acceptance"
        
        # Create event with exact format
        title = f"SME Booking — {client_name}"
        
        return self.create_event(
            title=title,
            start_time=event_date,
            end_time=end_time,
            location=location or venue,
            description=description,
            client_id=client_id,
            color_id=4,  # Red
            trace_id=trace_id
        )

