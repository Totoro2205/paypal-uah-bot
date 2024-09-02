import re
import json

from datetime import timedelta

import httpx
from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault
from bot.database.engine import drop_tables, create_tables


async def set_commands(bot: Bot) -> None:
    commands = [
        BotCommand(command="start", description="Start the bot"),
        BotCommand(command="rates", description="Get rates"),
        BotCommand(command="chart", description="Display chart"),
        BotCommand(command="help", description="How to use the bot"),
        BotCommand(command="about", description="About the bot"),
    ]
    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())


async def on_startup() -> None:
    await create_tables()
    pass


async def on_shutdown() -> None: ...


async def identify_myself() -> str:
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://ipapi.co/json/")
            location = json.loads(response.text)
            return (
                f'IP: {location["ip"]}, '
                f'Location: {location["city"]}, '
                f'{location["region"]}, '
                f'{location["country_name"]}'
            )
    except:
        return "Unknown IP"


def parse_time(time_str: str | None) -> timedelta:
    if not time_str:
        return timedelta(seconds=0)
    match_ = re.match(r"(\d+)([a-z])", time_str.lower().strip())
    if match_:
        value, unit = int(match_.group(1)), match_.group(2)
        match unit:
            case "h":
                time_delta = timedelta(hours=value)
            case "d":
                time_delta = timedelta(days=value)
            case "w":
                time_delta = timedelta(weeks=value)
            case _:
                return timedelta(seconds=0)
    else:
        return timedelta(seconds=0)
    return time_delta
