import asyncio

from bot.config import settings
from bot.sources.paypal import get_paypal_rate
from bot.sources.obmenka import get_obmenka_rates
from bot.sources.xe import get_xe_rate
from bot.sources.monobank import get_mono_rates
from bot.utils import logger
from bot.database.requests import save_rates


async def rates_worker():
    while True:
        try:
            paypal_rate = await get_paypal_rate()
            if paypal_rate:
                logger.debug(f"Paypal: 1 USD = {paypal_rate:.4f} UAH")
            else:
                logger.error(f"Can't get Paypal rate")

            obmenka_bid, obmenka_ask = await get_obmenka_rates()
            if obmenka_bid and obmenka_ask:
                logger.debug(
                    f"Obmenka: Bid - 1 USD = {obmenka_bid:.2f} UAH, Ask - 1 USD = {obmenka_ask:.2f} UAH"
                )
            else:
                logger.error(f"Can't get Obmenka rates")

            xe_rate = await get_xe_rate()
            if xe_rate:
                logger.debug(f"XE: 1 USD = {xe_rate:.4f} UAH")
            else:
                logger.error(f"Can't get XE rate")

            mono_bid, mono_ask = await get_mono_rates()
            if mono_bid and mono_ask:
                logger.debug(
                    f"monobank: Bid - 1 USD = {mono_bid:.2f} UAH, Ask - 1 USD = {mono_ask:.2f} UAH"
                )
            else:
                logger.error(f"Can't get monobank rates")

            await save_rates(
                paypal=paypal_rate,
                xe=xe_rate,
                mono_bid=mono_bid,
                mono_ask=mono_ask,
                obmenka_bid=obmenka_bid,
                obmenka_ask=obmenka_ask,
            )

        except Exception as _ex:
            logger.debug(f"Exception in rates worker: {repr(_ex)}")
        await asyncio.sleep(settings.RATES_INTERVAL)
