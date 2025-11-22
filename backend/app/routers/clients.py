"""
OMEGA Core v3.0 - Clients Router
Client management endpoints with encryption and hashing
"""

from typing import List, Optional
from fastapi import APIRouter, Request, Query, HTTPException, status, Path
from pydantic import BaseModel
from slowapi import Limiter
from slowapi.util import get_remote_address

from app.config import get_settings
from app.services.supabase_service import (
    create_client as create_client_service,
    get_client_by_id,
    list_clients,
    search_client_by_email,
    update_client as update_client_service,
    delete_client as delete_client_service,
)

settings = get_settings()
router = APIRouter(prefix="/api/clients", tags=["clients"])
limiter = Limiter(key_func=get_remote_address)

# Request/Response Models
class CreateClientRequest(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    company: Optional[str] = None

class UpdateClientRequest(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    company: Optional[str] = None

class ClientResponse(BaseModel):
    id: str
    name: str
    email_hash: str
    created_at: str
    last_contact_at: Optional[str] = None

class ClientListResponse(BaseModel):
    items: List[ClientResponse]
    total: int
    limit: int
    offset: int

@router.post("/", response_model=ClientResponse)
@limiter.limit("50/minute")
async def create_client(
    request: Request,
    client_request: CreateClientRequest,
):
    """
    Create new client
    
    Security:
    - Email is hashed (SHA256) before storage
    - PII is encrypted (AES-256) before storage
    - RLS enforced (tenant isolation)
    """
    tenant_id = getattr(request.state, "tenant_id", settings.default_tenant_id)
    trace_id = getattr(request.state, "trace_id", None)
    
    try:
        client_id = create_client_service(
            name=client_request.name,
            email=client_request.email,
            phone=client_request.phone,
            company=client_request.company,
            tenant_id=tenant_id,
            trace_id=trace_id
        )
        
        # Fetch created client
        client = get_client_by_id(client_id=client_id, tenant_id=tenant_id)
        
        if not client:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to retrieve created client"
            )
        
        return ClientResponse(
            id=str(client.get("id", "")),
            name=client.get("name", ""),
            email_hash=client.get("email_hash", ""),
            created_at=client.get("created_at", "").isoformat() if client.get("created_at") else "",
            last_contact_at=client.get("last_contact_at", "").isoformat() if client.get("last_contact_at") else None,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create client: {str(e)}"
        )


@router.get("/{client_id}", response_model=ClientResponse)
@limiter.limit("100/minute")
async def get_client(
    request: Request,
    client_id: str = Path(..., description="Client ID (UUID)"),
):
    """
    Get client by ID
    """
    tenant_id = getattr(request.state, "tenant_id", settings.default_tenant_id)
    
    try:
        client = get_client_by_id(client_id=client_id, tenant_id=tenant_id)
        
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found"
            )
        
        return ClientResponse(
            id=str(client.get("id", "")),
            name=client.get("name", ""),
            email_hash=client.get("email_hash", ""),
            created_at=client.get("created_at", "").isoformat() if client.get("created_at") else "",
            last_contact_at=client.get("last_contact_at", "").isoformat() if client.get("last_contact_at") else None,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get client: {str(e)}"
        )


@router.get("/", response_model=ClientListResponse)
@limiter.limit("100/minute")
async def list_clients_endpoint(
    request: Request,
    limit: int = Query(50, ge=1, le=1000),
    offset: int = Query(0, ge=0),
):
    """
    List clients with pagination
    """
    tenant_id = getattr(request.state, "tenant_id", settings.default_tenant_id)
    
    try:
        clients, total = list_clients(
            tenant_id=tenant_id,
            limit=limit,
            offset=offset
        )
        
        items = [
            ClientResponse(
                id=str(c.get("id", "")),
                name=c.get("name", ""),
                email_hash=c.get("email_hash", ""),
                created_at=c.get("created_at", "").isoformat() if c.get("created_at") else "",
                last_contact_at=c.get("last_contact_at", "").isoformat() if c.get("last_contact_at") else None,
            )
            for c in clients
        ]
        
        return ClientListResponse(
            items=items,
            total=total,
            limit=limit,
            offset=offset
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to list clients: {str(e)}"
        )


@router.get("/search/by-email/", response_model=ClientResponse)
@limiter.limit("100/minute")
async def search_by_email(
    request: Request,
    email: str = Query(..., description="Email address to search"),
):
    """
    Search client by email (hashed lookup)
    """
    tenant_id = getattr(request.state, "tenant_id", settings.default_tenant_id)
    
    try:
        client = search_client_by_email(email=email, tenant_id=tenant_id)
        
        if not client:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found"
            )
        
        return ClientResponse(
            id=str(client.get("id", "")),
            name=client.get("name", ""),
            email_hash=client.get("email_hash", ""),
            created_at=client.get("created_at", "").isoformat() if client.get("created_at") else "",
            last_contact_at=client.get("last_contact_at", "").isoformat() if client.get("last_contact_at") else None,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to search client: {str(e)}"
        )


@router.put("/{client_id}", response_model=ClientResponse)
@limiter.limit("50/minute")
async def update_client_endpoint(
    request: Request,
    client_id: str = Path(..., description="Client ID (UUID)"),
    client_request: UpdateClientRequest = ...,
):
    """
    Update client
    """
    tenant_id = getattr(request.state, "tenant_id", settings.default_tenant_id)
    trace_id = getattr(request.state, "trace_id", None)
    
    try:
        success = update_client_service(
            client_id=client_id,
            tenant_id=tenant_id,
            name=client_request.name,
            phone=client_request.phone,
            company=client_request.company,
            trace_id=trace_id
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found"
            )
        
        # Fetch updated client
        client = get_client_by_id(client_id=client_id, tenant_id=tenant_id)
        
        return ClientResponse(
            id=str(client.get("id", "")),
            name=client.get("name", ""),
            email_hash=client.get("email_hash", ""),
            created_at=client.get("created_at", "").isoformat() if client.get("created_at") else "",
            last_contact_at=client.get("last_contact_at", "").isoformat() if client.get("last_contact_at") else None,
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to update client: {str(e)}"
        )


@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
@limiter.limit("50/minute")
async def delete_client_endpoint(
    request: Request,
    client_id: str = Path(..., description="Client ID (UUID)"),
):
    """
    Delete client
    """
    tenant_id = getattr(request.state, "tenant_id", settings.default_tenant_id)
    trace_id = getattr(request.state, "trace_id", None)
    
    try:
        success = delete_client_service(
            client_id=client_id,
            tenant_id=tenant_id,
            trace_id=trace_id
        )
        
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Client not found"
            )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to delete client: {str(e)}"
        )

