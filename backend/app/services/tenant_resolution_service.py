"""
OMEGA Core v4.0 - Tenant Resolution Service
Resolves tenant for SSO users and creates sessions
"""
from __future__ import annotations
import uuid
from typing import Dict, Any, Optional
from datetime import datetime, timezone
from uuid import UUID
from app.database import get_cursor
from app.config import get_settings

settings = get_settings()


class TenantResolutionService:
    """
    Tenant Resolution Service for SSO users
    Handles user creation, tenant assignment, and session management
    """
    
    def resolve_tenant_for_user(
        self,
        provider: str,
        sub: str,
        email: str,
        name: Optional[str] = None,
        domain: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Resolve tenant for SSO user
        
        Logic:
        1. Check if user exists by provider + sub
        2. If exists, get their tenant(s)
        3. If single tenant, return it
        4. If multiple tenants, return list (frontend handles selection)
        5. If new user, create user and assign to default tenant
        
        Args:
            provider: OAuth provider (GOOGLE, MICROSOFT)
            sub: Provider subject ID
            email: User email
            name: User display name
            domain: Email domain
            
        Returns:
            Dict with user_id, tenant_id (or tenant_ids list), is_new_user
        """
        try:
            with get_cursor(tenant_id=None) as cur:
                # Check if user exists by provider + sub
                cur.execute(
                    """
                    SELECT u.id, u.email, u.name
                    FROM users_v4 u
                    INNER JOIN accounts a ON a.user_id = u.id
                    WHERE a.provider = %s AND a.provider_account_id = %s
                    """,
                    (provider.lower(), sub),
                )
                user_row = cur.fetchone()
                
                if user_row:
                    # User exists - get their tenant(s)
                    user_id = user_row[0]
                    cur.execute(
                        """
                        SELECT tenant_id, role
                        FROM tenant_users
                        WHERE user_id = %s
                        ORDER BY created_at ASC
                        """,
                        (user_id,),
                    )
                    tenant_rows = cur.fetchall()
                    
                    if len(tenant_rows) == 1:
                        # Single tenant - return it
                        return {
                            'user_id': str(user_id),
                            'tenant_id': str(tenant_rows[0][0]),
                            'role': tenant_rows[0][1],
                            'tenant_ids': None,
                            'is_new_user': False,
                        }
                    elif len(tenant_rows) > 1:
                        # Multiple tenants - return list
                        return {
                            'user_id': str(user_id),
                            'tenant_id': None,
                            'tenant_ids': [str(row[0]) for row in tenant_rows],
                            'roles': {str(row[0]): row[1] for row in tenant_rows},
                            'is_new_user': False,
                        }
                    else:
                        # User exists but no tenant assignment - assign to default
                        default_tenant_id = settings.default_tenant_id
                        self._assign_user_to_tenant(user_id, default_tenant_id, 'viewer')
                        return {
                            'user_id': str(user_id),
                            'tenant_id': str(default_tenant_id),
                            'role': 'viewer',
                            'tenant_ids': None,
                            'is_new_user': False,
                        }
                else:
                    # New user - create user and assign to default tenant
                    user_id = uuid.uuid4()
                    default_tenant_id = settings.default_tenant_id
                    
                    # Create user
                    cur.execute(
                        """
                        INSERT INTO users_v4 (id, email, name, email_verified, created_at, updated_at)
                        VALUES (%s, %s, %s, TRUE, NOW(), NOW())
                        """,
                        (user_id, email, name),
                    )
                    
                    # Create account link
                    cur.execute(
                        """
                        INSERT INTO accounts (
                            id, user_id, provider, provider_account_id, 
                            access_token, refresh_token, expires_at, created_at, updated_at
                        )
                        VALUES (%s, %s, %s, %s, NULL, NULL, NULL, NOW(), NOW())
                        """,
                        (uuid.uuid4(), user_id, provider.lower(), sub),
                    )
                    
                    # Assign to default tenant
                    self._assign_user_to_tenant(user_id, default_tenant_id, 'viewer')
                    
                    cur.connection.commit()
                    
                    return {
                        'user_id': str(user_id),
                        'tenant_id': str(default_tenant_id),
                        'role': 'viewer',
                        'tenant_ids': None,
                        'is_new_user': True,
                    }
        except Exception as e:
            # Fail-open: return default tenant on error
            return {
                'user_id': None,
                'tenant_id': settings.default_tenant_id,
                'role': 'viewer',
                'tenant_ids': None,
                'is_new_user': False,
                'error': str(e),
            }
    
    def _assign_user_to_tenant(self, user_id: UUID, tenant_id: str, role: str = 'viewer') -> None:
        """Assign user to tenant with role"""
        try:
            with get_cursor(tenant_id=None) as cur:
                # Check if assignment already exists
                cur.execute(
                    """
                    SELECT id FROM tenant_users
                    WHERE user_id = %s AND tenant_id = %s
                    """,
                    (user_id, tenant_id),
                )
                if cur.fetchone():
                    # Already assigned - update role
                    cur.execute(
                        """
                        UPDATE tenant_users
                        SET role = %s, updated_at = NOW()
                        WHERE user_id = %s AND tenant_id = %s
                        """,
                        (role, user_id, tenant_id),
                    )
                else:
                    # Create new assignment
                    cur.execute(
                        """
                        INSERT INTO tenant_users (id, user_id, tenant_id, role, created_at, updated_at)
                        VALUES (%s, %s, %s, %s, NOW(), NOW())
                        """,
                        (uuid.uuid4(), user_id, tenant_id, role),
                    )
                cur.connection.commit()
        except Exception:
            # Fail-open: assignment failures don't block SSO
            pass
    
    def create_session(
        self,
        user_id: UUID,
        tenant_id: UUID,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> Optional[UUID]:
        """
        Create session for user + tenant
        
        Args:
            user_id: User UUID
            tenant_id: Tenant UUID
            metadata: Optional session metadata (provider, IP, etc.)
            
        Returns:
            Session ID or None if creation fails
        """
        try:
            session_id = uuid.uuid4()
            with get_cursor(tenant_id=None) as cur:
                cur.execute(
                    """
                    INSERT INTO sessions (
                        id, user_id, tenant_id, metadata, 
                        expires_at, created_at, updated_at
                    )
                    VALUES (%s, %s, %s, %s, NOW() + INTERVAL '30 days', NOW(), NOW())
                    """,
                    (session_id, user_id, tenant_id, metadata or {}),
                )
                cur.connection.commit()
                return session_id
        except Exception:
            # Fail-open: session creation failures don't block SSO
            return None


# Singleton instance
_tenant_resolution_service: Optional[TenantResolutionService] = None


def get_tenant_resolution_service() -> TenantResolutionService:
    """Get or create tenant resolution service instance"""
    global _tenant_resolution_service
    if _tenant_resolution_service is None:
        _tenant_resolution_service = TenantResolutionService()
    return _tenant_resolution_service

