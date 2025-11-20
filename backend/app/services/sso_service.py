"""
OMEGA Core v4.0 - SSO Service
Google and Microsoft OIDC authentication
"""
from __future__ import annotations
import httpx
from typing import Dict, Any, Optional
from urllib.parse import urlencode
from app.config import get_settings

settings = get_settings()


class SSOService:
    """
    SSO Service for Google and Microsoft OIDC authentication
    """
    
    def __init__(self):
        self.google_client_id: Optional[str] = getattr(settings, 'google_oauth_client_id', None)
        self.google_client_secret: Optional[str] = getattr(settings, 'google_oauth_client_secret', None)
        self.google_redirect_uri: Optional[str] = getattr(settings, 'google_oauth_redirect_uri', None)
        
        self.microsoft_client_id: Optional[str] = getattr(settings, 'microsoft_oauth_client_id', None)
        self.microsoft_client_secret: Optional[str] = getattr(settings, 'microsoft_oauth_client_secret', None)
        self.microsoft_redirect_uri: Optional[str] = getattr(settings, 'microsoft_oauth_redirect_uri', None)
        self.microsoft_tenant: Optional[str] = getattr(settings, 'microsoft_oauth_tenant', 'common')
    
    def get_google_auth_url(self, state: str) -> str:
        """
        Generate Google OAuth authorization URL
        
        Args:
            state: CSRF state token
            
        Returns:
            Authorization URL
            
        Raises:
            ValueError: If Google OAuth is not configured
        """
        if not self.google_client_id or not self.google_redirect_uri:
            raise ValueError("Google OAuth client ID and redirect URI must be configured")
        
        params = {
            'client_id': self.google_client_id,
            'redirect_uri': self.google_redirect_uri,
            'response_type': 'code',
            'scope': 'openid email profile',
            'state': state,
            'access_type': 'offline',
            'prompt': 'consent',
        }
        
        return f"https://accounts.google.com/o/oauth2/v2/auth?{urlencode(params)}"
    
    async def exchange_google_code(self, code: str) -> Dict[str, Any]:
        """
        Exchange Google authorization code for user info
        
        Args:
            code: Authorization code from Google
            
        Returns:
            User data dictionary with provider, sub, email, name, domain
            
        Raises:
            ValueError: If Google OAuth is not configured
            HTTPException: If token exchange fails
        """
        if not self.google_client_id or not self.google_client_secret or not self.google_redirect_uri:
            raise ValueError("Google OAuth credentials must be configured")
        
        # Exchange code for tokens
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                'https://oauth2.googleapis.com/token',
                data={
                    'code': code,
                    'client_id': self.google_client_id,
                    'client_secret': self.google_client_secret,
                    'redirect_uri': self.google_redirect_uri,
                    'grant_type': 'authorization_code',
                },
            )
            token_response.raise_for_status()
            tokens = token_response.json()
        
        # Get user info
        async with httpx.AsyncClient() as client:
            user_response = await client.get(
                'https://www.googleapis.com/oauth2/v2/userinfo',
                headers={'Authorization': f"Bearer {tokens['access_token']}"},
            )
            user_response.raise_for_status()
            user_info = user_response.json()
        
        # Extract domain from email
        email = user_info.get('email', '')
        domain = email.split('@')[1] if '@' in email else None
        
        return {
            'provider': 'GOOGLE',
            'sub': user_info.get('id'),
            'email': email,
            'name': user_info.get('name'),
            'picture': user_info.get('picture'),
            'domain': domain,
            'access_token': tokens.get('access_token'),
            'refresh_token': tokens.get('refresh_token'),
        }
    
    def get_microsoft_auth_url(self, state: str) -> str:
        """
        Generate Microsoft OAuth authorization URL
        
        Args:
            state: CSRF state token
            
        Returns:
            Authorization URL
            
        Raises:
            ValueError: If Microsoft OAuth is not configured
        """
        if not self.microsoft_client_id or not self.microsoft_redirect_uri:
            raise ValueError("Microsoft OAuth client ID and redirect URI must be configured")
        
        params = {
            'client_id': self.microsoft_client_id,
            'redirect_uri': self.microsoft_redirect_uri,
            'response_type': 'code',
            'scope': 'openid email profile',
            'state': state,
            'response_mode': 'query',
        }
        
        tenant = self.microsoft_tenant or 'common'
        return f"https://login.microsoftonline.com/{tenant}/oauth2/v2.0/authorize?{urlencode(params)}"
    
    async def exchange_microsoft_code(self, code: str) -> Dict[str, Any]:
        """
        Exchange Microsoft authorization code for user info
        
        Args:
            code: Authorization code from Microsoft
            
        Returns:
            User data dictionary with provider, sub, email, name, domain
            
        Raises:
            ValueError: If Microsoft OAuth is not configured
            HTTPException: If token exchange fails
        """
        if not self.microsoft_client_id or not self.microsoft_client_secret or not self.microsoft_redirect_uri:
            raise ValueError("Microsoft OAuth credentials must be configured")
        
        tenant = self.microsoft_tenant or 'common'
        
        # Exchange code for tokens
        async with httpx.AsyncClient() as client:
            token_response = await client.post(
                f'https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token',
                data={
                    'code': code,
                    'client_id': self.microsoft_client_id,
                    'client_secret': self.microsoft_client_secret,
                    'redirect_uri': self.microsoft_redirect_uri,
                    'grant_type': 'authorization_code',
                    'scope': 'openid email profile',
                },
                headers={'Content-Type': 'application/x-www-form-urlencoded'},
            )
            token_response.raise_for_status()
            tokens = token_response.json()
        
        # Get user info
        async with httpx.AsyncClient() as client:
            user_response = await client.get(
                'https://graph.microsoft.com/v1.0/me',
                headers={'Authorization': f"Bearer {tokens['access_token']}"},
            )
            user_response.raise_for_status()
            user_info = user_response.json()
        
        # Extract domain from email
        email = user_info.get('mail') or user_info.get('userPrincipalName', '')
        domain = email.split('@')[1] if '@' in email else None
        
        return {
            'provider': 'MICROSOFT',
            'sub': user_info.get('id'),
            'email': email,
            'name': user_info.get('displayName'),
            'picture': None,  # Microsoft Graph doesn't provide picture in basic profile
            'domain': domain,
            'access_token': tokens.get('access_token'),
            'refresh_token': tokens.get('refresh_token'),
        }


# Singleton instance
_sso_service: Optional[SSOService] = None


def get_sso_service() -> SSOService:
    """Get or create SSO service instance"""
    global _sso_service
    if _sso_service is None:
        _sso_service = SSOService()
    return _sso_service

