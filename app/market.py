import yfinance as yf


def _pct(x):
    return round(x * 100, 2) if isinstance(x, (int, float)) else None


def fetch(symbol: str) -> dict:
    """Return fundamentals for a symbol. Raises ValueError if it isn't a real ticker."""
    info = yf.Ticker(symbol).info or {}
    price = info.get("currentPrice") or info.get("regularMarketPrice") or info.get("previousClose")
    if price is None and not info.get("shortName"):
        raise ValueError(f"No market data found for '{symbol}'")

    # Compute yield from the annual dividend rate; yfinance's dividendYield
    # field has changed units between versions.
    rate = info.get("dividendRate")
    div_yield = round(rate / price * 100, 2) if rate and price else 0.0

    return {
        "name": info.get("shortName") or info.get("longName"),
        "sector": info.get("sector"),
        "price": price,
        "beta": info.get("beta"),
        "pe": info.get("trailingPE"),
        "pb": info.get("priceToBook"),
        "dividend_yield": div_yield,
        "revenue_growth": _pct(info.get("revenueGrowth")),
        "earnings_growth": _pct(info.get("earningsGrowth")),
    }
