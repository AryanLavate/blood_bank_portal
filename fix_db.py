"""
fix_db.py
---------
Run this script ONCE to patch an existing PostgreSQL database if columns are missing
(e.g. after an old MySQL migration).

Usage (from project root):
    python fix_db.py
"""

import sys
import os

sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from utils.db import get_connection


def column_exists(cursor, table, column):
    cursor.execute(
        """SELECT 1 FROM information_schema.columns
           WHERE table_schema = 'public' AND table_name = %s AND column_name = %s""",
        (table, column),
    )
    return cursor.fetchone() is not None


def add_column_if_missing(cursor, table, column, definition):
    if not column_exists(cursor, table, column):
        print("  Adding column '{}' to table '{}' ...".format(column, table))
        cursor.execute(
            'ALTER TABLE "{}" ADD COLUMN {} {}'.format(table, column, definition)
        )
        print("  Done.")
    else:
        print("  Column '{}' in '{}' already exists, skipping.".format(column, table))


def main():
    from config import DB_NAME

    print("Connecting to database '{}'...".format(DB_NAME))
    conn = get_connection()
    cursor = conn.cursor()
    print("Connected.\n")

    print("=== Patching table: blood_requests ===")
    add_column_if_missing(
        cursor, "blood_requests", "status", "VARCHAR(20) DEFAULT 'Open'"
    )
    add_column_if_missing(cursor, "blood_requests", "city", "VARCHAR(100)")
    add_column_if_missing(
        cursor, "blood_requests", "urgency", "VARCHAR(20) DEFAULT 'Normal'"
    )
    add_column_if_missing(
        cursor,
        "blood_requests",
        "created_at",
        "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
    )

    print("\n=== Patching table: organ_requests ===")
    add_column_if_missing(
        cursor, "organ_requests", "status", "VARCHAR(20) DEFAULT 'Open'"
    )
    add_column_if_missing(cursor, "organ_requests", "city", "VARCHAR(100)")
    add_column_if_missing(
        cursor, "organ_requests", "urgency", "VARCHAR(20) DEFAULT 'Normal'"
    )
    add_column_if_missing(cursor, "organ_requests", "notes", "TEXT")
    add_column_if_missing(
        cursor,
        "organ_requests",
        "created_at",
        "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
    )

    print("\n=== Patching table: users ===")
    add_column_if_missing(cursor, "users", "city", "VARCHAR(100)")
    add_column_if_missing(
        cursor,
        "users",
        "availability_status",
        "VARCHAR(20) DEFAULT 'Available'",
    )
    add_column_if_missing(cursor, "users", "is_verified", "BOOLEAN DEFAULT FALSE")
    add_column_if_missing(cursor, "users", "organ_donor", "BOOLEAN DEFAULT FALSE")
    add_column_if_missing(
        cursor,
        "users",
        "created_at",
        "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
    )

    print("\n=== Patching table: donations ===")
    add_column_if_missing(
        cursor, "donations", "donation_type", "VARCHAR(20) DEFAULT 'Blood'"
    )
    add_column_if_missing(cursor, "donations", "donation_date", "DATE")

    print("\n=== Patching table: hospitals ===")
    add_column_if_missing(cursor, "hospitals", "city", "VARCHAR(100)")
    add_column_if_missing(cursor, "hospitals", "is_verified", "BOOLEAN DEFAULT FALSE")
    add_column_if_missing(
        cursor,
        "hospitals",
        "created_at",
        "TIMESTAMP DEFAULT CURRENT_TIMESTAMP",
    )

    conn.commit()
    cursor.close()
    conn.close()

    print("\nAll patches applied. Your database is now up to date.")


if __name__ == "__main__":
    main()
