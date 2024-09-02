from datetime import datetime, UTC
from typing import Optional, Literal
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import BigInteger, Float

from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine
from sqlalchemy.orm import Mapped, mapped_column

from bot.config import settings


class Base(AsyncAttrs, DeclarativeBase):
    repr_cols_num = 4
    repr_cols = tuple()

    def __repr__(self):
        cols = []
        for idx, col in enumerate(self.__table__.columns.keys()):
            if col in self.repr_cols or idx < self.repr_cols_num:
                cols.append(f"{col}={getattr(self, col)}")

        return f"<{self.__class__.__name__} {', '.join(cols)}>"


class Rates(Base):
    __tablename__ = settings.DB_TABLE_NAME

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    timestamp: Mapped[int] = mapped_column(BigInteger)
    paypal: Mapped[float] = mapped_column(Float)
    xe: Mapped[float] = mapped_column(Float)
    mono_bid: Mapped[float] = mapped_column(Float)
    mono_ask: Mapped[float] = mapped_column(Float)
    obmenka_bid: Mapped[float] = mapped_column(Float)
    obmenka_ask: Mapped[float] = mapped_column(Float)
