#quản lý cấu hình chung , đọc biến môi trường từ file .env
import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_NAME: str = "Predict New Word API"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    MODEL_PATH: str = os.getenv("MODEL_PATH", "models/predict_model.pkl")

    model_config=SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

settings = Settings()