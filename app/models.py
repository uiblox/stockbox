from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .db import Base


class Ticker(Base):
    __tablename__ = "tickers"

    id: Mapped[int] = mapped_column(primary_key=True)
    symbol: Mapped[str] = mapped_column(String(16), unique=True, index=True)
    name: Mapped[str | None] = mapped_column(String(200))
    sector: Mapped[str | None] = mapped_column(String(100))
    price: Mapped[float | None] = mapped_column(Float)
    beta: Mapped[float | None] = mapped_column(Float)
    pe: Mapped[float | None] = mapped_column(Float)
    pb: Mapped[float | None] = mapped_column(Float)
    dividend_yield: Mapped[float | None] = mapped_column(Float)  # percent, e.g. 3.2
    revenue_growth: Mapped[float | None] = mapped_column(Float)  # percent
    earnings_growth: Mapped[float | None] = mapped_column(Float)  # percent
    updated_at: Mapped[datetime | None] = mapped_column(DateTime)
    error: Mapped[str | None] = mapped_column(String(300))

    themes: Mapped[list["TickerTheme"]] = relationship(
        back_populates="ticker", cascade="all, delete-orphan"
    )


class TickerTheme(Base):
    __tablename__ = "ticker_themes"

    ticker_id: Mapped[int] = mapped_column(ForeignKey("tickers.id"), primary_key=True)
    theme: Mapped[str] = mapped_column(String(50), primary_key=True)

    ticker: Mapped[Ticker] = relationship(back_populates="themes")
