import asyncio

from datetime import datetime, timedelta
from bot.database.models import Rates
from bot.database.engine import session_maker
from sqlalchemy import select, update, insert, delete, and_, or_, not_, any_, desc, asc


async def get_banned_users_by_time(last_time: timedelta = timedelta(hours=2)) -> list:
    async with session_maker() as session:
        results = await session.scalars(
            select(Ban).where(
                or_(Ban.banned_at >= datetime.now() - last_time, Ban.banned_to == None)
            )
        )
        return results.all()


async def get_banned_users(number_of_users: int = 10) -> list:
    async with session_maker() as session:
        results = await session.execute(
            select(Ban.telegram_id, Ban.banned_at)
            .order_by(desc(Ban.banned_at))
            .limit(number_of_users)
        )
        return results.fetchall()


async def is_user_banned(tg_id: int) -> bool:
    async with session_maker() as session:
        result = await session.execute(
            select(Ban.telegram_id).where(
                and_(
                    Ban.telegram_id == tg_id,
                    or_(Ban.banned_to > datetime.now(), Ban.banned_to == None),
                )
            )
        )
        return bool(len(result.scalars().all()))


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


async def main():
    pass
    # print(await get_user_requests())
    # print(await get_spam_users())

    # await save_user_request(tg_id='12345', tg_username='Ivan', search_type='flp_name', search_str='qwe qwe qwe',
    #                         report_url='https://osint-bot.duckdns.org/reports/20240521164914-6090714570-2_3_4.html')


if __name__ == "__main__":
    asyncio.run(main())
