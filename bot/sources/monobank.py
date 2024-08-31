import httpx

from bot.utils import logger


async def get_mono_rates() -> tuple[float, float] | None:
    logger.debug("Getting monobank rates")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url="https://api.monobank.ua/bank/currency")
            response.raise_for_status()
            response_json = response.json()
            for pair in response_json:
                if pair["currencyCodeA"] == 840 and pair["currencyCodeB"] == 980:
                    return float(pair["rateBuy"]), float(pair["rateSell"])
    except Exception as _ex:
        logger.error(f"Error while getting <r>monobank</r> rate! {repr(_ex)}")
        return None
