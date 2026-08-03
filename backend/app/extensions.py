from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address


# Database instance
db = SQLAlchemy()


# Database migration instance
migrate = Migrate()


# Rate limiter instance
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[],
)