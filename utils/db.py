"""
PostgreSQL connections via psycopg2-binary.
Compatible with all existing Flask blueprints and model code.

Connection order:
  1) DATABASE_URL if set
  2) DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME (+ PG_SSLMODE)
"""

import psycopg2

from config import (
    DATABASE_URL,
    DB_HOST,
    DB_PORT,
    DB_USER,
    DB_PASSWORD,
    DB_NAME,
    PG_SSLMODE,
)


def get_connection():
    """
    New connection per call (simple and safe for Gunicorn workers).
    Caller must close the connection and cursor when done.
    """
    if DATABASE_URL:
        conn = psycopg2.connect(DATABASE_URL)
    else:
        conn = psycopg2.connect(
            host=DB_HOST,
            port=int(str(DB_PORT)),
            user=DB_USER,
            password=DB_PASSWORD,
            dbname=DB_NAME,
            sslmode=PG_SSLMODE,
        )
    conn.set_session(autocommit=False)
    return conn


def ping_db():
    conn = get_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.close()
    finally:
        conn.close()
