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
- PostgreSQL (`psycopg2-binary`)
- Gunicorn (production / Render)
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
├── app.py                 # Flask app factory
├── run.py                 # App instance for dev + gunicorn (run:app)
├── config.py              # Environment-driven configuration
├── requirements.txt       # Python dependencies
├── Procfile               # Render: gunicorn web process
└── .env.example           # Environment variable template
```

## Getting Started (local)

### Prerequisites

- Python 3.10 or newer
- PostgreSQL 14+ (schema uses `EXECUTE FUNCTION` on triggers; use PostgreSQL 14+ or adjust the trigger line in `database/schema.sql` for older servers)

### Installation

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### Configuration

```bash
copy .env.example .env
```

Either set **`DATABASE_URL`** (single connection string) or **`DB_HOST` / `DB_USER` / `DB_PASSWORD` / `DB_NAME`** (and optional `DB_PORT`).

### Database setup

Create an empty database, then apply the schema:

```bash
# Example (psql): createdb blood_bank_portal
python database/init_db.py
python admin/add_admin.py
```

Or use the interactive wizard (writes `.env`, applies schema + patches):

```bash
python db_setup.py
```

### Run the app (development)

```bash
python run.py
```

Open `http://127.0.0.1:5000`.

---

## Deploy on Render

### PostgreSQL

1. Create a **PostgreSQL** instance on Render.
2. Copy **Internal Database URL** or **External Database URL** into your web service as `DATABASE_URL`.

### Web service

| Setting | Value |
|--------|--------|
| **Build command** | `pip install -r requirements.txt` |
| **Start command** | `gunicorn run:app --bind 0.0.0.0:$PORT` (or rely on `Procfile`) |

Render sets **`PORT`** automatically; **`Procfile`** in this repo uses gunicorn with that port.

### Environment variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Yes* | `postgresql://...` from Render Postgres (*or set `DB_*` instead) |
| `SECRET_KEY` | Yes | Long random string for Flask sessions |
| `PGSSLMODE` | Sometimes | Use `require` if your URL has no `sslmode` and SSL is mandatory |
| `FLASK_DEBUG` | No | Set `false` in production |

Example `DATABASE_URL` (shape only; use your real URL):

```text
postgresql://user:password@dpg-xxxxx-a.oregon-postgres.render.com:5432/dbname
```

If the app cannot connect, append query params or set `PGSSLMODE=require`:

```text
postgresql://user:pass@host:5432/dbname?sslmode=require
```

After deploy, run migrations once from Render **Shell** (if needed):

```bash
python database/init_db.py
python admin/add_admin.py
```

---

## Production notes

- Use a strong `SECRET_KEY`.
- Set `FLASK_DEBUG=false` (or omit; default in `config.py` is false unless `FLASK_DEBUG` is truthy).
- The app uses `gunicorn run:app` where `app` is the Flask instance defined in `run.py`.
