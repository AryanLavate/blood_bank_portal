"""
admin_model.py
--------------
Database functions for the admins table.
"""

from utils.db import get_connection
from utils.helpers import hash_password


def get_admin_by_username(username):
    """Returns an admin row by username."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM admins WHERE username = %s", (username,))
    admin = cursor.fetchone()
    cursor.close()
    conn.close()
    return admin


def create_admin(username, password):
    """Creates a new admin. Password is hashed before storing."""
    conn = get_connection()
    cursor = conn.cursor()
    hashed = hash_password(password)
    cursor.execute(
        "INSERT INTO admins (username, password) VALUES (%s, %s)",
        (username, hashed)
    )
    conn.commit()
    cursor.close()
    conn.close()
