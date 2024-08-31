import sys

from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_ignore_empty=True)

    BOT_TOKEN: str = "ask:BotFather"
    DB: str = "/paypal.sqlite"
    DB_TABLE_NAME: str = "rates"
    RATES_INTERVAL: int = 1200
    TEMP_FOLDER: str = "tmp"

    CHART_XE: bool = True
    CHART_MONO: bool = True
    CHART_OBMENKA: bool = True
    CHART_TIME: str = "1w"

    LOGGING_LEVEL: str = "INFO"
    PROJECT_ROOT: Path = Path(sys.modules["__main__"].__file__).resolve().parents[0]
    PROJECT_TEMP: Path = Path(PROJECT_ROOT, TEMP_FOLDER)


settings = Settings()
