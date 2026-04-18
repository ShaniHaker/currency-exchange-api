# Currency Exchange API — Documentation

**Live API:** [https://web-production-4ba4.up.railway.app](https://web-production-4ba4.up.railway.app)  
**GitHub:** [ShaniHaker/currency-exchange-api](https://github.com/ShaniHaker/currency-exchange-api)

---

## Endpoints

### GET /currencies
Returns all supported currencies.

**Request:**
```
GET /currencies
```
**Response:**
```json
{
  "currencies": [
    { "code": "USD", "name": "US Dollar", "symbol": "$" },
    { "code": "ILS", "name": "Israeli Shekel", "symbol": "₪" },
    { "code": "EUR", "name": "Euro", "symbol": "€" },
    { "code": "GBP", "name": "British Pound", "symbol": "£" },
    { "code": "JPY", "name": "Japanese Yen", "symbol": "¥" }
  ]
}
```

---

### GET /rates
Returns the live exchange rate between two currencies.

**Request:**
```
GET /rates?from=USD&to=ILS
```
**Response:**
```json
{
  "from": "USD",
  "to": "ILS",
  "rate": 3.68,
  "timestamp": "Fri, 18 Apr 2026 00:02:31 +0000"
}
```

---

### GET /convert
Converts an amount from one currency to another. Also saves a record to history.

**Request:**
```
GET /convert?from=USD&to=ILS&amount=100
```
**Response:**
```json
{
  "from": "USD",
  "to": "ILS",
  "amount": 100.0,
  "rate": 3.68,
  "convertedAmount": 368.0,
  "timestamp": "Fri, 18 Apr 2026 00:02:31 +0000"
}
```

---

### GET /favorites
Returns all saved favorite currency pairs.

**Response:**
```json
{
  "favorites": [
    {
      "id": "abc123",
      "fromCurrency": "USD",
      "toCurrency": "ILS",
      "nickname": "Dollar to Shekel",
      "createdAt": "2026-04-18T10:00:00+00:00"
    }
  ]
}
```

---

### POST /favorites
Saves a new favorite currency pair.

**Request body:**
```json
{ "fromCurrency": "USD", "toCurrency": "ILS", "nickname": "Dollar to Shekel" }
```
**Response (201):**
```json
{
  "favorite": {
    "id": "abc123",
    "fromCurrency": "USD",
    "toCurrency": "ILS",
    "nickname": "Dollar to Shekel",
    "createdAt": "2026-04-18T10:00:00+00:00"
  }
}
```

---

### DELETE /favorites/{id}
Deletes a saved favorite by its ID.

**Response:**
```json
{ "message": "Favorite 'abc123' deleted successfully." }
```

---

### GET /history
Returns all past conversions, most recent first.

**Response:**
```json
{
  "history": [
    {
      "id": "xyz789",
      "fromCurrency": "USD",
      "toCurrency": "ILS",
      "amount": 100.0,
      "rate": 3.68,
      "convertedAmount": 368.0,
      "createdAt": "2026-04-18T10:00:00+00:00"
    }
  ]
}
```

---

## Error Responses

| Status | Meaning |
|--------|---------|
| 400 | Missing or invalid parameters |
| 404 | Resource not found |
| 503 | External API or database unavailable |

```json
{ "error": "Both 'from' and 'to' query parameters are required." }
```
