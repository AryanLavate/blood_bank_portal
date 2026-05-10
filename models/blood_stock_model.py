"""
blood_stock_model.py
--------------------
Database functions for blood stock inventory managed by hospitals.
"""

from utils.db import get_connection


def upsert_blood_stock(hospital_id, blood_group, units_available):
    """
    Inserts or updates the blood stock for a given hospital and blood group.
    PostgreSQL: ON CONFLICT on (hospital_id, blood_group).
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO blood_stock (hospital_id, blood_group, units_available)
           VALUES (%s, %s, %s)
           ON CONFLICT (hospital_id, blood_group)
           DO UPDATE SET units_available = EXCLUDED.units_available""",
        (hospital_id, blood_group, units_available),
    )
    conn.commit()
    cursor.close()
    conn.close()


def get_stock_by_hospital(hospital_id):
    """Returns all blood stock rows for a given hospital."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT blood_group, units_available, updated_at FROM blood_stock
           WHERE hospital_id = %s ORDER BY blood_group""",
        (hospital_id,),
    )
    stock = cursor.fetchall()
    cursor.close()
    conn.close()
    return stock


def get_all_stock():
    """
    Returns all blood stock across all hospitals.
    Used for public view.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT h.hospital_name, h.city, bs.blood_group, bs.units_available, bs.updated_at
           FROM blood_stock bs
           JOIN hospitals h ON bs.hospital_id = h.id
           ORDER BY h.hospital_name, bs.blood_group"""
    )
    stock = cursor.fetchall()
    cursor.close()
    conn.close()
    return stock
