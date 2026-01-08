from pydantic_settings import BaseSettings, SettingsConfigDict

class DatabaseSettings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="DB_", env_file=".env", env_file_encoding="utf-8", extra="ignore")
    HOST: str = "localhost"
    USER: str = "keyler_sa"
    PORT: int = 5433
    PASSWORD: str | None = None
    NAME: str = "db"
    @property
    def url_connection(self) -> str:
        return f"postgresql://{self.USER}:{self.PASSWORD}@{self.HOST}:{self.PORT}/{self.NAME}"

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")
    SECRET_KEY: str = "keyler"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    ENVIRONMENT: str = "DEV"
    @property
    def DATABASE(self) -> DatabaseSettings:
        return DatabaseSettings()

settings = Settings()