from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    rawg_api_key: str
    database_url: str = "sqlite:///./library.db"
    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
