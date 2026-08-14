from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_NAME: str = "AI Log Analyzer"
    APP_VERSION: str = "1.0.0"

    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    MAX_UPLOAD_SIZE_MB: int = 5
    ALLOWED_LOG_EXTENSIONS: set[str] = {".log", ".txt"}

    GEMINI_API_KEY: str

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True,
    )


@lru_cache
def get_settings():
    return Settings()


settings = get_settings()