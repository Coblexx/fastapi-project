from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_URL: str


DB_URL = Settings().DB_URL
