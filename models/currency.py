# models/currency.py
# Data models for the Currency Exchange API.
#
# Right now these are simple Python dataclasses used as plain data containers.
# Later, when you add a database (e.g. SQLAlchemy), you would replace these
# with database model classes that map to database tables.

from dataclasses import dataclass


@dataclass
class Currency:
    """
    Represents a single supported currency.

    Attributes:
        code    : ISO 4217 currency code, e.g. "USD"
        name    : Human-readable name, e.g. "US Dollar"
        symbol  : Currency symbol, e.g. "$"
    """
    code: str
    name: str
    symbol: str

    def to_dict(self):
        """Convert this object to a plain dictionary (easy to turn into JSON)."""
        return {
            "code": self.code,
            "name": self.name,
            "symbol": self.symbol,
        }


@dataclass
class ExchangeRate:
    """
    Represents an exchange rate between two currencies.

    Attributes:
        from_currency : The source currency code, e.g. "USD"
        to_currency   : The target currency code, e.g. "ILS"
        rate          : How many units of `to` equal one unit of `from`
        timestamp     : When this rate was recorded (ISO 8601 string)
    """
    from_currency: str
    to_currency: str
    rate: float
    timestamp: str

    def to_dict(self):
        return {
            "from": self.from_currency,
            "to": self.to_currency,
            "rate": self.rate,
            "timestamp": self.timestamp,
        }


@dataclass
class ConversionResult:
    """
    Represents the result of a currency conversion calculation.

    Attributes:
        from_currency    : Source currency code
        to_currency      : Target currency code
        amount           : Original amount provided by the caller
        rate             : Exchange rate used
        converted_amount : Result after applying the rate
        timestamp        : When the conversion was calculated (ISO 8601 string)
    """
    from_currency: str
    to_currency: str
    amount: float
    rate: float
    converted_amount: float
    timestamp: str

    def to_dict(self):
        return {
            "from": self.from_currency,
            "to": self.to_currency,
            "amount": self.amount,
            "rate": self.rate,
            "convertedAmount": self.converted_amount,
            "timestamp": self.timestamp,
        }
