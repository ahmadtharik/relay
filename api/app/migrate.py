import os
import psycopg  # Swap for 'sqlite3' or 'asyncpg' if needed
from pathlib import Path
import sys
# 1. Database Connection Configuration
DATABASE_URL = os.environ.get("DATABASE_URL")

MIGRATIONS = [
    (
        "001_create_tasks_table",
        """
        CREATE TABLE tasks (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            name TEXT,
            steps INT,
            progress INT DEFAULT 0,
            status TEXT DEFAULT 'queued',
            created_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMPTZ DEFAULT CURRENT_TIMESTAMP
        );"""),]

def run_migrations():
    print("🚀 Starting manual database migrations...")
    
    with psycopg.connect(DATABASE_URL) as conn:
        with conn.cursor() as cur:
            # Step A: Create the tracking table if it doesn't exist
            cur.execute("""
                CREATE TABLE IF NOT EXISTS schema_migrations (
                    version VARCHAR(255) PRIMARY KEY,
                    applied_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            conn.commit()

            # Step B: Get already applied migrations
            cur.execute("SELECT version FROM schema_migrations;")
            applied = {row[0] for row in cur.fetchall()}  # Extracted from tuple

            # Step C: Run pending migrations
            for version, sql in MIGRATIONS:
                if version in applied:
                    print(f"  [Skipped] {version} (Already applied)")
                    continue
                
                print(f"  [Applying] {version}...")
                try:
                    # Execute the plain SQL block
                    cur.execute(sql)
                    # Track it as completed
                    cur.execute(
                        "INSERT INTO schema_migrations (version) VALUES (%s);", 
                        (version,)
                    )
                    conn.commit()
                    print(f"  [Success] {version}")
                except Exception as e:
                    conn.rollback()
                    print(f"❌ Error applying migration '{version}': {e}")
                    print("🛑 Execution halted. Rolling back transaction.")
                    sys.exit(1)

    print("✅ All migrations are up to date.")

if __name__ == "__main__":
    run_migrations()