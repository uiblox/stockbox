# StockBox

A personal web app for organizing stock tickers by investment theme. Enter one or more tickers and StockBox pulls market data, assigns themes automatically, and shows each stock as a single card with theme tags.

## Features

- Add tickers (comma- or space-separated), remove them, or refresh all market data
- Themes assigned automatically from market data: Defensive, Value, Growth, Dividend, Cyclical, High Volatility
- One card per ticker with its themes as tags, plus a key explaining each theme
- Click a tag to filter by theme
- Data persisted in a local SQLite database

## Theme rules

Defined in `app/classifier.py`, so you can adjust the thresholds.

| Theme | Rule |
|---|---|
| Defensive | Consumer Defensive, Utilities or Healthcare sector, or beta < 0.8 |
| Value | P/E between 0 and 15, or P/B between 0 and 1.5 |
| Growth | Revenue growth >= 15% or earnings growth >= 20% |
| Dividend | Dividend yield >= 3% |
| Cyclical | Consumer Cyclical, Industrials, Basic Materials, Energy or Financial Services sector |
| High Volatility | Beta > 1.5 |

Tickers matching no rule are tagged Unclassified.

## Tech stack

Python, FastAPI, SQLAlchemy (SQLite), Jinja2 templates, and `yfinance` for market data. No API keys required.

## Run

```
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/uvicorn app.main:app --reload
```

Open http://localhost:8000. Data is stored in `stockbox.db` in the project folder.

## Notes

- Market data comes from Yahoo Finance via `yfinance`, which is unofficial and can occasionally break or rate-limit. Intended for personal use.
- There is no authentication, so run it locally rather than on a public server.
- Not financial advice.
