from pydantic_settings import BaseSettings


import os
from dotenv import load_dotenv

if os.path.exists(".env.local"):
    load_dotenv(".env.local")
else:
    load_dotenv()


class Settings(BaseSettings):
    ENV: str
    POSTGRES_CONN_STRING: str
    FF_PREDICTION_MODEL_NAME: str
    FF_PREDICTION_PREPROCESSOR_NAME: str
    API_BASE: str
    MLFLOW_TRACKING_URI: str

    class Config:
        env_file = ".env.local" if os.path.exists(".env.local") else ".env"
        env_file_encoding = 'utf-8'


settings = Settings()
