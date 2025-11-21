"""
Phase 0: Email Search Fix
Adds email_hash column to clients table and backfills existing records
"""
import sys
import os
import hashlib
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

# Import database directly to avoid config loading issues
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

# Load .env file
load_dotenv()

def hash_email(email: str) -> str:
    """Compute SHA256 hash of email for lookup"""
    return hashlib.sha256(email.lower().strip().encode()).hexdigest()

def get_db_connection():
    """Get database connection directly"""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        raise ValueError("DATABASE_URL environment variable is required")
    return psycopg2.connect(database_url)

def decrypt_email(encrypted_email: str) -> str:
    """Decrypt email using encryption service"""
    try:
        from app.encryption import decrypt
        return decrypt(encrypted_email)
    except Exception as e:
        print(f"[WARNING] Could not decrypt email: {e}")
        return None


def run_fix():
    """Execute email search fix"""
    print("=" * 60)
    print("PHASE 0: EMAIL SEARCH FIX")
    print("=" * 60)
    print()
    
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        # Step 1: Add email_hash column if it doesn't exist
        print("Step 1: Adding email_hash column to clients table...")
        try:
            # Check if column exists
            cursor.execute("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'clients' AND column_name = 'email_hash'
            """)
            column_exists = cursor.fetchone() is not None
            
            if not column_exists:
                cursor.execute("""
                    ALTER TABLE clients 
                    ADD COLUMN email_hash TEXT
                """)
                conn.commit()
                print("[OK] email_hash column added")
            else:
                print("[OK] email_hash column already exists")
        except Exception as e:
            print(f"[WARNING] {e}")
            conn.rollback()
        
        # Step 2: Create index if it doesn't exist
        print("\nStep 2: Creating email_hash index...")
        try:
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_clients_tenant_id_email_hash 
                ON clients (tenant_id, email_hash)
            """)
            conn.commit()
            print("[OK] email_hash index created")
        except Exception as e:
            print(f"[WARNING] {e}")
            conn.rollback()
        
        # Step 3: Backfill existing clients
        print("\nStep 3: Backfilling email hashes for existing clients...")
        try:
            # Get all clients without email_hash
            cursor.execute("""
                SELECT id, tenant_id, email 
                FROM clients 
                WHERE email_hash IS NULL AND email IS NOT NULL
            """)
            clients_to_backfill = cursor.fetchall()
            
            if not clients_to_backfill:
                print("[OK] No clients need backfilling")
            else:
                print(f"Found {len(clients_to_backfill)} clients to backfill...")
                backfilled = 0
                
                for row in clients_to_backfill:
                    client_id, tenant_id, encrypted_email = row[0], row[1], row[2]
                    try:
                        # Decrypt email
                        email = decrypt_email(encrypted_email)
                        if not email:
                            continue
                        # Hash email
                        email_hash = hash_email(email)
                        # Update client
                        cursor.execute("""
                            UPDATE clients 
                            SET email_hash = %s 
                            WHERE id = %s AND tenant_id = %s
                        """, (email_hash, client_id, tenant_id))
                        backfilled += 1
                    except Exception as e:
                        print(f"[WARNING] Failed to backfill client {client_id}: {e}")
                        continue
                
                conn.commit()
                print(f"[OK] Backfilled {backfilled} clients")
        except Exception as e:
            print(f"[WARNING] {e}")
            conn.rollback()
        
        # Step 4: Verify all clients have email_hash
        print("\nStep 4: Verifying all clients have email_hash...")
        cursor.execute("""
            SELECT COUNT(*) 
            FROM clients 
            WHERE email_hash IS NULL AND email IS NOT NULL
        """)
        missing_count = cursor.fetchone()[0]
        
        if missing_count == 0:
            print("[OK] All clients have email_hash")
        else:
            print(f"[WARNING] {missing_count} clients still missing email_hash")
        
        # Step 5: Verify column and index exist
        print("\nStep 5: Verifying column and index...")
        # Check column
        cursor.execute("""
            SELECT column_name 
            FROM information_schema.columns 
            WHERE table_name = 'clients' AND column_name = 'email_hash'
        """)
        if cursor.fetchone():
            print("[OK] email_hash column exists")
        else:
            print("[ERROR] email_hash column missing!")
            cursor.close()
            conn.close()
            return False
        
        # Check index
        cursor.execute("""
            SELECT indexname 
            FROM pg_indexes 
            WHERE tablename = 'clients' AND indexname = 'idx_clients_tenant_id_email_hash'
        """)
        if cursor.fetchone():
            print("[OK] email_hash index exists")
        else:
            print("[ERROR] email_hash index missing!")
            cursor.close()
            conn.close()
            return False
        
        cursor.close()
        conn.close()
        
        print("\n" + "=" * 60)
        print("[SUCCESS] EMAIL SEARCH FIX COMPLETE")
        print("=" * 60)
        return True
        
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = run_fix()
    sys.exit(0 if success else 1)

