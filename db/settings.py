from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    db_url: str = "sqlite+aiosqlite:///./db.sqlite3"


settings = Settings()
