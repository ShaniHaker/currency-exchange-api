# models/favorite.py
# Data model for a saved currency-pair favorite.

from dataclasses import dataclass


@dataclass
class Favorite:
    """
    Represents a user-saved currency pair.

    Attributes:
        id            : String version of MongoDB's _id (ObjectId → str)
        from_currency : Source currency code, e.g. "USD"
        to_currency   : Target currency code, e.g. "ILS"
        nickname      : Optional human-readable label, e.g. "Dollar to Shekel"
        created_at    : ISO 8601 timestamp of when this favorite was saved
    """
    id: str
    from_currency: str
    to_currency: str
    nickname: str
    created_at: str

    def to_dict(self) -> dict:
        return {
            "id":           self.id,
            "fromCurrency": self.from_currency,
            "toCurrency":   self.to_currency,
            "nickname":     self.nickname,
            "createdAt":    self.created_at,
        }
