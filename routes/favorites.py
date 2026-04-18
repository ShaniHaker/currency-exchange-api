# routes/favorites.py
# Handles all /favorites endpoints.

from flask import Blueprint, jsonify, request
from services.favorites_service import get_favorites, add_favorite, delete_favorite
from services.exchange_service import SUPPORTED_CURRENCIES

favorites_bp = Blueprint('favorites', __name__)

# The set of valid currency codes (used for input validation below)
VALID_CODES = set(SUPPORTED_CURRENCIES.keys())


@favorites_bp.route('/favorites', methods=['GET'])
def list_favorites():
    """
    GET /favorites
    Returns all saved favorite currency pairs, newest first.

    Example response:
    {
        "favorites": [
            {
                "id": "665f1a2b3c4d5e6f7a8b9c0d",
                "fromCurrency": "USD",
                "toCurrency": "ILS",
                "nickname": "Dollar to Shekel",
                "createdAt": "2024-06-04T10:00:00+00:00"
            }
        ]
    }
    """
    try:
        favorites = get_favorites()
    except RuntimeError as e:
        # RuntimeError is raised by get_db() when MongoDB is not configured
        return jsonify({"error": str(e)}), 503

    return jsonify({"favorites": favorites}), 200


@favorites_bp.route('/favorites', methods=['POST'])
def create_favorite():
    """
    POST /favorites
    Save a new favorite currency pair.

    Request body (JSON):
    {
        "fromCurrency": "USD",       <- required
        "toCurrency":   "ILS",       <- required
        "nickname":     "My pair"    <- optional
    }

    Example response (201 Created):
    {
        "favorite": {
            "id": "665f1a2b3c4d5e6f7a8b9c0d",
            "fromCurrency": "USD",
            "toCurrency": "ILS",
            "nickname": "My pair",
            "createdAt": "2024-06-04T10:00:00+00:00"
        }
    }
    """
    # request.get_json() parses the incoming JSON body.
    # silent=True returns None instead of raising an error for bad JSON.
    body = request.get_json(silent=True)

    if not body:
        return jsonify({
            "error": "Request body must be JSON.",
            "example": {"fromCurrency": "USD", "toCurrency": "ILS", "nickname": "Dollar to Shekel"}
        }), 400

    from_currency = body.get("fromCurrency", "").upper()
    to_currency   = body.get("toCurrency",   "").upper()
    nickname      = body.get("nickname", "").strip()   # optional

    # --- Validate required fields ---
    if not from_currency or not to_currency:
        return jsonify({
            "error": "'fromCurrency' and 'toCurrency' are required."
        }), 400

    if from_currency not in VALID_CODES or to_currency not in VALID_CODES:
        return jsonify({
            "error": f"Unsupported currency code(s): '{from_currency}', '{to_currency}'.",
            "supported": list(VALID_CODES)
        }), 400

    if from_currency == to_currency:
        return jsonify({
            "error": "'fromCurrency' and 'toCurrency' must be different."
        }), 400

    try:
        favorite = add_favorite(from_currency, to_currency, nickname)
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 503

    # 201 Created is the correct HTTP status for a successful resource creation
    return jsonify({"favorite": favorite}), 201


@favorites_bp.route('/favorites/<id>', methods=['DELETE'])
def remove_favorite(id):
    """
    DELETE /favorites/<id>
    Delete a saved favorite by its ID.

    URL parameter:
        id : The favorite's ID string (returned by POST /favorites)

    Responses:
        200  : Favorite deleted successfully
        404  : No favorite with that ID found
        400  : ID format is invalid
        503  : Database unavailable
    """
    try:
        deleted = delete_favorite(id)
    except ValueError as e:
        # Raised when the ID string is not a valid MongoDB ObjectId format
        return jsonify({"error": str(e)}), 400
    except RuntimeError as e:
        return jsonify({"error": str(e)}), 503

    if not deleted:
        return jsonify({"error": f"No favorite found with id '{id}'."}), 404

    return jsonify({"message": f"Favorite '{id}' deleted successfully."}), 200
