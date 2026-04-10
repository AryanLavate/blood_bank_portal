"""
blood_request_model.py
----------------------
Database functions for blood requests posted by hospitals.
"""

from utils.db import get_connection


def create_blood_request(hospital_id, blood_group, units_required, city, urgency):
    """Inserts a new blood request posted by a hospital."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO blood_requests
           (hospital_id, blood_group, units_required, city, urgency)
           VALUES (%s, %s, %s, %s, %s)""",
        (hospital_id, blood_group, units_required, city, urgency)
    )
    conn.commit()
    cursor.close()
    conn.close()


def get_all_blood_requests():
    """
    Returns all blood requests joined with hospital names.
    Used by admin and public search.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT br.id, h.hospital_name, br.blood_group, br.units_required,
                  br.city, br.urgency, br.status, br.created_at
           FROM blood_requests br
           JOIN hospitals h ON br.hospital_id = h.id
           ORDER BY br.created_at DESC"""
    )
    requests = cursor.fetchall()
    cursor.close()
    conn.close()
    return requests


def get_blood_requests_by_hospital(hospital_id):
    """Returns all blood requests posted by a specific hospital."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT * FROM blood_requests
           WHERE hospital_id = %s
           ORDER BY created_at DESC""",
        (hospital_id,)
    )
    requests = cursor.fetchall()
    cursor.close()
    conn.close()
    return requests


def get_blood_requests_for_donor(city):
    """
    Returns open blood requests matching a donor's city.
    Used to show relevant emergency requests to a logged-in donor.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT br.id, h.hospital_name, br.blood_group, br.units_required,
                  br.city, br.urgency, br.created_at
           FROM blood_requests br
           JOIN hospitals h ON br.hospital_id = h.id
           WHERE LOWER(br.city) = LOWER(%s) AND br.status = 'Open'
           ORDER BY br.created_at DESC""",
        (city,)
    )
    requests = cursor.fetchall()
    cursor.close()
    conn.close()
    return requests


def close_blood_request(request_id):
    """Marks a blood request as Fulfilled."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE blood_requests SET status = 'Fulfilled' WHERE id = %s",
        (request_id,)
    )
    conn.commit()
    cursor.close()
    conn.close()


def delete_blood_request(request_id):
    """Deletes a blood request. Used by admin."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM blood_requests WHERE id = %s", (request_id,))
    conn.commit()
    cursor.close()
    conn.close()


def count_blood_requests():
    """Returns total number of blood requests."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM blood_requests")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else 0
