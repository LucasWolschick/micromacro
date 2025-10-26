import logging
import os
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV = os.getenv("ENV", "dev")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f".env.{ENV}", env_file_encoding="utf-8", case_sensitive=False
    )

    connection_string: str
    db_name: str
    port: int

    log: int | str = logging.INFO


settings = Settings()  # type: ignore
