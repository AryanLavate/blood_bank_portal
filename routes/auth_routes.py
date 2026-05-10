"""
auth_routes.py
--------------
Handles registration and login for all three user types:
  - Donors (users)
  - Hospitals
  - Admins
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from utils.helpers import hash_password, check_password
from models.user_model import create_user, get_user_by_email
from models.hospital_model import create_hospital, get_hospital_by_email
from models.admin_model import get_admin_by_username

auth_bp = Blueprint('auth', __name__)


# ------------------------------------------------------------------
# Home Page
# ------------------------------------------------------------------

@auth_bp.route('/')
def home():
    return render_template('index.html')


# ------------------------------------------------------------------
# Donor Registration and Login
# ------------------------------------------------------------------

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name     = request.form.get('name', '').strip()
        age      = request.form.get('age', '').strip()
        blood    = request.form.get('blood', '').strip().upper()
        organ    = 1 if request.form.get('organ_donor') else 0
        phone    = request.form.get('phone', '').strip()
        email    = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        city     = request.form.get('city', '').strip()

        # Basic validation
        if not all([name, age, blood, phone, email, password, city]):
            flash('All fields are required.', 'danger')
            return render_template('auth/register.html')

        # Check if email already exists
        existing = get_user_by_email(email)
        if existing:
            flash('An account with this email already exists.', 'danger')
            return render_template('auth/register.html')

        create_user(name, age, blood, organ, phone, email, password, city)
        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        user = get_user_by_email(email)
        if user and check_password(password, user[7]):
            session['user_id']   = user[0]
            session['user_name'] = user[1]
            session['role']      = 'donor'
            flash('Welcome back, ' + user[1] + '!', 'success')
            return redirect(url_for('user.dashboard'))

        flash('Invalid email or password.', 'danger')

    return render_template('auth/login.html')


# ------------------------------------------------------------------
# Hospital Registration and Login
# ------------------------------------------------------------------

@auth_bp.route('/hospital/register', methods=['GET', 'POST'])
def hospital_register():
    if request.method == 'POST':
        name     = request.form.get('hospital_name', '').strip()
        email    = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        phone    = request.form.get('phone', '').strip()
        city     = request.form.get('city', '').strip()

        if not all([name, email, password, phone, city]):
            flash('All fields are required.', 'danger')
            return render_template('auth/hospital_register.html')

        existing = get_hospital_by_email(email)
        if existing:
            flash('A hospital account with this email already exists.', 'danger')
            return render_template('auth/hospital_register.html')

        create_hospital(name, email, password, phone, city)
        flash('Hospital registered. Please log in.', 'success')
        return redirect(url_for('auth.hospital_login'))

    return render_template('auth/hospital_register.html')


@auth_bp.route('/hospital/login', methods=['GET', 'POST'])
def hospital_login():
    if request.method == 'POST':
        email    = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()

        hospital = get_hospital_by_email(email)
        if hospital and check_password(password, hospital[3]):
            session['hospital_id']   = hospital[0]
            session['hospital_name'] = hospital[1]
            session['role']          = 'hospital'
            flash('Welcome, ' + hospital[1] + '!', 'success')
            return redirect(url_for('hospital.dashboard'))

        flash('Invalid email or password.', 'danger')

    return render_template('auth/hospital_login.html')


# ------------------------------------------------------------------
# Admin Login
# ------------------------------------------------------------------

@auth_bp.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()

        admin = get_admin_by_username(username)
        if admin and check_password(password, admin[2]):
            session['admin_id']       = admin[0]
            session['admin_username'] = admin[1]
            session['role']           = 'admin'
            flash('Admin login successful.', 'success')
            return redirect(url_for('admin.dashboard'))

        flash('Invalid admin credentials.', 'danger')

    return render_template('auth/admin_login.html')


# ------------------------------------------------------------------
# Logout (shared for all roles)
# ------------------------------------------------------------------

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.home'))