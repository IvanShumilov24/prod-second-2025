import os

from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings:
    SERVER_ADDRESS = os.getenv("SERVER_ADDRESS")
    SERVER_PORT= os.getenv("SERVER_PORT")

    POSTGRES_CONN = os.getenv("POSTGRES_CONN")
    POSTGRES_JDBC_URL = os.getenv("POSTGRES_JDBC_URL")
    POSTGRES_USERNAME = os.getenv("POSTGRES_USERNAME", "postgres")
    POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_HOST = os.getenv("POSTGRES_HOST", "postgres")
    POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_DATABASE = os.getenv("POSTGRES_DATABASE", "prod")

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USERNAME}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DATABASE}"

    REDIS_HOST = os.getenv("REDIS_HOST")
    REDIS_PORT = os.getenv("REDIS_PORT")

    ANTIFRAUD_ADDRESS = os.getenv("ANTIFRAUD_ADDRESS")

    RANDOM_SECRET = os.getenv("RANDOM_SECRET")

    # model_config = SettingsConfigDict(env_file=".env", extra="allow")


settings = Settings()
