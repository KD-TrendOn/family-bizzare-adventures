from pathlib import Path
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from os import getenv


load_dotenv()


class DbSettings(BaseModel):
    url: str = getenv("DATABASE_URL")
    # echo: bool = False
    echo: bool = True


class Settings(BaseSettings):
    api_v1_prefix: str = "/api/v1"
    db: DbSettings = DbSettings()
    # db_echo: bool = True


settings = Settings()
