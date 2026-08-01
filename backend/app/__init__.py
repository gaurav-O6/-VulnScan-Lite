from flask import Flask
from flask_cors import CORS

from app.config import Config
from app.extensions import db, migrate

from app.api import (
    health_bp,
    scans_bp,
)

from app.models import Scan


def create_app():
    """
    Application Factory.

    Creates and configures the Flask application.
    """

    app = Flask(__name__)


    app.config.from_object(Config)


    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": [
                    "http://localhost:5173",
                    "http://localhost:5174",
                ]
            }
        },
    )


    db.init_app(app)

    migrate.init_app(
        app,
        db
    )


    app.register_blueprint(
        health_bp
    )

    app.register_blueprint(
        scans_bp
    )


    return app