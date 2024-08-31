import httpx

from bot.utils import logger

cookies = {
    "optimizelyOptOut": "true",
    "userId": "51d85a3d-6148-44a9-bce4-4b4baf12a671",
    "xeConsentState": "{%22performance%22:true%2C%22marketing%22:true%2C%22compliance%22:false}",
    "amp_470887": "Ezeu8HuvwTURv8otfblQX0...1hj846jq4.1hj847fh1.p.5.u",
    "lastConversion": "{%22amount%22:1%2C%22fromCurrency%22:%22USD%22%2C%22toCurrency%22:%22UAH%22}",
}

headers = {
    "authority": "www.xe.com",
    "accept": "*/*",
    "accept-language": "ru,en-US;q=0.9,en;q=0.8",
    "authorization": "Basic bG9kZXN0YXI6cHVnc25heA==",
    "cache-control": "no-cache",
    "dnt": "1",
    "pragma": "no-cache",
    "referer": "https://www.xe.com/currencycharts/?from=USD&to=UAH&view=1W",
    "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
}

params = {
    "currencyPairs": ["USD/UAH"],
}


async def get_xe_rate() -> float | None:
    logger.debug("Getting XE rates")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url="https://www.xe.com/api/protected/live-currency-rates/",
                headers=headers,
                params=params,
                cookies=cookies,
            )
            response.raise_for_status()
            response_json = response.json()[0]
            return float(response_json["rate"])
    except Exception as _ex:
        logger.error(f"Error while getting <r>XE</r> rate! {repr(_ex)}")
        return None
