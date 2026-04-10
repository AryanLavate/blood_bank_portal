"""
admin_routes.py
---------------
Routes for the admin panel: manage users, hospitals,
blood requests, statistics, and more.
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from utils.helpers import admin_login_required
from models.user_model import (
    get_all_users, delete_user, verify_user, count_users
)
from models.hospital_model import (
    get_all_hospitals, delete_hospital, verify_hospital, count_hospitals
)
from models.blood_request_model import (
    get_all_blood_requests, delete_blood_request, count_blood_requests
)
from models.organ_request_model import get_all_organ_requests, delete_organ_request
from models.donation_model import get_all_donations, count_donations
from models.blood_stock_model import get_all_stock

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/admin/dashboard')
@admin_login_required
def dashboard():
    # Collect summary statistics for the admin overview cards
    stats = {
        'total_users':     count_users(),
        'total_hospitals': count_hospitals(),
        'total_requests':  count_blood_requests(),
        'total_donations': count_donations(),
    }
    return render_template('admin/dashboard.html', stats=stats)


@admin_bp.route('/admin/users')
@admin_login_required
def manage_users():
    users = get_all_users()
    return render_template('admin/manage_users.html', users=users)


@admin_bp.route('/admin/users/delete/<int:user_id>', methods=['POST'])
@admin_login_required
def delete_user_route(user_id):
    delete_user(user_id)
    flash('User deleted successfully.', 'success')
    return redirect(url_for('admin.manage_users'))


@admin_bp.route('/admin/users/verify/<int:user_id>', methods=['POST'])
@admin_login_required
def verify_user_route(user_id):
    verify_user(user_id)
    flash('User verified successfully.', 'success')
    return redirect(url_for('admin.manage_users'))


@admin_bp.route('/admin/hospitals')
@admin_login_required
def manage_hospitals():
    hospitals = get_all_hospitals()
    return render_template('admin/manage_hospitals.html', hospitals=hospitals)


@admin_bp.route('/admin/hospitals/delete/<int:hospital_id>', methods=['POST'])
@admin_login_required
def delete_hospital_route(hospital_id):
    delete_hospital(hospital_id)
    flash('Hospital deleted successfully.', 'success')
    return redirect(url_for('admin.manage_hospitals'))


@admin_bp.route('/admin/hospitals/verify/<int:hospital_id>', methods=['POST'])
@admin_login_required
def verify_hospital_route(hospital_id):
    verify_hospital(hospital_id)
    flash('Hospital verified successfully.', 'success')
    return redirect(url_for('admin.manage_hospitals'))


@admin_bp.route('/admin/blood_requests')
@admin_login_required
def blood_requests():
    requests = get_all_blood_requests()
    return render_template('admin/blood_requests.html', requests=requests)


@admin_bp.route('/admin/blood_requests/delete/<int:req_id>', methods=['POST'])
@admin_login_required
def delete_request_route(req_id):
    delete_blood_request(req_id)
    flash('Blood request deleted.', 'success')
    return redirect(url_for('admin.blood_requests'))


@admin_bp.route('/admin/organ_requests')
@admin_login_required
def organ_requests():
    requests = get_all_organ_requests()
    return render_template('admin/organ_requests.html', requests=requests)


@admin_bp.route('/admin/organ_requests/delete/<int:req_id>', methods=['POST'])
@admin_login_required
def delete_organ_request_route(req_id):
    delete_organ_request(req_id)
    flash('Organ request deleted.', 'success')
    return redirect(url_for('admin.organ_requests'))


@admin_bp.route('/admin/statistics')
@admin_login_required
def statistics():
    donations = get_all_donations()
    stock     = get_all_stock()
    stats = {
        'total_users':     count_users(),
        'total_hospitals': count_hospitals(),
        'total_requests':  count_blood_requests(),
        'total_donations': count_donations(),
    }
    return render_template(
        'admin/statistics.html',
        donations=donations,
        stock=stock,
        stats=stats
    )