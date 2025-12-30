from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    NOTION_TOKEN: str
    DATABASE_ID: str
    DATABASE_URL: str

    class Config:
        env_file = ".env"

settings = Settings()