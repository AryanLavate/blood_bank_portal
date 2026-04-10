"""
hospital_model.py
-----------------
Database functions for the hospitals table.
"""

from utils.db import get_connection
from utils.helpers import hash_password


def create_hospital(hospital_name, email, password, phone, city):
    """Inserts a new hospital record. Password is hashed."""
    conn = get_connection()
    cursor = conn.cursor()
    hashed = hash_password(password)
    cursor.execute(
        """INSERT INTO hospitals
           (hospital_name, email, password, phone, city)
           VALUES (%s, %s, %s, %s, %s)""",
        (hospital_name, email, hashed, phone, city)
    )
    conn.commit()
    cursor.close()
    conn.close()


def get_hospital_by_email(email):
    """Returns a hospital row by email."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM hospitals WHERE email = %s", (email,))
    hospital = cursor.fetchone()
    cursor.close()
    conn.close()
    return hospital


def get_hospital_by_id(hospital_id):
    """Returns a hospital row by primary key."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM hospitals WHERE id = %s", (hospital_id,))
    hospital = cursor.fetchone()
    cursor.close()
    conn.close()
    return hospital


def get_all_hospitals():
    """Returns all hospitals. Used by admin."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM hospitals ORDER BY created_at DESC")
    hospitals = cursor.fetchall()
    cursor.close()
    conn.close()
    return hospitals


def delete_hospital(hospital_id):
    """Deletes a hospital record. Used by admin."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM hospitals WHERE id = %s", (hospital_id,))
    conn.commit()
    cursor.close()
    conn.close()


def verify_hospital(hospital_id):
    """Marks a hospital as verified by admin."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE hospitals SET is_verified = 1 WHERE id = %s", (hospital_id,))
    conn.commit()
    cursor.close()
    conn.close()


def count_hospitals():
    """Returns total number of registered hospitals."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM hospitals")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else 0
