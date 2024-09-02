from datetime import datetime
from bot.database.models import Rates
from bot.database.engine import session_maker
from sqlalchemy import select, insert, desc, asc


async def save_rates(
    paypal: float,
    xe: float,
    mono_bid: float,
    mono_ask: float,
    obmenka_bid: float,
    obmenka_ask: float,
) -> None:
    async with session_maker() as session:
        await session.execute(
            insert(Rates).values(
                timestamp=int(datetime.timestamp(datetime.today())),
                paypal=paypal,
                xe=xe,
                mono_bid=mono_bid,
                mono_ask=mono_ask,
                obmenka_bid=obmenka_bid,
                obmenka_ask=obmenka_ask,
            )
        )

        await session.commit()


async def read_rates(number_of_rates: int | None, start_timestamp: int | None) -> list:
    if number_of_rates is None:
        if start_timestamp is None:
            async with session_maker() as session:
                results = await session.execute(
                    select(Rates).order_by(desc("timestamp"))
                )
        else:
            async with session_maker() as session:
                results = await session.execute(
                    select(Rates)
                    .where(Rates.timestamp >= start_timestamp)
                    .order_by(asc("timestamp"))
                )
    else:
        async with session_maker() as session:
            results = await session.execute(
                select(Rates).order_by(desc("timestamp")).limit(number_of_rates)
            )
    return results.all()
