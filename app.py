"""
app.py
------
Flask application factory.
Registers all blueprints; unchanged URL structure for production on Render.
"""

from flask import Flask

from config import DEBUG, SECRET_KEY

from routes.auth_routes import auth_bp
from routes.user_routes import user_bp
from routes.hospital_routes import hospital_bp
from routes.admin_routes import admin_bp


def create_app():
    app = Flask(__name__)
    app.secret_key = SECRET_KEY
    app.config["DEBUG"] = DEBUG

    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(hospital_bp)
    app.register_blueprint(admin_bp)

    @app.after_request
    def add_cache_control(response):
        response.headers["Cache-Control"] = (
            "no-store, no-cache, must-revalidate, max-age=0"
        )
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "-1"
        return response

    return app
