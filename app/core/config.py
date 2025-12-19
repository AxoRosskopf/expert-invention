from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    NOTION_TOKEN: str
    DATABASE_ID: str

    class Config:
        env_file = ".env"

settings = Settings()