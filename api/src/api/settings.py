from pydantic_settings import BaseSettings


import os
from dotenv import load_dotenv

if os.path.exists(".env.local"):
    load_dotenv(".env.local")
else:
    load_dotenv()


class Settings(BaseSettings):
    POSTGRES_CONN_STRING: str
    UI_URL: str

    class Config:
        env_file = ".env.local" if os.path.exists(".env.local") else ".env"
        env_file_encoding = 'utf-8'


settings = Settings()
