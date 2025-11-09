import logging
import os
from pydantic import HttpUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

ENV = os.getenv("ENV", "dev")


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=f".env.{ENV}", env_file_encoding="utf-8", case_sensitive=False
    )

    connection_string: str
    db_name: str

    catalog_api_url: HttpUrl
    inventory_api_url: HttpUrl

    log: int | str = logging.INFO


settings = Settings()  # type: ignore
