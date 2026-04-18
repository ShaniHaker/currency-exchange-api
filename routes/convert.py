# routes/convert.py
# Handles the  GET /convert?from=USD&to=ILS&amount=100  endpoint.
# After every successful conversion the result is saved to history.

from flask import Blueprint, jsonify, request
from services.exchange_service import convert_currency, SUPPORTED_CURRENCIES, ExternalAPIError
from services.history_service import save_conversion

convert_bp = Blueprint('convert', __name__)


@convert_bp.route('/convert', methods=['GET'])
def convert():
    """
    GET /convert?from=<code>&to=<code>&amount=<number>
    Converts an amount from one currency to another using the live rate.
    The result is automatically saved to the conversion history.

    Query parameters:
        from    (required) : Source currency code, e.g. USD
        to      (required) : Target currency code, e.g. ILS
        amount  (required) : Numeric amount to convert, e.g. 100

    Example response:
    {
        "from": "USD",
        "to": "ILS",
        "amount": 100.0,
        "rate": 3.68,
        "convertedAmount": 368.0,
        "timestamp": "Tue, 14 Apr 2026 00:02:31 +0000"
    }
    """
    from_code  = request.args.get('from',   '').upper()
    to_code    = request.args.get('to',     '').upper()
    amount_str = request.args.get('amount', '')

    # Validate that all three parameters were provided
    if not from_code or not to_code or not amount_str:
        return jsonify({
            "error": "Query parameters 'from', 'to', and 'amount' are all required.",
            "example": "/convert?from=USD&to=ILS&amount=100"
        }), 400

    # Validate that amount is a valid positive number
    try:
        amount = float(amount_str)
        if amount <= 0:
            raise ValueError
    except ValueError:
        return jsonify({"error": "'amount' must be a positive number."}), 400

    # Validate that both currency codes are in our supported list
    if from_code not in SUPPORTED_CURRENCIES or to_code not in SUPPORTED_CURRENCIES:
        return jsonify({
            "error": f"Unsupported currency code(s): '{from_code}', '{to_code}'.",
            "supported": list(SUPPORTED_CURRENCIES.keys())
        }), 400

    # --- Fetch the live rate and calculate the conversion ---
    try:
        result = convert_currency(from_code, to_code, amount)
    except ExternalAPIError as e:
        return jsonify({"error": str(e)}), 503

    # --- Save the result to MongoDB history ---
    # We try to save but do NOT block the response if the DB is unavailable.
    # The conversion itself succeeded, so we still return 200 to the caller.
    try:
        save_conversion(result)
    except Exception:
        pass

    return jsonify(result.to_dict()), 200
