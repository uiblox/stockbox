"""Rule-based theme assignment. Tweak the thresholds here."""

DEFENSIVE_SECTORS = {"Consumer Defensive", "Utilities", "Healthcare"}
CYCLICAL_SECTORS = {
    "Consumer Cyclical", "Industrials", "Basic Materials", "Energy", "Financial Services",
}

THEME_DESCRIPTIONS = {
    "Defensive": "Defensive sector (staples, utilities, healthcare) or beta < 0.8",
    "Value": "P/E between 0 and 15, or P/B between 0 and 1.5",
    "Growth": "Revenue growth >= 15% or earnings growth >= 20%",
    "Dividend": "Dividend yield >= 3%",
    "Cyclical": "Economically sensitive sector (industrials, energy, financials, ...)",
    "High Volatility": "Beta > 1.5",
}


def classify(t) -> list[str]:
    """t needs: sector, beta, pe, pb, dividend_yield, revenue_growth, earnings_growth."""
    themes = []
    if t.sector in DEFENSIVE_SECTORS or (t.beta is not None and t.beta < 0.8):
        themes.append("Defensive")
    if (t.pe is not None and 0 < t.pe <= 15) or (t.pb is not None and 0 < t.pb <= 1.5):
        themes.append("Value")
    if (t.revenue_growth is not None and t.revenue_growth >= 15) or (
        t.earnings_growth is not None and t.earnings_growth >= 20
    ):
        themes.append("Growth")
    if t.dividend_yield is not None and t.dividend_yield >= 3:
        themes.append("Dividend")
    if t.sector in CYCLICAL_SECTORS:
        themes.append("Cyclical")
    if t.beta is not None and t.beta > 1.5:
        themes.append("High Volatility")
    return themes or ["Unclassified"]
