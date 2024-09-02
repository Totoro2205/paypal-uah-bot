from bot.utils.logger import logger
from bot.messages.msg_texts import unsupported_content_message
from aiogram import Router, F
from aiogram.types import Message

messages_router = Router(name=__name__)


@messages_router.message(
    F.text
    | F.animation
    | F.document
    | F.file
    | F.video
    | F.photo
    | F.gif
    | F.audio
    | F.sticker
)
async def message_with_unsupported_content(message: Message):
    logger.info(
        f"Unsupported message from user <g>{message.from_user.full_name} ({message.from_user.id})</g>"
    )
    await message.answer_sticker(
        "CAACAgIAAxkBAAINkmZNIk8x2f9eg2LbFGVK0SvRZPiqAAL5GQACRceASCpKdk9ErHumNQQ"
    )
    await message.answer(unsupported_content_message)
