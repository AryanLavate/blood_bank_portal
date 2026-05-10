"""
PostgreSQL connection helper for the Blood Bank Portal.
Uses psycopg2. Prefer DATABASE_URL on Render.
"""

import psycopg2

from config import DATABASE_URL, DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME


def get_connection():
    """
    Return a new PostgreSQL connection.
    Caller is responsible for closing the connection (and cursor).
    """
    if DATABASE_URL:
        conn = psycopg2.connect(DATABASE_URL)
    else:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            dbname=DB_NAME,
        )
    conn.set_session(autocommit=False)
    return conn


def ping_db():
    """Lightweight connectivity check (optional use in health checks)."""
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.close()
    finally:
        conn.close()
