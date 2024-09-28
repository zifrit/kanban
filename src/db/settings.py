from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # db_url: str = "sqlite+aiosqlite:///./db.sqlite3"
    db_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/postgres"


settings = Settings()
