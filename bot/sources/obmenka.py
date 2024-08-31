import httpx

from bot.utils import logger

headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-US,en;q=0.9",
    "cache-control": "no-cache",
    "content-type": "application/json;charset=UTF-8",
    "dnt": "1",
    "origin": "https://obmenka.od.ua",
    "pragma": "no-cache",
    "priority": "u=1, i",
    "referer": "https://obmenka.od.ua/usd-uah",
    "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
    "x-requested-with": "XMLHttpRequest",
}

json_data = {
    "getrates": True,
    "pairID": 671,
}


async def get_obmenka_rates() -> tuple[float, float] | None:
    logger.debug("Getting Obmenka rates")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url="https://obmenka.od.ua/controls", headers=headers, json=json_data
            )
            response.raise_for_status()
            response_json = response.json()
            return (
                float(response_json["data"]["rate"]["rateBidOpt"]),
                float(response_json["data"]["rate"]["rateAskOpt"]),
            )
    except Exception as _ex:
        logger.error(f"Error while getting <r>Obmenka</r> rate! {repr(_ex)}")
        return None
