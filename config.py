"""
Application configuration for production and development.

Render Web Service — set in the dashboard (Environment):
  DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD, SECRET_KEY

Optional:
  DATABASE_URL — if set, overrides DB_* for psycopg2 (full postgresql:// URL)
  PGSSLMODE — sslmode for psycopg2 (default: require on *.render.com hosts, else prefer)
  FLASK_DEBUG — set false in production
"""

import os

from dotenv import load_dotenv

load_dotenv()


def _normalize_database_url(url: str) -> str:
    if not url:
        return ""
    url = url.strip()
    if url.startswith("postgres://"):
        url = "postgresql://" + url[len("postgres://") :]
    return url


# Optional single URL (Render “Internal Database URL” or external URL)
DATABASE_URL = _normalize_database_url(os.getenv("DATABASE_URL", ""))
if DATABASE_URL and "sslmode=" not in DATABASE_URL:
    _sm = os.getenv("PGSSLMODE")
    if _sm:
        _sep = "&" if "?" in DATABASE_URL else "?"
        DATABASE_URL = f"{DATABASE_URL}{_sep}sslmode={_sm}"

# Render PostgreSQL — individual variables (recommended for your setup)
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
DB_NAME = os.getenv("DB_NAME", "blood_bank_portal")

SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key-in-production")

DEBUG = os.getenv("FLASK_DEBUG", "false").lower() in ("1", "true", "yes")

# psycopg2 sslmode: Render managed Postgres requires TLS for external hostnames
_default_ssl = (
    "require"
    if "render.com" in (DB_HOST or "").lower()
    else "prefer"
)
PG_SSLMODE = os.getenv("PGSSLMODE", _default_ssl)
