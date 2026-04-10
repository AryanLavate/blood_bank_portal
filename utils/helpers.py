"""
helpers.py
----------
Utility functions used across the application.
Includes password hashing, session decorators, and input validation.
"""

import hashlib
from functools import wraps
from flask import session, redirect, url_for, flash


def hash_password(password):
    """
    Hashes a plain-text password using SHA-256.
    Returns the hashed string.
    """
    return hashlib.sha256(password.encode()).hexdigest()


def check_password(plain_password, hashed_password):
    """
    Compares a plain-text password with a stored hash.
    Returns True if they match.
    """
    return hash_password(plain_password) == hashed_password


def login_required(f):
    """
    Decorator: protects donor routes.
    Redirects to /login if user is not logged in.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to continue.', 'warning')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def hospital_login_required(f):
    """
    Decorator: protects hospital routes.
    Redirects to /hospital/login if hospital is not logged in.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'hospital_id' not in session:
            flash('Please log in as a hospital to continue.', 'warning')
            return redirect(url_for('auth.hospital_login'))
        return f(*args, **kwargs)
    return decorated_function


def admin_login_required(f):
    """
    Decorator: protects admin routes.
    Redirects to /admin/login if admin is not logged in.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_id' not in session:
            flash('Admin access required.', 'danger')
            return redirect(url_for('auth.admin_login'))
        return f(*args, **kwargs)
    return decorated_function


# List of valid blood groups for input validation
VALID_BLOOD_GROUPS = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']


def is_valid_blood_group(bg):
    """Returns True if the blood group string is valid."""
    return bg.strip().upper() in VALID_BLOOD_GROUPS
