from pydantic_settings import BaseSettings
from pydantic import Field
from typing import List

class Settings(BaseSettings):
    gemini_api_key: str = Field("", alias="GEMINI_API_KEY")
    data_dir: str = "data"
    database_url: str = "sqlite+aiosqlite:///./data/app.db"
    cors_allow_origins: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]
    gemini_model: str = "gemini-2.5-flash"

    class Config:
        env_file = ".env"

settings = Settings()