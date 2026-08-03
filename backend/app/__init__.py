from flask import Flask
from flask_cors import CORS

from app.config import Config
from app.extensions import (
    db,
    migrate,
    limiter,
)

from app.api import (
    health_bp,
    scans_bp,
)

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



    # Enable CORS for frontend development
    #
    # Vite can automatically move ports
    # (5173, 5174, 5175, etc.)
    # when another process occupies the port.
    #
    # Allow localhost development ports only.
    CORS(
        app,
        resources={
            r"/api/*": {
                "origins": r"http://localhost:\d+"
            }
        },
    )



    # Initialize extensions
    db.init_app(app)

    migrate.init_app(
        app,
        db
    )

    limiter.init_app(
        app
    )



    # Register API blueprints
    app.register_blueprint(
        health_bp
    )

    app.register_blueprint(
        scans_bp
    )



    return app