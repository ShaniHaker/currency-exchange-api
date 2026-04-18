# models/history.py
# Data model for a conversion history record.

from dataclasses import dataclass


@dataclass
class HistoryRecord:
    """
    Represents one saved conversion result.

    Attributes:
        id               : String version of MongoDB's _id (ObjectId → str)
        from_currency    : Source currency code, e.g. "USD"
        to_currency      : Target currency code, e.g. "ILS"
        amount           : Original amount that was converted
        rate             : Exchange rate that was used
        converted_amount : The resulting amount after conversion
        created_at       : ISO 8601 timestamp of when the conversion happened
    """
    id: str
    from_currency: str
    to_currency: str
    amount: float
    rate: float
    converted_amount: float
    created_at: str

    def to_dict(self) -> dict:
        return {
            "id":              self.id,
            "fromCurrency":    self.from_currency,
            "toCurrency":      self.to_currency,
            "amount":          self.amount,
            "rate":            self.rate,
            "convertedAmount": self.converted_amount,
            "createdAt":       self.created_at,
        }
