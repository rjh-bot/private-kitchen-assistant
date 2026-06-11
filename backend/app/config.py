import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    deepseek_api_key: str = ""
    deepseek_base_url: str = "https://api.deepseek.com"
    database_url: str = "sqlite+aiosqlite:///./data/kitchen.db"
    model_name: str = "deepseek-chat"
    embed_model: str = "BAAI/bge-small-zh-v1.5"
    cache_ttl: int = 3600

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
