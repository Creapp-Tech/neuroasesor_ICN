import os
import psycopg2
from pathlib import Path

def run_migrations():
    conn = psycopg2.connect(os.environ["DATABASE_URL"])
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS _migrations (
            filename TEXT PRIMARY KEY,
            applied_at TIMESTAMPTZ DEFAULT NOW()
        )
    """)
    conn.commit()

    sql_files = sorted(Path("migrations").glob("*.sql"))

    for sql_file in sql_files:
        cursor.execute("SELECT 1 FROM _migrations WHERE filename = %s", (sql_file.name,))
        if cursor.fetchone():
            print(f" Skipping {sql_file.name} (already applied)")
            continue

        print(f"Running: {sql_file.name}")
        cursor.execute(sql_file.read_text())
        cursor.execute("INSERT INTO _migrations (filename) VALUES (%s)", (sql_file.name,))
        conn.commit()
        print(f" {sql_file.name} done")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    run_migrations()
