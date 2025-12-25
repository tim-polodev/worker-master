from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MONGO_DB_HOST: str
    MONGO_DB_PORT: str
    MONGO_DB_PASSWORD: str
    MONGO_DB_NAME: str
    MONGO_DB_USER: str
    # MONGO_URI = (
    #     f"mongodb://{MONGO_DB_USER}:{MONGO_DB_PASSWORD}@{MONGO_DB_HOST}:{MONGO_DB_PORT}"
    # )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",  # Ignore extra fields in the .env file not defined here
    )

    # class Config:
    #     env_file = ".env"


settings = Settings()
