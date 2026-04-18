# services/history_service.py
# Business logic for the conversion history collection.

from datetime import datetime, timezone
from database import get_db
from models.history import HistoryRecord
from models.currency import ConversionResult


# ---------------------------------------------------------------------------
# Private helper
# ---------------------------------------------------------------------------

def _doc_to_history(doc: dict) -> HistoryRecord:
    """Convert a raw MongoDB document into a HistoryRecord dataclass."""
    return HistoryRecord(
        id=str(doc["_id"]),
        from_currency=doc["fromCurrency"],
        to_currency=doc["toCurrency"],
        amount=doc["amount"],
        rate=doc["rate"],
        converted_amount=doc["convertedAmount"],
        created_at=doc["createdAt"],
    )


# ---------------------------------------------------------------------------
# Public service functions
# ---------------------------------------------------------------------------

def save_conversion(result: ConversionResult) -> None:
    """
    Persist a completed conversion to the history collection.

    Called automatically by the /convert route after every successful
    conversion.  If the database write fails for any reason, the error
    is re-raised so the caller can decide how to handle it.

    Parameters:
        result : The ConversionResult returned by exchange_service
    """
    db = get_db()

    doc = {
        "fromCurrency":    result.from_currency,
        "toCurrency":      result.to_currency,
        "amount":          result.amount,
        "rate":            result.rate,
        "convertedAmount": result.converted_amount,
        # Use the current time as the "saved at" timestamp, not the rate timestamp
        "createdAt":       datetime.now(timezone.utc).isoformat(),
    }

    db.history.insert_one(doc)


def get_history() -> list[dict]:
    """
    Return all conversion history records, most recent first.
    """
    db = get_db()
    docs = db.history.find(sort=[("createdAt", -1)])
    return [_doc_to_history(doc).to_dict() for doc in docs]
