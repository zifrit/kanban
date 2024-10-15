from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USER: str = "postgres"
    DB_PASS: str = "postgres"
    DB_NAME: str = "postgres"
    PROJECT_TITLE: str = "my_app"
    CRYPTO_SECRET_KEY: str = (
        "5f8e99e562ba9cbf399134a33209bd477910d6cf4f48a0ad3e5d240773c8e7de"
    )
    CRYPTO_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    PROJECT_HOST: str = "localhost"
    PROJECT_PORT: int = 8000
    HOST_URL: str = f"http://{PROJECT_HOST}:{PROJECT_PORT}"
    ALLOWED_ORIGINS: str = (
        "http://0.0.0.0, http://127.0.0.1, http://localhost, http://app"
    )
    MAX_SIZE_FILE: int = 1024 * 1024  # 1 mb

    @property
    def DATABASE_URL_ASYNC(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()
