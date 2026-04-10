"""
init_db.py
----------
Run this script once to create your database and all tables automatically.
Usage: python database/init_db.py
"""

import sys
import os

# Add project root to path so we can import config
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import MySQLdb
from config import DB_HOST, DB_USER, DB_PASSWORD, DB_NAME

def run_schema():
    # First connect without selecting a database
    conn = MySQLdb.connect(host=DB_HOST, user=DB_USER, passwd=DB_PASSWORD)
    cursor = conn.cursor()

    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')

    with open(schema_path, 'r') as f:
        sql_content = f.read()

    # Split on semicolons and run each statement
    statements = [s.strip() for s in sql_content.split(';') if s.strip() and not s.strip().startswith('--')]

    for statement in statements:
        try:
            cursor.execute(statement)
            conn.commit()
        except MySQLdb.Error as e:
            print("Error on statement: " + statement[:60])
            print("MySQL Error: " + str(e))

    cursor.close()
    conn.close()
    print("Database and tables created successfully.")

if __name__ == '__main__':
    run_schema()
