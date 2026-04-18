# Currency Exchange API

A beginner-friendly RESTful API built with **Flask** and **MongoDB Atlas**, deployed on **Railway**.  
Serves live exchange rates, currency conversion, favorites, and conversion history.

**Live URL:** `https://web-production-4ba4.up.railway.app`

---

## Architecture

```
┌─────────────────────────────────────────┐
│              Android App                │
│         (CurrencyExchangeProject)       │
└────────────────┬────────────────────────┘
                 │ HTTP / REST
┌────────────────▼────────────────────────┐
│           Flask API (Railway)           │
│  ┌──────────┐  ┌──────────┐            │
│  │  routes/ │  │services/ │            │
│  └──────────┘  └──────────┘            │
│  ┌──────────┐  ┌──────────┐            │
│  │  models/ │  │database  │            │
│  └──────────┘  └──────────┘            │
└────────┬──────────────┬────────────────┘
         │              │
┌────────▼──────┐  ┌────▼───────────────┐
│ open.er-api   │  │  MongoDB Atlas     │
│ (exchange     │  │  (favorites +      │
│  rates)       │  │   history)         │
└───────────────┘  └────────────────────┘
```

---

## Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/currencies` | List all supported currencies |
| GET | `/rates?from=USD&to=ILS` | Get live exchange rate |
| GET | `/convert?from=USD&to=ILS&amount=100` | Convert an amount |
| GET | `/favorites` | Get all saved favorites |
| POST | `/favorites` | Save a favorite pair |
| DELETE | `/favorites/<id>` | Delete a favorite |
| GET | `/history` | Get conversion history |

### Example responses

**GET /rates?from=USD&to=ILS**
```json
{
  "from": "USD",
  "to": "ILS",
  "rate": 3.68,
  "timestamp": "Fri, 18 Apr 2026 00:02:31 +0000"
}
```

**GET /convert?from=USD&to=ILS&amount=100**
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

**POST /favorites**
```json
// Request body:
{ "fromCurrency": "USD", "toCurrency": "ILS", "nickname": "Dollar to Shekel" }

// Response (201):
{ "favorite": { "id": "abc123", "fromCurrency": "USD", "toCurrency": "ILS", "nickname": "Dollar to Shekel", "createdAt": "..." } }
```

---

## Project Structure

```
currency-exchange-api/
├── app.py                  # Entry point — creates and wires the Flask app
├── config.py               # App configuration (reads from .env)
├── database.py             # MongoDB connection (single shared client)
├── requirements.txt        # Python dependencies
├── Procfile                # Railway startup command
│
├── routes/                 # One file per endpoint group
│   ├── currencies.py       # GET /currencies
│   ├── rates.py            # GET /rates
│   ├── convert.py          # GET /convert
│   ├── favorites.py        # GET/POST/DELETE /favorites
│   └── history.py          # GET /history
│
├── services/               # Business logic (no Flask imports)
│   ├── exchange_service.py # Calls open.er-api.com
│   ├── favorites_service.py
│   └── history_service.py
│
└── models/                 # Data classes
    ├── currency.py
    ├── favorite.py
    └── history.py
```

---

## Local Setup

```bash
# 1. Clone the repo
git clone https://github.com/ShaniHaker/currency-exchange-api.git
cd currency-exchange-api

# 2. Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Create a .env file
cp .env.example .env
# Edit .env and add your MongoDB Atlas connection string

# 5. Run
python app.py
# Server starts at http://127.0.0.1:5000
```

---

## Environment Variables

| Variable | Description |
|----------|-------------|
| `MONGO_URI` | MongoDB Atlas connection string |
| `MONGO_DB_NAME` | Database name (default: `currency_exchange`) |

> MongoDB is **optional** — `/currencies`, `/rates`, and `/convert` work without it.  
> Only `/favorites` and `/history` require a database connection.

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| Framework | Flask 3 |
| Database | MongoDB Atlas (via pymongo) |
| Exchange rates | [open.er-api.com](https://open.er-api.com) (free, no key) |
| Deployment | Railway |

---

## License

MIT — see [LICENSE](LICENSE)
