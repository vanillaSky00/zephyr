from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    DATABASE_URL: str = "postgresql+psycopg://admin:password@db:5432/app"
    REDIS_URL: str = "redis://redis:6379/0"
    STORAGE_DIR: str = "/data/uploads"

    # ML
    WHISPER_MODEL: str = "small"
    WHISPER_DEVICE: str = "cpu"      # "cuda" if you have GPU
    WHISPER_COMPUTE_TYPE: str = "int8"
    EMOTION_MODEL: str = "j-hartmann/emotion-english-distilroberta-base"

settings = Settings()
