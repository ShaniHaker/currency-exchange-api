# services/favorites_service.py
# Business logic for the favorites collection.
# Routes call these functions; they never touch MongoDB directly.

from datetime import datetime, timezone
from bson import ObjectId          # ObjectId is MongoDB's unique ID type
from bson.errors import InvalidId
from database import get_db
from models.favorite import Favorite


# ---------------------------------------------------------------------------
# Private helper
# ---------------------------------------------------------------------------

def _doc_to_favorite(doc: dict) -> Favorite:
    """
    Convert a raw MongoDB document (dict) into a Favorite dataclass.

    MongoDB stores the primary key as "_id" with type ObjectId.
    We convert it to a plain string so it can be included in JSON responses.
    """
    return Favorite(
        id=str(doc["_id"]),
        from_currency=doc["fromCurrency"],
        to_currency=doc["toCurrency"],
        nickname=doc.get("nickname", ""),   # nickname is optional
        created_at=doc["createdAt"],
    )


# ---------------------------------------------------------------------------
# Public service functions
# ---------------------------------------------------------------------------

def get_favorites() -> list[dict]:
    """
    Return all saved favorites, most recently added first.
    """
    db = get_db()
    # Pass sort directly to find(): [("field", direction)]  -1 = descending
    docs = db.favorites.find(sort=[("createdAt", -1)])
    return [_doc_to_favorite(doc).to_dict() for doc in docs]


def add_favorite(from_currency: str, to_currency: str, nickname: str) -> dict:
    """
    Save a new favorite currency pair and return it as a dictionary.

    If the same currency pair already exists, return the existing favorite
    instead of creating a duplicate.

    Parameters:
        from_currency : Source currency code, e.g. "USD"
        to_currency   : Target currency code, e.g. "ILS"
        nickname      : Optional label, e.g. "Dollar to Shekel"
    """
    db = get_db()

    # -----------------------------------------------------------------------
    # Prevent duplicate favorites:
    # If a favorite with the same from/to pair already exists,
    # return it instead of inserting a new document.
    # -----------------------------------------------------------------------
    existing = db.favorites.find_one({
        "fromCurrency": from_currency,
        "toCurrency": to_currency
    })

    if existing:
        return _doc_to_favorite(existing).to_dict()

    # If no duplicate exists, create a new favorite
    doc = {
        "fromCurrency": from_currency,
        "toCurrency":   to_currency,
        "nickname":     nickname,
        "createdAt":    datetime.now(timezone.utc).isoformat(),
    }

    # insert_one() returns a result object whose inserted_id is the new _id
    insert_result = db.favorites.insert_one(doc)
    doc["_id"] = insert_result.inserted_id

    return _doc_to_favorite(doc).to_dict()


def delete_favorite(id_str: str) -> bool:
    """
    Delete a favorite by its string ID.
    Returns True if a document was deleted, False if no match was found.

    Raises ValueError if `id_str` is not a valid MongoDB ObjectId format.
    """
    # Validate the ID format before opening a DB connection,
    # so a bad ID always returns 400 even when the DB is not configured.
    try:
        object_id = ObjectId(id_str)
    except InvalidId:
        raise ValueError(f"'{id_str}' is not a valid favorite ID.")

    db = get_db()

    result = db.favorites.delete_one({"_id": object_id})

    # deleted_count is 1 if a document was found and removed, 0 otherwise
    return result.deleted_count == 1
