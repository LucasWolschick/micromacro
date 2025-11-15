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

    queues_connection_string: str

    log: int | str = logging.INFO


settings = Settings()  # type: ignore
