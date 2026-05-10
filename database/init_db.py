"""
init_db.py
----------
Apply database/schema.sql to the configured PostgreSQL database.

Usage (from project root):
    python database/init_db.py

Requires: DATABASE_URL or DB_HOST / DB_USER / DB_PASSWORD / DB_NAME (see config.py).
Uses sqlparse to split statements (handles dollar-quoted functions in schema).
"""

import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import sqlparse

from utils.db import get_connection


def run_schema():
    schema_path = os.path.join(os.path.dirname(__file__), "schema.sql")
    with open(schema_path, "r", encoding="utf-8") as f:
        sql_content = f.read()

    conn = get_connection()
    conn.autocommit = True
    cursor = conn.cursor()

    try:
        for statement in sqlparse.split(sql_content):
            stmt = statement.strip()
            if not stmt:
                continue
            cursor.execute(stmt)
    finally:
        cursor.close()
        conn.close()

    print("Schema applied successfully.")


if __name__ == "__main__":
    run_schema()
