"""
hospital_routes.py
------------------
Routes for the hospital dashboard, blood and organ request management,
blood stock updates, and viewing nearby donors.
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from utils.helpers import hospital_login_required
from models.hospital_model import get_hospital_by_id
from models.blood_request_model import (
    create_blood_request, get_blood_requests_by_hospital, close_blood_request
)
from models.organ_request_model import (
    create_organ_request, get_organ_requests_by_hospital
)
from models.blood_stock_model import get_stock_by_hospital, upsert_blood_stock
from models.user_model import search_donors
from models.notification_model import notify_matching_donors

hospital_bp = Blueprint('hospital', __name__)


@hospital_bp.route('/hospital/dashboard')
@hospital_login_required
def dashboard():
    hospital_id = session['hospital_id']
    hospital    = get_hospital_by_id(hospital_id)
    requests    = get_blood_requests_by_hospital(hospital_id)
    organ_reqs  = get_organ_requests_by_hospital(hospital_id)
    stock       = get_stock_by_hospital(hospital_id)
    return render_template(
        'hospital/dashboard.html',
        hospital=hospital,
        requests=requests,
        organ_requests=organ_reqs,
        stock=stock
    )


@hospital_bp.route('/hospital/blood_request', methods=['GET', 'POST'])
@hospital_login_required
def create_request():
    hospital_id = session['hospital_id']
    hospital    = get_hospital_by_id(hospital_id)

    if request.method == 'POST':
        blood_group     = request.form.get('blood_group', '').strip().upper()
        units_required  = request.form.get('units_required', '').strip()
        city            = request.form.get('city', hospital[5]).strip()
        urgency         = request.form.get('urgency', 'Normal')

        if not all([blood_group, units_required, city]):
            flash('All fields are required.', 'danger')
            return render_template('hospital/create_request.html', hospital=hospital)

        create_blood_request(hospital_id, blood_group, units_required, city, urgency)

        # Automatically notify matching donors
        msg = ('Urgent blood request: ' + blood_group + ' blood needed at ' +
               hospital[1] + ' in ' + city + '. Please respond if available.')
        notify_matching_donors(blood_group, city, msg)

        flash('Blood request posted. Matching donors have been notified.', 'success')
        return redirect(url_for('hospital.dashboard'))

    return render_template('hospital/create_request.html', hospital=hospital)


@hospital_bp.route('/hospital/close_request/<int:req_id>', methods=['POST'])
@hospital_login_required
def close_request(req_id):
    close_blood_request(req_id)
    flash('Request marked as fulfilled.', 'success')
    return redirect(url_for('hospital.dashboard'))


@hospital_bp.route('/hospital/organ_request', methods=['GET', 'POST'])
@hospital_login_required
def organ_request():
    hospital_id = session['hospital_id']
    hospital    = get_hospital_by_id(hospital_id)

    if request.method == 'POST':
        organ_type  = request.form.get('organ_type', '').strip()
        blood_group = request.form.get('blood_group', '').strip().upper()
        city        = request.form.get('city', hospital[5]).strip()
        urgency     = request.form.get('urgency', 'Normal')
        notes       = request.form.get('notes', '').strip()

        if not organ_type:
            flash('Organ type is required.', 'danger')
            return render_template('hospital/organ_request.html', hospital=hospital)

        create_organ_request(hospital_id, organ_type, blood_group, city, urgency, notes)

        # Automatically notify matching donors
        msg = ('Urgent organ transplant request: ' + organ_type + ' needed at ' +
               hospital[1] + ' in ' + city + '. Please respond if available.')
        notify_matching_donors(blood_group, city, msg)

        flash('Organ transplant request posted successfully. Matching donors have been notified.', 'success')
        return redirect(url_for('hospital.dashboard'))

    return render_template('hospital/organ_request.html', hospital=hospital)


@hospital_bp.route('/hospital/blood_stock', methods=['GET', 'POST'])
@hospital_login_required
def blood_stock():
    hospital_id = session['hospital_id']
    hospital    = get_hospital_by_id(hospital_id)

    if request.method == 'POST':
        blood_group      = request.form.get('blood_group', '').strip().upper()
        units_available  = request.form.get('units_available', '0').strip()
        upsert_blood_stock(hospital_id, blood_group, units_available)
        flash('Blood stock updated for ' + blood_group + '.', 'success')
        return redirect(url_for('hospital.blood_stock'))

    stock = get_stock_by_hospital(hospital_id)
    return render_template('hospital/blood_stock.html', stock=stock, hospital=hospital)


@hospital_bp.route('/hospital/view_donors')
@hospital_login_required
def view_donors():
    blood_group = request.args.get('blood_group', '')
    city        = request.args.get('city', '')
    availability = request.args.get('availability', 'Available')

    donors = search_donors(
        blood_group=blood_group or None,
        city=city or None,
        availability=availability or None
    )
    return render_template(
        'hospital/view_donors.html',
        donors=donors,
        blood_group=blood_group,
        city=city,
        availability=availability
    )