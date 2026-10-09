from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings (BaseSettings):
    app_name: str = "POS BACKEND"
    debug: bool = False
    database_url : str 
    secret_key : str
    access_token_expire_minutes : int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings ()