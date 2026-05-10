"""
One-off column patches for PostgreSQL (legacy DBs).
Prefer: python database/init_db.py on a fresh database.
"""

from utils.db import get_connection


conn = get_connection()
cursor = conn.cursor()


def add_col(table, col, defn):
    try:
        cursor.execute(f'ALTER TABLE "{table}" ADD COLUMN {col} {defn}')
        print(f"Added {col} to {table}")
    except Exception as e:
        print(f"Skipped {col} in {table}: {e}")


add_col("blood_requests", "status", "VARCHAR(20) DEFAULT 'Open'")
add_col("blood_requests", "city", "VARCHAR(100)")
add_col("blood_requests", "urgency", "VARCHAR(20) DEFAULT 'Normal'")
add_col(
    "blood_requests",
    "created_at",
    "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
)

add_col("organ_requests", "status", "VARCHAR(20) DEFAULT 'Open'")
add_col("organ_requests", "city", "VARCHAR(100)")
add_col("organ_requests", "urgency", "VARCHAR(20) DEFAULT 'Normal'")
add_col("organ_requests", "notes", "TEXT")
add_col(
    "organ_requests",
    "created_at",
    "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
)

add_col("users", "city", "VARCHAR(100)")
add_col("users", "availability_status", "VARCHAR(20) DEFAULT 'Available'")
add_col("users", "is_verified", "BOOLEAN DEFAULT FALSE")
add_col("users", "organ_donor", "BOOLEAN DEFAULT FALSE")
add_col("users", "created_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP")

add_col("donations", "donation_type", "VARCHAR(20) DEFAULT 'Blood'")
add_col("donations", "donation_date", "DATE")

add_col("hospitals", "city", "VARCHAR(100)")
add_col("hospitals", "is_verified", "BOOLEAN DEFAULT FALSE")
add_col("hospitals", "created_at", "TIMESTAMP DEFAULT CURRENT_TIMESTAMP")

conn.commit()
print("Done")

cursor.close()
conn.close()
