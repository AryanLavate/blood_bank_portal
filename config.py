"""
Application configuration.
Loads from environment variables and optional .env (python-dotenv).
Render: set DATABASE_URL to the PostgreSQL connection string from the dashboard.
Local: set DATABASE_URL or DB_HOST / DB_USER / DB_PASSWORD / DB_NAME / DB_PORT.
"""

import os

from dotenv import load_dotenv

load_dotenv()


def _normalize_database_url(url: str) -> str:
    """Render sometimes uses postgres://; psycopg2 expects postgresql://."""
    if not url:
        return ""
    url = url.strip()
    if url.startswith("postgres://"):
        url = "postgresql://" + url[len("postgres://") :]
    return url


DATABASE_URL = _normalize_database_url(os.getenv("DATABASE_URL", ""))

# Individual connection parameters (used when DATABASE_URL is not set)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "blood_bank_portal")

SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key-in-production")

# Flask / gunicorn
DEBUG = os.getenv("FLASK_DEBUG", "false").lower() in ("1", "true", "yes")

# SSL for managed PostgreSQL (Render). Set PGSSLMODE=require on Render if not in URL.
# Local dev: omit PGSSLMODE or use PGSSLMODE=disable
if DATABASE_URL and "sslmode=" not in DATABASE_URL:
    sslmode = os.getenv("PGSSLMODE")
    if sslmode:
        sep = "&" if "?" in DATABASE_URL else "?"
        DATABASE_URL = f"{DATABASE_URL}{sep}sslmode={sslmode}"
