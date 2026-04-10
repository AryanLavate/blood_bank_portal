"""
db_setup.py
-----------
One-time setup for running this project on a new PC.
Enter your MySQL username and password; this script will:
  1. Save credentials to .env
  2. Create the database and all tables
  3. Apply any schema patches
  4. Verify the connection

Usage: python db_setup.py
"""

import os
import sys

# Ensure we're in project root
PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
os.chdir(PROJECT_ROOT)
sys.path.insert(0, PROJECT_ROOT)


def get_credentials():
    """Prompt for MySQL username and password."""
    print("\n=== Blood Bank Portal - Database Setup ===\n")
    print("Enter your MySQL credentials (MySQL server must be running).\n")
    user = input("MySQL username [root]: ").strip() or "root"
    password = input("MySQL password: ").strip()
    if not password:
        print("Password cannot be empty.")
        sys.exit(1)
    return user, password


def write_env(user, password):
    """Write .env with the given MySQL credentials."""
    env_content = "\n".join([
        "DB_HOST=localhost",
        f"DB_USER={user}",
        f"DB_PASSWORD={password}",
        "DB_NAME=blood_bank_portal",
        "SECRET_KEY=replace-with-a-strong-random-secret",
        "",
    ])
    env_path = os.path.join(PROJECT_ROOT, ".env")
    with open(env_path, "w") as f:
        f.write(env_content)
    print("\n[OK] .env updated with your credentials.")


def create_database_and_tables():
    """Create database and all tables using schema.sql."""
    import MySQLdb
    from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

    schema_path = os.path.join(PROJECT_ROOT, "database", "schema.sql")
    with open(schema_path, "r") as f:
        sql_content = f.read()

    # Split on semicolons, ignore comments and empty statements
    statements = [
        s.strip() for s in sql_content.split(";")
        if s.strip() and not s.strip().startswith("--")
    ]

    print("\n[1/3] Connecting to MySQL and creating database & tables...")
    conn = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD)
    cursor = conn.cursor()

    for statement in statements:
        try:
            cursor.execute(statement)
            conn.commit()
        except MySQLdb.Error as e:
            print("  Error: " + str(e))
            cursor.close()
            conn.close()
            raise

    cursor.close()
    conn.close()
    print("[OK] Database and tables created successfully.")


def apply_patches():
    """Apply any missing columns (fix_db)."""
    from fix_db import main as fix_db_main
    print("\n[2/3] Applying schema patches (if any)...")
    fix_db_main()


def verify_connection():
    """Verify that the app can connect to the database."""
    from utils.db import get_connection
    print("\n[3/3] Verifying connection...")
    try:
        conn = get_connection()
        conn.close()
        print("[OK] Connection successful.")
    except Exception as e:
        print("[FAIL] Could not connect: " + str(e))
        sys.exit(1)


def main():
    user, password = get_credentials()
    write_env(user, password)
    create_database_and_tables()
    apply_patches()
    verify_connection()
    print("\n" + "=" * 50)
    print("Setup complete. You can now run the application:")
    print("  python run.py")
    print("=" * 50 + "\n")


if __name__ == "__main__":
    main()
