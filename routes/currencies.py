# routes/currencies.py
# Handles the  GET /currencies  endpoint.
#
# A Blueprint groups related routes so we can keep each file focused.

from flask import Blueprint, jsonify
from services.exchange_service import get_all_currencies

# Create a Blueprint named "currencies".
# The name is used internally by Flask (e.g. for url_for()).
currencies_bp = Blueprint('currencies', __name__)


@currencies_bp.route('/currencies', methods=['GET'])
def list_currencies():
    """
    GET /currencies
    Returns a list of all supported currency codes with names and symbols.

    Example response:
    {
        "currencies": [
            { "code": "USD", "name": "US Dollar", "symbol": "$" },
            ...
        ]
    }
    """
    currencies = get_all_currencies()
    return jsonify({"currencies": currencies}), 200
