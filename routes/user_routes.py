"""
user_routes.py
--------------
Routes for the donor/user dashboard, profile management,
availability updates, and viewing blood requests and notifications.
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from utils.helpers import login_required
from models.user_model import (
    get_user_by_id, update_user_availability, update_user_profile
)
from models.blood_request_model import get_blood_requests_for_donor
from models.organ_request_model import get_organ_requests_for_donor
from models.notification_model import (
    get_notifications_for_user, mark_all_read, count_unread
)
from models.donation_model import get_donations_by_user

user_bp = Blueprint('user', __name__)


@user_bp.route('/donor/dashboard')
@login_required
def dashboard():
    user_id = session['user_id']
    user    = get_user_by_id(user_id)

    # columns: id, name, age, blood_group, organ_donor, phone, email,
    #          password, city, availability_status, is_verified, created_at
    blood_group = user[3]
    city        = user[8]

    # Fetch blood requests that match this donor's city
    requests = get_blood_requests_for_donor(city)
    organ_requests = get_organ_requests_for_donor(city)

    # Count unread notifications
    unread_count = count_unread(user_id)

    return render_template(
        'donor/dashboard.html',
        user=user,
        requests=requests,
        organ_requests=organ_requests,
        unread_count=unread_count
    )


@user_bp.route('/donor/profile')
@login_required
def profile():
    user = get_user_by_id(session['user_id'])
    donations = get_donations_by_user(session['user_id'])
    return render_template('donor/profile.html', user=user, donations=donations)


@user_bp.route('/donor/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user_id = session['user_id']
    user    = get_user_by_id(user_id)

    if request.method == 'POST':
        name        = request.form.get('name', '').strip()
        age         = request.form.get('age', '').strip()
        phone       = request.form.get('phone', '').strip()
        city        = request.form.get('city', '').strip()
        organ_donor = 1 if request.form.get('organ_donor') else 0

        update_user_profile(user_id, name, age, phone, city, organ_donor)
        session['user_name'] = name
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('user.profile'))

    return render_template('donor/edit_profile.html', user=user)


@user_bp.route('/donor/availability', methods=['POST'])
@login_required
def update_availability():
    status = request.form.get('status', 'Available')
    update_user_availability(session['user_id'], status)
    flash('Availability status updated to ' + status + '.', 'success')
    return redirect(url_for('user.dashboard'))


@user_bp.route('/donor/requests')
@login_required
def view_requests():
    user        = get_user_by_id(session['user_id'])
    city        = user[8]
    requests       = get_blood_requests_for_donor(city)
    organ_requests = get_organ_requests_for_donor(city)
    return render_template('donor/view_requests.html', requests=requests, organ_requests=organ_requests, user=user)


@user_bp.route('/donor/notifications')
@login_required
def notifications():
    user_id       = session['user_id']
    notifications = get_notifications_for_user(user_id)
    mark_all_read(user_id)
    return render_template('donor/notifications.html', notifications=notifications)