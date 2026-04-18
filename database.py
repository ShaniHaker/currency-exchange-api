# database.py
# Handles the MongoDB connection.
#
# HOW IT WORKS
# ------------
# A single MongoClient is created once when the app starts (in init_db),
# then reused for every request.  MongoClient is thread-safe and manages
# its own internal connection pool, so one shared instance is the right approach.
#
# MongoDB is OPTIONAL — if it is unavailable at startup (wrong URI, DNS
# failure, SSL error, Atlas timeout, etc.) the Flask app keeps running
# normally.  Only endpoints that actually use the database (/favorites,
# /history) will return 503 until the problem is resolved.

from pymongo import MongoClient
from flask import current_app

# Module-level variable that holds the single shared client.
# None means MongoDB is not available (init_db failed or was not called).
_client: MongoClient | None = None


def init_db(app) -> None:
    """
    Try to create a MongoClient and verify the connection with one ping.
    Called once from create_app() at startup.

    This function NEVER raises — any failure is printed as a warning and
    the app continues without MongoDB.  Endpoints that need the database
    will return 503 until the connection becomes available (requires restart).

    Parameters:
        app : The Flask application instance
    """
    global _client

    uri = app.config.get('MONGO_URI', '')

    if not uri:
        print(
            "[database] WARNING: MONGO_URI is not set. "
            "MongoDB features (/favorites, /history) will return 503. "
            "Copy .env.example to .env and fill in your Atlas connection string."
        )
        return

    try:
        # Use a local variable first — we only write to _client if the
        # connection actually works.  This prevents a broken client from
        # being stored in _client when something goes wrong after construction.
        #
        # Timeout settings (all in milliseconds):
        #   serverSelectionTimeoutMS : how long to wait to find a usable server
        #   connectTimeoutMS         : how long to wait for a new TCP connection
        #   socketTimeoutMS          : how long to wait for a response on a socket
        # Without these, a bad URI can hang the app for 30 seconds.
        candidate = MongoClient(
            uri,
            serverSelectionTimeoutMS=1000,
            connectTimeoutMS=1000,
            socketTimeoutMS=1000,
        )

        # Ping the server to confirm the connection is actually usable.
        # This is the call that triggers DNS resolution and the handshake.
        candidate.admin.command('ping')

        # Only store the client after a successful ping.
        _client = candidate
        print("[database] MongoDB connected successfully.")

    except Exception as e:
        # Catch everything — ConnectionFailure, ServerSelectionTimeoutError,
        # ConfigurationError (bad URI), DNS errors, SSL errors, etc.
        # We intentionally do NOT re-raise so the Flask app keeps running.
        print(
            f"[database] WARNING: Could not connect to MongoDB ({type(e).__name__}: {e}). "
            "The server will start without database support. "
            "MongoDB features (/favorites, /history, conversion history) will return 503. "
            "Fix the connection and restart the server to re-enable them."
        )


def get_db():
    """
    Return the shared MongoDB database object.

    Raises RuntimeError if MongoDB is unavailable (init_db failed or was
    never called successfully).  Routes catch this and return 503.

    Usage in a service:
        from database import get_db
        db = get_db()
        db.favorites.find()
    """
    if _client is None:
        raise RuntimeError(
            "MongoDB is not available. "
            "Check the server logs for the connection error, "
            "fix your MONGO_URI, and restart the server."
        )

    db_name = current_app.config.get('MONGO_DB_NAME', 'currency_exchange')
    return _client[db_name]
