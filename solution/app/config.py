from pydantic_settings import SettingsConfigDict, BaseSettings


class Settings(BaseSettings):
    SERVER_ADDRESS: str
    SERVER_PORT: int

    POSTGRES_CONN: str
    POSTGRES_JDBC_URL: str
    POSTGRES_USERNAME: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: str
    POSTGRES_DATABASE: str

    REDIS_HOST: str
    REDIS_PORT: str

    ANTIFRAUD_ADDRESS: str

    RANDOM_SECRET: str

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


settings = Settings()
