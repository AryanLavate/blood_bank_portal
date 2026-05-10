"""
PostgreSQL via psycopg2-binary. No MySQL.
Uses DATABASE_URL if set; otherwise DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME.
"""

import os

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
            connect_timeout=int(os.getenv("PG_CONNECT_TIMEOUT", "10")),
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
