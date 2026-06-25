from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str
    HOST: str
    PORT: int

    MONGODB_URI: str
    DATABASE_NAME: str

    JWT_SECRET: str

    DISCORD_CLIENT_ID: str
    DISCORD_CLIENT_SECRET: str
    DISCORD_REDIRECT_URI: str

    BOT_TOKEN: str

    class Config:
        env_file = ".env"

settings = Settings()
