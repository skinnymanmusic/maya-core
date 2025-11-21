"""
Apply conversations table migration
Standalone script that doesn't require app imports
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import psycopg2

# Load .env
load_dotenv()

def apply_migration():
    """Apply conversations table migration"""
    database_url = os.getenv("DATABASE_URL")
    if not database_url:
        print("[ERROR] DATABASE_URL environment variable is required")
        return False
    
    try:
        # Read migration file
        migration_file = Path(__file__).parent / "migrations" / "014_add_conversations_table.sql"
        sql = migration_file.read_text()
        
        # Connect and execute
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        cursor.execute(sql)
        conn.commit()
        cursor.close()
        conn.close()
        
        print("[OK] Conversations and SMS messages tables created")
        return True
    except Exception as e:
        print(f"[ERROR] {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = apply_migration()
    sys.exit(0 if success else 1)

