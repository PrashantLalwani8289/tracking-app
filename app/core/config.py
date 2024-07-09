from typing import List

from pydantic import AnyHttpUrl, PostgresDsn
from pydantic_settings import BaseSettings

from app.config import env_variables
# from app.features.aws.secretKey import get_secret_keys

env_data = env_variables()
# keys = get_secret_keys()


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Tracking App"
    PROJECT_VERSION: str = "0.1.0"
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://localhost:3001",
        "http://localhost:3002"
    ]
    POSTGRES_USER: str = env_data["POSTGRES_USER"]
    POSTGRES_PASSWORD: str = env_data["POSTGRES_PASSWORD"]
    POSTGRES_SERVER: str = env_data["POSTGRES_SERVER"]
    POSTGRES_DB: str = env_data["POSTGRES_DB"]
    DATABASE_URI: PostgresDsn = env_data ["DATABASE_URI"]


settings = Settings()
