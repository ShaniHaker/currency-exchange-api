# services/exchange_service.py
# All external-API logic and business logic lives here.
# Routes call these functions — they don't need to know HOW data is fetched.
#
# External API used: https://open.er-api.com  (free, no API key required)
#
# Endpoint used:
#   GET https://open.er-api.com/v6/latest/{base_currency}
#
# Example response for /v6/latest/USD:
#   {
#     "result":               "success",
#     "base_code":            "USD",
#     "time_last_update_utc": "Tue, 14 Apr 2026 00:02:31 +0000",
#     "rates": {
#       "USD": 1,
#       "ILS": 3.68,
#       "EUR": 0.92,
#       ...
#     }
#   }

import requests
from flask import current_app
from models.currency import Currency, ExchangeRate, ConversionResult


# ---------------------------------------------------------------------------
# Custom exception
# ---------------------------------------------------------------------------

class ExternalAPIError(Exception):
    """
    Raised when the external exchange-rate API cannot be reached or returns
    an error response. Routes catch this and return a 503 to the caller.
    """
    pass


# ---------------------------------------------------------------------------
# Static currency data (the /currencies list stays hard-coded)
# ---------------------------------------------------------------------------

SUPPORTED_CURRENCIES = {
    "USD": Currency(code="USD", name="US Dollar",      symbol="$"),
    "ILS": Currency(code="ILS", name="Israeli Shekel", symbol="₪"),
    "EUR": Currency(code="EUR", name="Euro",            symbol="€"),
    "GBP": Currency(code="GBP", name="British Pound",  symbol="£"),
    "JPY": Currency(code="JPY", name="Japanese Yen",   symbol="¥"),
}


# ---------------------------------------------------------------------------
# Private helpers
# ---------------------------------------------------------------------------

def _fetch_rates(base_code: str) -> dict:
    """
    Call the open.er-api.com API and return the full rates dict for the
    given base currency.

    Example return value: {"USD": 1, "ILS": 3.68, "EUR": 0.92, ...}

    Raises ExternalAPIError on any network problem or API-level error.
    """
    base_url = current_app.config['EXCHANGERATE_BASE_URL']
    timeout  = current_app.config['EXCHANGERATE_TIMEOUT_SECONDS']

    url = f"{base_url}/latest/{base_code}"

    try:
        # timeout= prevents the app from hanging forever if the API is slow
        response = requests.get(url, timeout=timeout)
        # Raise a Python exception for HTTP error codes like 404 or 500
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise ExternalAPIError("The exchange rate API timed out. Please try again.")
    except requests.exceptions.ConnectionError:
        raise ExternalAPIError(
            "Could not connect to the exchange rate API. "
            "Check your internet connection."
        )
    except requests.exceptions.HTTPError as e:
        raise ExternalAPIError(f"Exchange rate API returned an HTTP error: {e}")

    data = response.json()

    # The API signals errors with  "result": "error"  instead of HTTP codes
    if data.get("result") != "success":
        error_type = data.get("error-type", "unknown error")
        raise ExternalAPIError(f"Exchange rate API error: {error_type}")

    return data


# ---------------------------------------------------------------------------
# Public service functions (called by route handlers)
# ---------------------------------------------------------------------------

def get_all_currencies() -> list[dict]:
    """Return the static list of supported currencies as dictionaries."""
    return [currency.to_dict() for currency in SUPPORTED_CURRENCIES.values()]


def get_exchange_rate(from_code: str, to_code: str) -> ExchangeRate:
    """
    Fetch the live exchange rate from `from_code` to `to_code`.

    Makes one API call:
        GET /v6/latest/{from_code}

    Then reads  data["rates"][to_code]  for the rate.

    Raises ExternalAPIError if the API call fails.
    """
    data = _fetch_rates(from_code)

    rate = data["rates"].get(to_code)
    if rate is None:
        raise ExternalAPIError(
            f"Rate for '{to_code}' was not present in the API response."
        )

    # The API gives us a human-readable UTC string — use it directly.
    timestamp = data["time_last_update_utc"]

    return ExchangeRate(
        from_currency=from_code,
        to_currency=to_code,
        rate=rate,
        timestamp=timestamp,
    )


def convert_currency(from_code: str, to_code: str, amount: float) -> ConversionResult:
    """
    Convert `amount` from `from_code` to `to_code` using the live rate.

    Makes one API call (same endpoint as get_exchange_rate):
        GET /v6/latest/{from_code}

    Then calculates:  converted_amount = amount * rate

    Raises ExternalAPIError if the API call fails.
    """
    data = _fetch_rates(from_code)

    rate = data["rates"].get(to_code)
    if rate is None:
        raise ExternalAPIError(
            f"Rate for '{to_code}' was not present in the API response."
        )

    converted_amount = round(amount * rate, 2)
    timestamp        = data["time_last_update_utc"]

    return ConversionResult(
        from_currency=from_code,
        to_currency=to_code,
        amount=amount,
        rate=rate,
        converted_amount=converted_amount,
        timestamp=timestamp,
    )
