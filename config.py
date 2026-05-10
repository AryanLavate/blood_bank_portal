"""
Environment-based configuration for Render and local dev.
All values come from os.getenv(); use the Render dashboard for secrets (never commit them).

Required on Render (Web Service → Environment):
  DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD, SECRET_KEY

Optional:
  DATABASE_URL — if set, used instead of DB_* for connections
  PGSSLMODE — passed to psycopg2 (default: require when DB_HOST contains render.com)
  FLASK_DEBUG — "true" only for local debugging; omit or "false" on Render
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


DATABASE_URL = _normalize_database_url(os.getenv("DATABASE_URL", ""))
if DATABASE_URL and "sslmode=" not in DATABASE_URL:
    _ssl = os.getenv("PGSSLMODE")
    if _ssl:
        _sep = "&" if "?" in DATABASE_URL else "?"
        DATABASE_URL = f"{DATABASE_URL}{_sep}sslmode={_ssl}"

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "blood_bank_portal")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")

SECRET_KEY = os.getenv("SECRET_KEY", "change-this-secret-key-in-production")

DEBUG = os.getenv("FLASK_DEBUG", "false").lower() in ("1", "true", "yes")

_default_ssl = (
    "require" if "render.com" in (DB_HOST or "").lower() else "prefer"
)
PG_SSLMODE = os.getenv("PGSSLMODE", _default_ssl)
