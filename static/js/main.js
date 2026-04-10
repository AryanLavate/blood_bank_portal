/*
 * main.js
 * Client-side interactivity for Blood Bank and Organ Donation Portal
 */

// ---- Auto-dismiss flash alerts after 4 seconds ----
document.addEventListener('DOMContentLoaded', function () {

    var alerts = document.querySelectorAll('.alert-auto-dismiss');
    alerts.forEach(function (alert) {
        setTimeout(function () {
            alert.style.transition = 'opacity 0.5s';
            alert.style.opacity = '0';
            setTimeout(function () {
                alert.remove();
            }, 500);
        }, 4000);
    });

    // ---- Blood group filter: uppercase input automatically ----
    var bgInputs = document.querySelectorAll('input[data-blood-group]');
    bgInputs.forEach(function (input) {
        input.addEventListener('input', function () {
            this.value = this.value.toUpperCase();
        });
    });

    // ---- Confirm delete dialogs ----
    var deleteForms = document.querySelectorAll('form[data-confirm]');
    deleteForms.forEach(function (form) {
        form.addEventListener('submit', function (e) {
            var msg = form.getAttribute('data-confirm') || 'Are you sure?';
            if (!confirm(msg)) {
                e.preventDefault();
            }
        });
    });

    // ---- Highlight urgent blood request rows ----
    var urgencyBadges = document.querySelectorAll('.badge-urgent');
    urgencyBadges.forEach(function (badge) {
        var row = badge.closest('tr');
        if (row) {
            row.classList.add('row-urgent');
        }
    });

    // ---- Stock units: color feedback ----
    var stockInputs = document.querySelectorAll('input[data-stock-units]');
    stockInputs.forEach(function (input) {
        input.addEventListener('input', function () {
            var val = parseInt(this.value) || 0;
            if (val === 0) {
                this.classList.add('is-invalid');
                this.classList.remove('is-valid');
            } else {
                this.classList.remove('is-invalid');
                this.classList.add('is-valid');
            }
        });
    });

});