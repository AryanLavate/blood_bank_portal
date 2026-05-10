"""
run.py
------
Entry point for local development and gunicorn (Render).
Gunicorn: gunicorn run:app --bind 0.0.0.0:$PORT
"""

import os

from app import create_app

app = create_app()

if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "true").lower() in ("1", "true", "yes")

    print("Login URLs:")
    print(f"- User (Donor): http://{host}:{port}/login")
    print(f"- Admin:        http://{host}:{port}/admin/login")

    app.run(debug=debug, host=host, port=port)
