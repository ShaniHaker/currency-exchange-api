# app.py
# This is the main entry point for the Currency Exchange API.
# It creates the Flask app, registers all routes, and starts the server.

from flask import Flask
from routes.currencies import currencies_bp
from routes.rates import rates_bp
from routes.convert import convert_bp
from routes.favorites import favorites_bp
from routes.history import history_bp
from database import init_db
from config import Config


def create_app():
    """
    Application factory function.
    Creates and configures the Flask app instance.
    """
    app = Flask(__name__)

    # Load configuration from config.py
    app.config.from_object(Config)

    # Register route blueprints.
    # A Blueprint is a way to organize a group of related routes.
    app.register_blueprint(currencies_bp)
    app.register_blueprint(rates_bp)
    app.register_blueprint(convert_bp)
    app.register_blueprint(favorites_bp)
    app.register_blueprint(history_bp)

    # Create the MongoDB client once at startup and reuse it for all requests.
    init_db(app)

    return app


# Run the app when this file is executed directly (e.g. `python app.py`)
if __name__ == '__main__':
    import os
    app = create_app()
    # Railway (and most cloud platforms) set a PORT environment variable.
    # We read it here so the app binds to the right port automatically.
    # Locally it falls back to 5000.
    port = int(os.environ.get('PORT', 5000))
    # debug=True enables auto-reload and detailed error pages during development.
    # Never use debug=True in production!
    app.run(host="0.0.0.0", port=port, debug=True)
