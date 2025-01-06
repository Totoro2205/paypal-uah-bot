import httpx

from bot.utils import logger

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9,zh;q=0.8,pt-BR;q=0.7,pt;q=0.6,zh-CN;q=0.5,uk;q=0.4,ru-UA;q=0.3,ru;q=0.2,uk-UA;q=0.1,ru-RU;q=0.1',
    'cache-control': 'no-cache',
    'content-type': 'application/json;charset=UTF-8',
    # 'cookie': 'PHPSESSID=4eamv9iflh6rs11qcnhqpk5fr4; sbjs_migrations=1418474375998%3D1; sbjs_current_add=fd%3D2025-01-06%2013%3A07%3A36%7C%7C%7Cep%3Dhttps%3A%2F%2Fkyt-obmin.od.ua%2F%7C%7C%7Crf%3D%28none%29; sbjs_first_add=fd%3D2025-01-06%2013%3A07%3A36%7C%7C%7Cep%3Dhttps%3A%2F%2Fkyt-obmin.od.ua%2F%7C%7C%7Crf%3D%28none%29; sbjs_current=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29; sbjs_first=typ%3Dtypein%7C%7C%7Csrc%3D%28direct%29%7C%7C%7Cmdm%3D%28none%29%7C%7C%7Ccmp%3D%28none%29%7C%7C%7Ccnt%3D%28none%29%7C%7C%7Ctrm%3D%28none%29; sbjs_udata=vst%3D1%7C%7C%7Cuip%3D%28none%29%7C%7C%7Cuag%3DMozilla%2F5.0%20%28Macintosh%3B%20Intel%20Mac%20OS%20X%2010_15_7%29%20AppleWebKit%2F537.36%20%28KHTML%2C%20like%20Gecko%29%20Chrome%2F131.0.0.0%20Safari%2F537.36; _gcl_au=1.1.1973593053.1736161661; _ga=GA1.1.1608883401.1736161662; _fbp=fb.2.1736161661796.33399329387546777; wujs_rates_is_opt=1; _st=1736162684; sbjs_session=pgs%3D4%7C%7C%7Ccpg%3Dhttps%3A%2F%2Fkyt-obmin.od.ua%2F; _ga_EG153ERKS4=GS1.1.1736161661.1.1.1736162699.45.0.0; biatv-cookie={%22firstVisitAt%22:1736161661%2C%22visitsCount%22:1%2C%22currentVisitStartedAt%22:1736161661%2C%22currentVisitLandingPage%22:%22https://kyt-obmin.od.ua/%22%2C%22currentVisitUpdatedAt%22:1736162699%2C%22currentVisitOpenPages%22:4%2C%22campaignTime%22:1736161661%2C%22campaignCount%22:1%2C%22utmDataCurrent%22:{%22utm_source%22:%22(direct)%22%2C%22utm_medium%22:%22(none)%22%2C%22utm_campaign%22:%22(direct)%22%2C%22utm_content%22:%22(not%20set)%22%2C%22utm_term%22:%22(not%20set)%22%2C%22beginning_at%22:1736161661}%2C%22utmDataFirst%22:{%22utm_source%22:%22(direct)%22%2C%22utm_medium%22:%22(none)%22%2C%22utm_campaign%22:%22(direct)%22%2C%22utm_content%22:%22(not%20set)%22%2C%22utm_term%22:%22(not%20set)%22%2C%22beginning_at%22:1736161661}}; bingc-activity-data={%22numberOfImpressions%22:2%2C%22activeFormSinceLastDisplayed%22:75%2C%22pageviews%22:3%2C%22callWasMade%22:0%2C%22updatedAt%22:1736162774}',
    'dnt': '1',
    'origin': 'https://kyt-obmin.od.ua',
    'pragma': 'no-cache',
    'priority': 'u=1, i',
    'referer': 'https://kyt-obmin.od.ua/',
    'sec-ch-ua': '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"macOS"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
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
                url="https://kyt-obmin.od.ua/controls", headers=headers, json=json_data
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
