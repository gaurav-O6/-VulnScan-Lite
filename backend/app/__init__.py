from flask import Flask

from app.config import Config
from app.extensions import db, migrate
from app.api.health import health_bp

# Import models so Flask-Migrate can discover them
from app.models import Scan


def create_app():
    """
    Application Factory.
    Creates and configures the Flask application.
    """

    app = Flask(__name__)

    # Load configuration
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register API blueprints
    app.register_blueprint(health_bp)

    return app