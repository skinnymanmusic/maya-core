"""
OMEGA Core v4.0 - Agent Profile Backfill Script
Backfills tenant_agent_profiles table for existing tenants
"""
import sys
from pathlib import Path
from uuid import uuid4

# Add backend to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from app.database import get_cursor
from app.config import get_settings

settings = get_settings()

# Default agent profiles
DEFAULT_AGENTS = [
    {"agent_type": "maya", "name": "Maya Email Assistant", "is_active": True},
    {"agent_type": "nova", "name": "Nova Pricing Engine", "is_active": True},
    {"agent_type": "eli", "name": "Eli Venue Intelligence", "is_active": True},
    {"agent_type": "solin", "name": "Solin MCP", "is_active": True},
    {"agent_type": "rho", "name": "Rho Scheduling", "is_active": True},
]


def backfill_agent_profiles():
    """Backfill agent profiles for all tenants"""
    try:
        with get_cursor(tenant_id=None) as cur:
            # Get all active tenants
            cur.execute(
                """
                SELECT id FROM tenants WHERE is_active = TRUE
                """
            )
            tenants = cur.fetchall()
            
            for tenant_row in tenants:
                tenant_id = tenant_row[0]
                
                for agent in DEFAULT_AGENTS:
                    # Check if profile already exists
                    cur.execute(
                        """
                        SELECT id FROM tenant_agent_profiles
                        WHERE tenant_id = %s AND agent_type = %s
                        """,
                        (tenant_id, agent["agent_type"]),
                    )
                    if cur.fetchone():
                        continue  # Already exists
                    
                    # Create profile
                    cur.execute(
                        """
                        INSERT INTO tenant_agent_profiles (
                            id, tenant_id, agent_type, name, is_active, created_at, updated_at
                        )
                        VALUES (%s, %s, %s, %s, %s, NOW(), NOW())
                        """,
                        (uuid4(), tenant_id, agent["agent_type"], agent["name"], agent["is_active"]),
                    )
                
                cur.connection.commit()
                print(f"✅ Backfilled agents for tenant {tenant_id}")
        
        print("✅ Agent profile backfill complete")
        return True
    except Exception as e:
        print(f"❌ Backfill error: {e}")
        return False


if __name__ == "__main__":
    if backfill_agent_profiles():
        sys.exit(0)
    else:
        sys.exit(1)

