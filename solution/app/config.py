import os

from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    SERVER_ADDRESS: str = os.getenv("SERVER_ADDRESS")
    SERVER_PORT: int = os.getenv("SERVER_PORT")

    POSTGRES_CONN: str = os.getenv("POSTGRES_CONN")
    POSTGRES_JDBC_URL: str = os.getenv("POSTGRES_JDBC_URL")
    POSTGRES_USERNAME: str = os.getenv("POSTGRES_USERNAME")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_HOST: str = os.getenv("POSTGRES_HOST")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT")
    POSTGRES_DATABASE: str = os.getenv("POSTGRES_DATABASE")

    @property
    def DATABASE_URL(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USERNAME}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DATABASE}"

    REDIS_HOST: str = os.getenv("REDIS_HOST")
    REDIS_PORT: str = os.getenv("REDIS_PORT")

    ANTIFRAUD_ADDRESS: str = os.getenv("ANTIFRAUD_ADDRESS")

    RANDOM_SECRET: str = os.getenv("RANDOM_SECRET")

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


settings = Settings()
