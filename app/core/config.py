from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Plum API"
    DATABASE_URL: str = "sqlite:///./app.db"
    DEBUG: bool = True

    class Config:
        env_file = ".env"

settings = Settings()