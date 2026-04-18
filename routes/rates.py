# routes/rates.py
# Handles the  GET /rates?from=USD&to=ILS  endpoint.

from flask import Blueprint, jsonify, request
from services.exchange_service import get_exchange_rate, SUPPORTED_CURRENCIES, ExternalAPIError

rates_bp = Blueprint('rates', __name__)


@rates_bp.route('/rates', methods=['GET'])
def exchange_rate():
    """
    GET /rates?from=<code>&to=<code>
    Returns the live exchange rate between two currencies.

    Query parameters:
        from  (required) : Source currency code, e.g. USD
        to    (required) : Target currency code, e.g. ILS

    Example response:
    {
        "from": "USD",
        "to": "ILS",
        "rate": 3.68,
        "timestamp": "2024-01-15T10:30:00+00:00"
    }
    """
    from_code = request.args.get('from', '').upper()
    to_code   = request.args.get('to',   '').upper()

    # Validate that both parameters were provided
    if not from_code or not to_code:
        return jsonify({
            "error": "Both 'from' and 'to' query parameters are required.",
            "example": "/rates?from=USD&to=ILS"
        }), 400

    # Validate that both codes are in our supported list
    if from_code not in SUPPORTED_CURRENCIES or to_code not in SUPPORTED_CURRENCIES:
        return jsonify({
            "error": f"Unsupported currency code(s): '{from_code}', '{to_code}'.",
            "supported": list(SUPPORTED_CURRENCIES.keys())
        }), 400

    try:
        rate = get_exchange_rate(from_code, to_code)
    except ExternalAPIError as e:
        # The external API failed — return a 503 "Service Unavailable" response.
        # 503 tells the caller "our server is fine, but a dependency is down."
        return jsonify({"error": str(e)}), 503

    return jsonify(rate.to_dict()), 200
