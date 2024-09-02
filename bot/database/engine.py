import asyncio
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)

from bot.config.config import settings
from bot.database.models import Base, Rates


engine = create_async_engine(
    url=f"sqlite+aiosqlite://{settings.DB}",
    echo=True if settings.LOGGING_LEVEL == "DEBUG" else False,
)

session_maker = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def create_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_tables() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


async def main():
    await drop_tables()
    await create_tables()


if __name__ == "__main__":
    asyncio.run(main())
