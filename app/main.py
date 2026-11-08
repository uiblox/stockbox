import re
from datetime import datetime
from pathlib import Path

from fastapi import Depends, FastAPI, Form, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import select
from sqlalchemy.orm import Session

from . import market
from .classifier import THEME_DESCRIPTIONS, classify
from .db import Base, engine, get_db
from .models import Ticker, TickerTheme

Base.metadata.create_all(engine)

app = FastAPI(title="StockBox")
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")

SYMBOL_RE = re.compile(r"^[A-Z0-9.\-^=]{1,16}$")


def refresh(db: Session, t: Ticker) -> None:
    """Pull fresh market data for a ticker and re-assign its themes."""
    try:
        for k, v in market.fetch(t.symbol).items():
            setattr(t, k, v)
        t.error = None
        t.themes = [TickerTheme(theme=name) for name in classify(t)]
    except Exception as e:  # network or unknown symbol
        t.error = str(e)[:300]
    t.updated_at = datetime.utcnow()


@app.get("/")
def index(request: Request, theme: str | None = None, db: Session = Depends(get_db)):
    tickers = db.scalars(select(Ticker).order_by(Ticker.symbol)).all()
    order = list(THEME_DESCRIPTIONS) + ["Unclassified"]
    for t in tickers:
        t.tags = sorted((tt.theme for tt in t.themes), key=order.index)
    counts = {n: sum(n in t.tags for t in tickers) for n in order}
    shown = [t for t in tickers if theme in t.tags] if theme else tickers
    return templates.TemplateResponse(
        request,
        "index.html",
        {
            "tickers": shown,
            "total": len(tickers),
            "key": [(n, THEME_DESCRIPTIONS.get(n, "No theme rules matched"), counts[n]) for n in order],
            "active": theme,
            "failed": [t for t in tickers if t.error],
        },
    )


@app.post("/tickers")
def add_tickers(symbols: str = Form(...), db: Session = Depends(get_db)):
    for sym in re.split(r"[\s,;]+", symbols.upper().strip()):
        if not sym or not SYMBOL_RE.match(sym):
            continue
        if db.scalar(select(Ticker).where(Ticker.symbol == sym)):
            continue
        t = Ticker(symbol=sym)
        db.add(t)
        refresh(db, t)
        if t.error and t.name is None:  # unknown symbol: don't keep it
            db.expunge(t)
            continue
        db.commit()
    return RedirectResponse("/", status_code=303)


@app.post("/tickers/{symbol}/delete")
def delete_ticker(symbol: str, db: Session = Depends(get_db)):
    t = db.scalar(select(Ticker).where(Ticker.symbol == symbol))
    if t:
        db.delete(t)
        db.commit()
    return RedirectResponse("/", status_code=303)


@app.post("/refresh")
def refresh_all(db: Session = Depends(get_db)):
    for t in db.scalars(select(Ticker)).all():
        refresh(db, t)
    db.commit()
    return RedirectResponse("/", status_code=303)
