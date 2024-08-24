import os
from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent


class DevSettings(BaseSettings):
    DEBUG: bool = True
    SECRET_KEY: str = "NOT_A_SECRET"
    ALLOWED_HOSTS: str = "localhost,127.0.0.1,*.trycloudflare.com"

    BOT_TOKEN: str
    FRONT_BASE_URL: str
    BACK_BASE_URL: str

    SQLALCHEMY_DATABASE_URI: str
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False

    GEMINI_API_KEY: str

    # Environment
    model_config = SettingsConfigDict(
        env_file=os.path.join(BASE_DIR, ".env"),
        env_file_encoding='utf-8'
    )


settings = DevSettings()
