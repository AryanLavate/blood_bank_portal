"""
user_model.py
-------------
Database functions for the users (donors) table.
"""

from utils.db import get_connection
from utils.helpers import hash_password

# Stable column order for tuple indexing in templates and routes
USER_SELECT_COLUMNS = """
id, name, age, blood_group, organ_donor, phone, email, password,
city, availability_status, is_verified, created_at
"""


def create_user(name, age, blood_group, organ_donor, phone, email, password, city):
    """
    Inserts a new user/donor record into the database.
    Password is hashed before storing.
    """
    conn = get_connection()
    cursor = conn.cursor()
    hashed = hash_password(password)
    cursor.execute(
        """INSERT INTO users
           (name, age, blood_group, organ_donor, phone, email, password, city)
           VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""",
        (name, age, blood_group, organ_donor, phone, email, hashed, city),
    )
    conn.commit()
    cursor.close()
    conn.close()


def get_user_by_email(email):
    """Returns the full user row by email address."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT {USER_SELECT_COLUMNS} FROM users WHERE email = %s",
        (email,),
    )
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user


def get_user_by_id(user_id):
    """Returns a single user row by primary key."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT {USER_SELECT_COLUMNS} FROM users WHERE id = %s",
        (user_id,),
    )
    user = cursor.fetchone()
    cursor.close()
    conn.close()
    return user


def update_user_availability(user_id, status):
    """Updates the availability_status field for a donor."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET availability_status = %s WHERE id = %s",
        (status, user_id),
    )
    conn.commit()
    cursor.close()
    conn.close()


def update_user_profile(user_id, name, age, phone, city, organ_donor):
    """Updates editable profile fields for a donor."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """UPDATE users
           SET name = %s, age = %s, phone = %s, city = %s, organ_donor = %s
           WHERE id = %s""",
        (name, age, phone, city, organ_donor, user_id),
    )
    conn.commit()
    cursor.close()
    conn.close()


def get_all_users():
    """Returns all users. Used by admin."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        f"SELECT {USER_SELECT_COLUMNS} FROM users ORDER BY created_at DESC"
    )
    users = cursor.fetchall()
    cursor.close()
    conn.close()
    return users


def search_donors(blood_group=None, city=None, availability=None):
    """
    Searches donors with optional filters.
    All parameters are optional; unset filters are ignored.
    """
    conn = get_connection()
    cursor = conn.cursor()
    query = f"SELECT {USER_SELECT_COLUMNS} FROM users WHERE 1=1"
    params = []
    if blood_group:
        query += " AND blood_group = %s"
        params.append(blood_group)
    if city:
        query += " AND city ILIKE %s"
        params.append("%" + city + "%")
    if availability:
        query += " AND availability_status = %s"
        params.append(availability)
    query += " ORDER BY name ASC"
    cursor.execute(query, params)
    donors = cursor.fetchall()
    cursor.close()
    conn.close()
    return donors


def delete_user(user_id):
    """Deletes a user record by ID. Used by admin."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM users WHERE id = %s", (user_id,))
    conn.commit()
    cursor.close()
    conn.close()


def verify_user(user_id):
    """Marks a user as verified. Used by admin."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE users SET is_verified = TRUE WHERE id = %s",
        (user_id,),
    )
    conn.commit()
    cursor.close()
    conn.close()


def count_users():
    """Returns total number of registered users."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else 0
