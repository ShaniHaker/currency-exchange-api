# routes/history.py
# Handles the GET /history endpoint.

from flask import Blueprint, jsonify
from services.history_service import get_history

history_bp = Blueprint('history', __name__)


@history_bp.route('/history', methods=['GET'])
def list_history():
    """
    GET /history
    Returns all past conversions, most recent first.

    Example response:
    {
        "history": [
            {
                "id": "665f1a2b3c4d5e6f7a8b9c0d",
                "fromCurrency": "USD",
                "toCurrency": "ILS",
                "amount": 100.0,
                "rate": 3.68,
                "convertedAmount": 368.0,
                "createdAt": "2024-06-04T10:00:00+00:00"
            }
        ]
    }
    """
    try:
        history = get_history()
    except RuntimeError as e:
        # RuntimeError is raised by get_db() when MongoDB is not configured
        return jsonify({"error": str(e)}), 503

    return jsonify({"history": history}), 200
