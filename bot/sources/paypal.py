import httpx
import json
import re

from bot.utils import logger


headers = {
    "authority": "www.paypal.com",
    "accept": "*/*",
    "accept-language": "ru,en-US;q=0.9,en;q=0.8",
    "cache-control": "no-cache",
    "dnt": "1",
    "pragma": "no-cache",
    "referer": "https://www.paypal.com/lu/cshelp/article/where-can-i-find-paypals-currency-calculator-and-exchange-rates-help109",
    "sec-ch-ua": '"Chromium";v="122", "Not(A:Brand";v="24", "Google Chrome";v="122"',
    "sec-ch-ua-arch": '"arm"',
    "sec-ch-ua-bitness": '"64"',
    "sec-ch-ua-full-version": '"122.0.6261.69"',
    "sec-ch-ua-full-version-list": '"Chromium";v="122.0.6261.69", "Not(A:Brand";v="24.0.0.0", "Google Chrome";v="122.0.6261.69"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-model": '""',
    "sec-ch-ua-platform": '"macOS"',
    "sec-ch-ua-platform-version": '"14.3.1"',
    "sec-ch-ua-wow64": "?0",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
}

params = {
    "fromCountry": "UA",
    "toCountry": "UA",
    "fromPaymentCurrency": "USD",
    "toTransCurrency": "UAH",
    "tType": "FX_ON_BALANCE_TRANSFER",
    "transAmount": "100",
    "component": "helpcenternodeweb",
}


async def get_paypal_rate() -> float | None:
    logger.debug("Getting Paypal rates")
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url="https://www.paypal.com/smarthelp/currency-conversion",
                params=params,
            )
            response.raise_for_status()
            response_json = json.loads(response.text)["result"]
            match = re.search("=(.+?)UAH", response_json)
            return float(match.group(1).strip())
    except Exception as _ex:
        logger.error(f"Error while getting <r>Paypal</r> rate! {repr(_ex)}")
        return None
