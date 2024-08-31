import sys
from loguru import logger
from bot.config.config import settings

logger.remove()
logger.add(
    sink=sys.stdout,
    format="<white>{time:YYYY-MM-DD HH:mm:ss}</white>"
    " | <level>{level: <8}</level>"
    " | <cyan><b>{module}:{line}</b></cyan>"
    " | <white><b>{message}</b></white>",
    level=settings.LOGGING_LEVEL,
)
logger = logger.opt(colors=True)
