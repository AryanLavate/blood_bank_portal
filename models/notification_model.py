"""
notification_model.py
---------------------
Database functions for the notifications table.
Notifications are sent to donors when matching blood requests are posted.
"""

from utils.db import get_connection


def create_notification(user_id, message):
    """Inserts a new notification for a donor."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO notifications (user_id, message) VALUES (%s, %s)",
        (user_id, message),
    )
    conn.commit()
    cursor.close()
    conn.close()


def get_notifications_for_user(user_id):
    """Returns all notifications for a donor, newest first."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT id, user_id, message, is_read, created_at FROM notifications
           WHERE user_id = %s ORDER BY created_at DESC""",
        (user_id,),
    )
    notifications = cursor.fetchall()
    cursor.close()
    conn.close()
    return notifications


def mark_all_read(user_id):
    """Marks all notifications as read for a user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE notifications SET is_read = TRUE WHERE user_id = %s",
        (user_id,),
    )
    conn.commit()
    cursor.close()
    conn.close()


def count_unread(user_id):
    """Returns count of unread notifications for a donor."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        """SELECT COUNT(*) FROM notifications
           WHERE user_id = %s AND is_read IS NOT TRUE""",
        (user_id,),
    )
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result[0] if result else 0


def notify_matching_donors(blood_group, city, message):
    """
    Sends a notification to all available donors in a city, optionally matching blood group.
    Called when a hospital posts a blood or organ request.
    - Blood request: notifies donors with matching blood_group and city.
    - Organ request: if blood_group is given, same as above; if empty, notifies all available donors in city.
    """
    if not city or not str(city).strip():
        return
    city_clean = str(city).strip()
    blood_clean = (blood_group or "").strip().upper() if blood_group else ""

    conn = get_connection()
    cursor = conn.cursor()
    try:
        if blood_clean:
            cursor.execute(
                """SELECT id FROM users
                   WHERE availability_status = 'Available'
                     AND blood_group = %s
                     AND city IS NOT NULL AND LOWER(TRIM(city)) = LOWER(%s)""",
                (blood_clean, city_clean),
            )
        else:
            cursor.execute(
                """SELECT id FROM users
                   WHERE availability_status = 'Available'
                     AND city IS NOT NULL AND LOWER(TRIM(city)) = LOWER(%s)""",
                (city_clean,),
            )
        donors = cursor.fetchall()
        for donor in donors:
            cursor.execute(
                "INSERT INTO notifications (user_id, message) VALUES (%s, %s)",
                (donor[0], message),
            )
        conn.commit()
    finally:
        cursor.close()
        conn.close()
