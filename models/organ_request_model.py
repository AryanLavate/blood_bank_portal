"""
organ_request_model.py
----------------------
Database functions for organ transplant requests posted by hospitals.
"""

from utils.db import get_connection


def create_organ_request(hospital_id, organ_type, blood_group, city, urgency, notes):
    """Inserts a new organ transplant request."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO organ_requests
           (hospital_id, organ_type, blood_group, city, urgency, notes)
           VALUES (%s, %s, %s, %s, %s, %s)""",
        (hospital_id, organ_type, blood_group, city, urgency, notes)
    )
    conn.commit()
    cursor.close()
    conn.close()


def get_all_organ_requests():
    """Returns all organ requests joined with hospital info."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT ore.id, h.hospital_name, ore.organ_type, ore.blood_group,
                  ore.city, ore.urgency, ore.status, ore.notes, ore.created_at
           FROM organ_requests ore
           JOIN hospitals h ON ore.hospital_id = h.id
           ORDER BY ore.created_at DESC"""
    )
    requests = cursor.fetchall()
    cursor.close()
    conn.close()
    return requests


def get_organ_requests_by_hospital(hospital_id):
    """Returns organ requests for a specific hospital."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT * FROM organ_requests WHERE hospital_id = %s ORDER BY created_at DESC",
        (hospital_id,)
    )
    requests = cursor.fetchall()
    cursor.close()
    conn.close()
    return requests


def delete_organ_request(request_id):
    """Deletes an organ request. Used by admin."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM organ_requests WHERE id = %s", (request_id,))
    conn.commit()
    cursor.close()
    conn.close()

def get_organ_requests_for_donor(city):
    """
    Returns open organ transplant requests matching a donor's city.
    Used to show relevant emergency organ requests to a logged-in donor.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT ore.id, h.hospital_name, ore.organ_type, ore.blood_group,
                  ore.city, ore.urgency, ore.created_at
           FROM organ_requests ore
           JOIN hospitals h ON ore.hospital_id = h.id
           WHERE LOWER(ore.city) = LOWER(%s) AND ore.status = 'Open'
           ORDER BY ore.created_at DESC""",
        (city,)
    )
    requests = cursor.fetchall()
    cursor.close()
    conn.close()
    return requests
