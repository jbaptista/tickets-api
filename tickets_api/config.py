from pydantic import BaseModel, SecretStr
from pydantic_settings import BaseSettings, SettingsConfigDict


class Database(BaseModel):
    user: str
    password: SecretStr
    host: str
    port: int
    db_name: str

    @property
    def url(self):
        return f"postgresql+asyncpg://{self.user}:{self.password.get_secret_value()}@{self.host}:{self.port}/{self.db_name}"


class Config(BaseSettings):
    model_config = SettingsConfigDict(
        env_nested_delimiter="__", env_file=".env", env_file_encoding="utf-8"
    )

    log_level: str = "INFO"
    is_local: bool = False
    version: str = "unknown"
    database: Database = Database(
        user="postgres",
        password=SecretStr("postgres"),
        host="localhost",
        port=5432,
        db_name="postgres",
    )
    account_service_url: str = "https://jsonplaceholder.typicode.com"
