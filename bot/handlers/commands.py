import os
from datetime import datetime
from pathlib import Path

from bot.config import settings
from bot.utils.bot_utils import parse_time
from bot.utils.logger import logger
from bot.messages.msg_texts import help_message, about_message
from bot.database.models import Rates
from bot.database.requests import read_rates
from aiogram import Router
from aiogram.types import Message, FSInputFile
from aiogram.filters import CommandStart, Command, CommandObject
import matplotlib.pyplot as plt

commands_router = Router(name=__name__)


@commands_router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    logger.info(f"Command <y>start</y> from user <g>{message.from_user.id}</g>")
    await message.answer(
        text=f"Hello, <b>{message.from_user.full_name}</b>!\n"
        f"Use bot commands to get rates or chart."
    )


@commands_router.message(Command(commands="rates"))
async def cmd_help(message: Message) -> None:
    logger.info(
        f"Command <y>rates</y> from user <g>{message.from_user.full_name} ({message.from_user.id})</g>"
    )
    rates = await read_rates(number_of_rates=1, start_timestamp=None)
    last_rates: Rates = rates[0][0]
    logger.debug(f"Rates: {last_rates}")

    await message.answer(
        f"Exchange rates 🇺🇸 🇺🇦"
        f"\n{datetime.fromtimestamp(last_rates.timestamp)} (UTC):"
        f"\nPaypal: {last_rates.paypal:.4f}"
        f"\nXE: {last_rates.xe:.4f}"
        f"\nObmenka: {last_rates.obmenka_bid:.2f} / {last_rates.obmenka_ask:.2f}"
        f"\nmonobank: {last_rates.mono_bid:.2f} / {last_rates.mono_ask:.2f}"
    )


@commands_router.message(Command(commands="chart"))
async def cmd_help(message: Message, command: CommandObject) -> None:
    logger.info(
        f"Command <y>chart</y> from user <g>{message.from_user.full_name} ({message.from_user.id})</g>"
    )
    if command.args is None or command.args == []:
        chart_interval = settings.CHART_TIME
    else:
        chart_interval = command.args.split()[0]
    logger.debug(f"Chart time: {chart_interval}")
    chart_start_timestamp = int(
        datetime.timestamp(datetime.today() - parse_time(chart_interval))
    )
    logger.debug(
        f"Start timestamp: {chart_start_timestamp} ({datetime.fromtimestamp(chart_start_timestamp)})"
    )
    rates = await read_rates(
        number_of_rates=None, start_timestamp=chart_start_timestamp
    )
    logger.debug(f"Rates number: {len(rates)}, Rates: {rates}")
    temp_file_name = (
        f"{int(datetime.timestamp(datetime.today()))}-{message.from_user.id}.png"
    )
    temp_image = Path(settings.PROJECT_TEMP, temp_file_name)
    X, Y1, Y2, Y3, Y4, Y5, Y6 = [], [], [], [], [], [], []
    for rate_tuple in rates:
        rate: Rates = rate_tuple[0]
        X.append(datetime.fromtimestamp(rate.timestamp))
        Y1.append(float(rate.paypal))
        Y2.append(float(rate.xe))
        Y3.append(float(rate.obmenka_bid))
        Y4.append(float(rate.obmenka_ask))
        Y5.append(float(rate.mono_bid))
        Y6.append(float(rate.mono_ask))

    plt.plot(X, Y1, color="blue", label="Paypal")
    if settings.CHART_XE:
        plt.plot(X, Y2, color="red", label="XE")
    if settings.CHART_OBMENKA:
        plt.plot(X, Y3, color="lime", label="Obmenka Bid")
        plt.plot(X, Y4, color="green", label="Obmenka Ask")
    if settings.CHART_MONO:
        plt.plot(X, Y5, color="gold", label="mono Bid")
        plt.plot(X, Y6, color="darkorange", label="mono Ask")
    plt.title("USD-UAH")
    plt.xticks(rotation=45)
    plt.grid()
    plt.legend()
    plt.savefig(temp_image)
    plt.close()
    plot_image = FSInputFile(temp_image)
    await message.answer_photo(photo=plot_image)
    if os.path.isfile(temp_image):
        os.remove(temp_image)
        logger.debug(f"File {temp_image} removed")
    else:
        logger.debug(f"Error: {temp_image} file not found")


@commands_router.message(Command(commands="help"))
async def cmd_help(message: Message) -> None:
    logger.info(
        f"Command <y>help</y> from user <g>{message.from_user.full_name} ({message.from_user.id})</g>"
    )
    await message.answer(text=help_message)


@commands_router.message(Command(commands="about"))
async def cmd_about(message: Message) -> None:
    logger.info(
        f"Command <y>about</y> from user <g>{message.from_user.full_name} ({message.from_user.id})</g>"
    )
    await message.answer(text=about_message)
