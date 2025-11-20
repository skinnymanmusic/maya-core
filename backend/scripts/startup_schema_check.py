"""
OMEGA Core v3.0 - Startup Schema Check
Validates database schema matches expected state
"""
import sys
from pathlib import Path

# Add backend to path
backend_path = Path(__file__).parent.parent
sys.path.insert(0, str(backend_path))

from app.database import get_cursor
from app.services.aegis_anomaly_service import AegisAnomalyService


def check_migrations():
    """Check if all required tables exist"""
    required_tables = [
        'tenants', 'users', 'clients', 'emails', 'calendar_events',
        'audit_log', 'sync_log', 'processed_messages', 'email_retry_queue',
        'unsafe_threads', 'repair_log', 'system_state',
        'archivus_threads', 'archivus_memories',
    ]
    
    missing_tables = []
    
    try:
        with get_cursor(tenant_id=None) as cur:
            for table in required_tables:
                cur.execute(
                    """
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables
                        WHERE table_schema = 'public'
                        AND table_name = %s
                    )
                    """,
                    (table,),
                )
                exists = cur.fetchone()[0]
                if not exists:
                    missing_tables.append(table)
    except Exception as e:
        print(f"❌ Schema check error: {e}")
        return False
    
    if missing_tables:
        print(f"❌ Missing tables: {', '.join(missing_tables)}")
        # Record schema drift in Aegis
        try:
            aegis = AegisAnomalyService()
            # Note: Aegis doesn't have record_schema_drift method yet
            # This is a placeholder
        except Exception:
            pass
        return False
    
    print("✅ All required tables exist")
    return True


def run_check():
    """Run schema check"""
    if check_migrations():
        print("✅ Schema check passed")
        sys.exit(0)
    else:
        print("❌ Schema check failed")
        sys.exit(1)


if __name__ == "__main__":
    run_check()

