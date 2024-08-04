from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter="__", env_file=".env", env_file_encoding="utf-8"
    )

    log_level: str = "INFO"
    is_local: bool = False
    version: str = "unknown"
