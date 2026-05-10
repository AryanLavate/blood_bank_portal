"""
run.py
------
Exposes `app` for Gunicorn:  gunicorn run:app --bind 0.0.0.0:$PORT

Render sets PORT; local dev uses PORT or 5000.
"""

import os

from app import create_app

app = create_app()

if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", "5000"))
    debug = os.getenv("FLASK_DEBUG", "false").lower() in ("1", "true", "yes")

    print("Login URLs:")
    print(f"- User (Donor): http://{host}:{port}/login")
    print(f"- Admin:        http://{host}:{port}/admin/login")

    app.run(debug=debug, host=host, port=port)
