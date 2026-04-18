# config.py
# Central configuration for the Flask app.
#
# Values that differ between environments (local vs. production) are read
# from environment variables.  python-dotenv loads those from a ".env" file
# automatically, so you never have to hard-code secrets in source code.

import os
from dotenv import load_dotenv

# Load variables from the ".env" file into os.environ.
# This must run before any os.environ.get() calls below.
load_dotenv()


class Config:
    """Base configuration shared across all environments."""

    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-secret-key')

    # --- External exchange-rate API (no key required) ---
    EXCHANGERATE_BASE_URL        = 'https://open.er-api.com/v6'
    EXCHANGERATE_TIMEOUT_SECONDS = 10

    # --- MongoDB ---
    # Paste your Atlas connection string into the .env file.
    MONGO_URI     = os.environ.get('MONGO_URI', '')
    MONGO_DB_NAME = os.environ.get('MONGO_DB_NAME', 'currency_exchange')

    # --- Flask JSON ---
    JSON_SORT_KEYS             = False
    JSONIFY_PRETTYPRINT_REGULAR = True
