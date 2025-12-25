from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MONGO_DB_HOST: str
    MONGO_DB_PORT: str
    MONGO_DB_PASSWORD: str
    MONGO_DB_NAME: str
    MONGO_DB_USER: str
    REQUEST_LIMITER: str = "5/minute"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # Ignore extra fields in the .env file not defined here
    )


settings = Settings()
