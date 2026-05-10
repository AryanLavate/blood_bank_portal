"""
db_setup.py
-----------
Interactive setup for PostgreSQL (local or Render).

  1. Writes .env
  2. Applies database/schema.sql (new Python process loads fresh config)
  3. Runs fix_db patches
  4. Verifies connection (new Python process)

Usage: python db_setup.py
"""

import os
import subprocess
import sys

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
os.chdir(PROJECT_ROOT)
sys.path.insert(0, PROJECT_ROOT)


def write_env_database_url(url: str, secret_key: str):
    env_path = os.path.join(PROJECT_ROOT, ".env")
    lines = [
        f"DATABASE_URL={url}",
        f"SECRET_KEY={secret_key}",
        "FLASK_DEBUG=true",
        "# Render: if URL has no sslmode, set PGSSLMODE=require",
        "",
    ]
    with open(env_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("\n[OK] .env updated with DATABASE_URL.")


def write_env_individual(host, port, user, password, dbname, secret_key):
    env_path = os.path.join(PROJECT_ROOT, ".env")
    lines = [
        f"DB_HOST={host}",
        f"DB_PORT={port}",
        f"DB_USER={user}",
        f"DB_PASSWORD={password}",
        f"DB_NAME={dbname}",
        f"SECRET_KEY={secret_key}",
        "FLASK_DEBUG=true",
        "# Local without SSL: PGSSLMODE=disable",
        "",
    ]
    with open(env_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))
    print("\n[OK] .env updated with DB_* variables.")


def prompt_credentials():
    print("\n=== Blood Bank Portal - PostgreSQL Setup ===\n")
    print(
        "Paste your full DATABASE_URL (recommended for Render), "
        "or press Enter to use separate fields.\n"
    )
    url = input("DATABASE_URL (postgresql://...) []: ").strip()
    secret = input("SECRET_KEY [dev-change-me]: ").strip() or "dev-change-me"
    if url:
        write_env_database_url(url, secret)
        return
    print("\nEnter PostgreSQL connection details:\n")
    host = input("DB host [localhost]: ").strip() or "localhost"
    port = input("DB port [5432]: ").strip() or "5432"
    user = input("DB user [postgres]: ").strip() or "postgres"
    password = input("DB password: ").strip()
    if not password:
        print("Password cannot be empty.")
        sys.exit(1)
    dbname = input("DB name [blood_bank_portal]: ").strip() or "blood_bank_portal"
    write_env_individual(host, port, user, password, dbname, secret)


def _run_script(rel_path: str) -> None:
    path = os.path.join(PROJECT_ROOT, rel_path)
    rc = subprocess.call([sys.executable, path], cwd=PROJECT_ROOT)
    if rc != 0:
        print(f"[FAIL] {rel_path} exited with code {rc}")
        sys.exit(rc)


def verify_connection():
    rc = subprocess.call(
        [
            sys.executable,
            "-c",
            "from utils.db import get_connection; c = get_connection(); c.close(); "
            "print('[OK] Connection successful.')",
        ],
        cwd=PROJECT_ROOT,
    )
    if rc != 0:
        sys.exit(rc)


def main():
    prompt_credentials()
    print("\n[1/3] Applying database/schema.sql ...")
    _run_script(os.path.join("database", "init_db.py"))
    print("[OK] Schema applied.")
    print("\n[2/3] Applying schema patches (fix_db) ...")
    _run_script("fix_db.py")
    print("[OK] Patches done.")
    print("\n[3/3] Verifying connection...")
    verify_connection()
    print("\n" + "=" * 50)
    print("Setup complete. Run the application:")
    print("  python run.py")
    print("Production (Render / gunicorn):")
    print("  gunicorn run:app --bind 0.0.0.0:$PORT")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    main()
