# Blood Bank and Organ Donation Portal

A Flask-based web application for coordinating blood donation and organ donor workflows between donors, hospitals, and administrators.

## Features

- Multi-role authentication (Donor, Hospital, Admin)
- Donor profile and availability management
- Hospital blood request posting and donor matching
- Blood stock management for hospitals
- Admin dashboard for verification and oversight
- Session-based protected routes

## Tech Stack

- Python 3.10+
- Flask
- MySQL (`mysqlclient`)
- Bootstrap 5
- HTML/CSS/JavaScript

## Project Structure

```text
blood_bank_portal/
├── admin/                 # Admin scripts (e.g., first admin creation)
├── database/              # DB schema and initialization scripts
├── models/                # Data access and business logic
├── routes/                # Flask route handlers
├── static/                # CSS/JS assets
├── templates/             # Jinja2 templates
├── utils/                 # DB connection and helper utilities
├── app.py                 # Flask app setup
├── config.py              # Environment-driven configuration
├── run.py                 # App entry point
├── requirements.txt       # Python dependencies
└── .env.example           # Environment variable template
```

## Getting Started

### Prerequisites

- Python 3.10 or newer
- MySQL Server

### Installation

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Configuration

Copy the environment template and update values:

```bash
copy .env.example .env
```

Required variables:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_NAME=blood_bank_portal
SECRET_KEY=replace-with-a-strong-random-secret
```

### Database Setup

```bash
python database/init_db.py
python admin/add_admin.py
```

### Run the App

```bash
python run.py
```

Open `http://127.0.0.1:5000`.

## Security Notes

- Passwords are hashed before storage.
- SQL queries use parameterized inputs.
- Sensitive credentials are managed through `.env`.
- `.env` is ignored by Git to prevent secret leaks.
