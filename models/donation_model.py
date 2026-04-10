"""
donation_model.py
-----------------
Database functions for the donations table.
"""

from utils.db import get_connection


def record_donation(user_id, hospital_id, donation_type, donation_date):
    """Records a completed donation event."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO donations
           (user_id, hospital_id, donation_type, donation_date)
           VALUES (%s, %s, %s, %s)""",
        (user_id, hospital_id, donation_type, donation_date)
    )
    conn.commit()
    cursor.close()
    conn.close()


def get_donations_by_user(user_id):
    """Returns all donation records for a specific donor."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT d.id, h.hospital_name, d.donation_type, d.donation_date
           FROM donations d
           JOIN hospitals h ON d.hospital_id = h.id
           WHERE d.user_id = %s
           ORDER BY d.donation_date DESC""",
        (user_id,)
    )
    donations = cursor.fetchall()
    cursor.close()
    conn.close()
    return donations


def get_all_donations():
    """Returns all donations. Used by admin statistics."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT d.id, u.name AS donor_name, h.hospital_name,
                  d.donation_type, d.donation_date
           FROM donations d
           JOIN users u ON d.user_id = u.id
           JOIN hospitals h ON d.hospital_id = h.id
           ORDER BY d.donation_date DESC"""
    )
    donations = cursor.fetchall()
    cursor.close()
    conn.close()
    return donations


def count_donations():
    """Returns total number of donation records."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM donations")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else 0
